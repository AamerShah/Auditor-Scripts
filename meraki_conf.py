#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import csv

# --------------------- VENV & DEPENDENCY CHECK ---------------------
REQUIRED_MODULES = ["meraki", "colorama"]

def create_or_activate_venv():
    venv_path = os.path.join(os.getcwd(), ".meraki_venv")
    activate_script = os.path.join(venv_path, "bin", "activate_this.py")
    if not os.path.exists(venv_path):
        print("[*] Creating virtual environment in .meraki_venv...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("[+] Virtual environment created.")
    # Install missing modules
    python_bin = os.path.join(venv_path, "bin", "python")
    pip_bin = os.path.join(venv_path, "bin", "pip")
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
        except ModuleNotFoundError:
            print(f"[*] Installing missing dependency: {module}")
            subprocess.check_call([pip_bin, "install", module])
    # Re-run script inside venv if not already
    if sys.prefix != os.path.abspath(venv_path):
        print("[*] Switching to virtual environment...")
        os.execv(python_bin, [python_bin] + sys.argv)

create_or_activate_venv()

# --------------------- IMPORT MODULES ---------------------
import meraki
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ================= CONFIG =================
API_KEY = ""
VERBOSE = True

# --------------------- HELPERS ---------------------
def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(Fore.RED + f"[-] {func.__name__} error: {e}")
        return None

def print_header(title):
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*10 + f" {title} " + "="*10)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def save_csv(path, rows, headers=["Category","Issue"]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not rows:
        print(Fore.YELLOW + f"[!] No issues for {os.path.basename(path)}, skipping CSV.")
        return
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

# --------------------- AUDIT FUNCTIONS ---------------------
def audit_vpn(vpn_config):
    issues = []
    if not vpn_config:
        issues.append("No VPN config found")
    elif vpn_config.get("mode") != "hub-and-spoke":
        issues.append(f"VPN mode is '{vpn_config.get('mode')}', recommended: hub-and-spoke")
    return issues

def audit_firewall(fw_rules):
    issues = []
    if not fw_rules:
        issues.append("No firewall rules found")
    else:
        for rule in fw_rules:
            if rule.get("policy") == "allow" and rule.get("destCidr") == "any":
                issues.append("Overly permissive firewall rule: allow any -> any")
    return issues

def audit_wireless(ssids):
    issues = []
    if not ssids:
        issues.append("No SSIDs found")
    else:
        for s in ssids:
            if not s.get("enabled", False):
                continue
            if s.get("authMode") == "open":
                issues.append(f"SSID '{s['name']}' is open (no auth)")
            enc = s.get("encryptionMode","").lower()
            if "wpa" in enc and "wpa3" not in enc:
                issues.append(f"SSID '{s['name']}' does not enforce WPA3")
            if not s.get("wipsEnabled", False):
                issues.append(f"SSID '{s['name']}' WIPS is disabled")
    return issues

def audit_vlans(vlans):
    issues = []
    if not vlans:
        issues.append("No VLANs found")
    else:
        for v in vlans:
            if not v.get("applianceIp"):
                issues.append(f"VLAN {v.get('id')} may be unsegmented")
    return issues

# --------------------- RUN AUDIT ---------------------
def run_audit(dashboard, network_id, network_name):
    folder = os.path.join("meraki", network_name.replace(" ", "_"))
    print_header(f"Fetching Configurations for {network_name}")

    vpn = safe_call(dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn, networkId=network_id)
    firewall = safe_call(dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules, networkId=network_id)
    vlans = safe_call(dashboard.appliance.getNetworkApplianceVlans, networkId=network_id)
    ssids = safe_call(dashboard.wireless.getNetworkWirelessSsids, networkId=network_id)

    # Save config
    save_json(os.path.join(folder, "config.json"), {"vpn": vpn, "firewall": firewall, "vlans": vlans, "ssids": ssids})
    print(Fore.GREEN + f"[+] Saved config.json for {network_name}")

    # Run audits
    audit_results = {
        "VPN": audit_vpn(vpn),
        "Firewall": audit_firewall(firewall.get("rules") if firewall else None),
        "VLANs": audit_vlans(vlans),
        "Wireless": audit_wireless(ssids)
    }

    # Save CSV
    all_issues = []
    for cat, issues in audit_results.items():
        for i in issues:
            all_issues.append([cat, i])
    save_csv(os.path.join(folder, "audit.csv"), all_issues)

    # Terminal summary
    print_header(f"Security Audit Summary for {network_name}")
    for cat, issues in audit_results.items():
        if issues:
            print(Fore.RED + f"[-] {cat} Issues:")
            for i in issues:
                print("   " + i)
        else:
            print(Fore.GREEN + f"[+] {cat} OK")

# --------------------- MAIN ---------------------
def main():
    dashboard = meraki.DashboardAPI(API_KEY, output_log=False)
    print(Fore.GREEN + "[+] Meraki client initialized")

    # Get organizations
    orgs = safe_call(dashboard.organizations.getOrganizations)
    if not orgs:
        print(Fore.RED + "No organizations found.")
        sys.exit(1)

    print_header("Available Organizations")
    for idx, o in enumerate(orgs, start=1):
        print(f"{idx}. {o['name']} (ID: {o['id']})")

    while True:
        try:
            choice = int(input(Fore.YELLOW + "\nSelect Organization (number): ").strip())
            if 1 <= choice <= len(orgs):
                org_id = orgs[choice-1]["id"]
                break
            else:
                print(Fore.RED + "Invalid choice")
        except ValueError:
            print(Fore.RED + "Enter a number")

    # Get networks
    nets = safe_call(dashboard.organizations.getOrganizationNetworks, organizationId=org_id)
    if not nets:
        print(Fore.RED + "No networks found for org")
        sys.exit(1)

    print_header("Available Networks")
    for idx, n in enumerate(nets, start=1):
        print(f"{idx}. {n['name']} (ID: {n['id']}, products: {', '.join(n['productTypes'])})")
    print(f"{len(nets)+1}. Dump ALL networks")

    while True:
        try:
            choice = int(input(Fore.YELLOW + "\nSelect Network (number): ").strip())
            if 1 <= choice <= len(nets):
                network_id = nets[choice-1]["id"]
                network_name = nets[choice-1]["name"]
                run_audit(dashboard, network_id, network_name)
                break
            elif choice == len(nets)+1:
                print(Fore.CYAN + "[*] Dumping all networks...")
                for n in nets:
                    run_audit(dashboard, n["id"], n["name"])
                break
            else:
                print(Fore.RED + "Invalid choice")
        except ValueError:
            print(Fore.RED + "Enter a number")

if __name__ == "__main__":
    main()
