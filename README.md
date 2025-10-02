# Network & Security Auditor Suite

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/github-AamerShah%2FAuditor--Scripts-181717?logo=github)](https://github.com/AamerShah/Auditor-Scripts)

---

## 🚀 Overview

A comprehensive suite of **network and security auditing scripts** designed to connect to various infrastructure platforms, fetch configuration data, and perform automated security audits based on industry best practices.

### Currently Supported Platforms

1. **Meraki Auditor** (`meraki_conf.py`) – Fetches Cisco Meraki network configurations and performs CIS-aligned security audits

*Additional platform auditors coming soon...*

### Output Per Auditor

- 📄 **JSON configuration dump** – Complete device/network configuration
- 📊 **CSV security audit report** – Detailed findings with severity levels
- 🎨 **Color-coded terminal summary** – Real-time audit progress and results

---

## 🎨 Features

- ✅ **Interactive CLI** – Select organizations and networks with ease
- ⚡ **Bulk operations** – Audit all networks in a single run (Meraki)
- 🎨 **Enhanced UX** – Color-coded output for info, warnings, and errors
- 🔒 **Read-only mode** – 100% safe for production environments
- 🔧 **Auto-dependency management** – Automatic installation of required packages
- 📦 **Virtual environment support** – Optional `.venv` creation per auditor
- 🧩 **Modular architecture** – Easily extensible for new platforms

---

## ⚡ Requirements

### System Requirements
- **Python 3.13+**
- Linux/macOS recommended (Windows may require adjustments)

### Dependencies

```bash
pip install meraki colorama
```

### API Credentials

Each auditor requires platform-specific credentials:

- **Meraki**: Dashboard API Key (add to line 42 of `meraki_conf.py`)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AamerShah/Auditor-Scripts.git
cd Auditor-Scripts
```

### 2. (Optional) Make Scripts Executable

```bash
chmod +x *.py
```

### 3. Set Up Python Environment

**Option A: Auto-setup** (recommended)
- Scripts automatically create `.venv` and install dependencies on first run

**Option B: Manual setup**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure API Credentials

Edit the auditor script and add your credentials:

```python
# meraki_conf.py - Line 40
API_KEY = "your_meraki_api_key_here"
```

---

## 🖥 Usage

### Running an Auditor

```bash
python3 meraki_conf.py
```

### Meraki Auditor Workflow

1. 📋 Script displays available organizations
2. 🏢 Select target organization
3. 🌐 Choose specific network **OR** select "Dump All Networks"
4. ⚙️ Audit runs and generates reports
5. 💾 Results saved to `meraki/<network_name>/`

### Output Structure

```
meraki/
└── NetworkName/
    ├── config.json    # Complete configuration dump
    └── audit.csv      # Security findings report
```

---

## 🎯 Security Checks

### Meraki Auditor Checks

| Category | Checks Performed |
|----------|------------------|
| **VPN** | Topology validation, weak PSK detection |
| **Firewall** | Overly permissive rules, any-any policies |
| **VLANs** | Network segmentation issues |
| **Wireless** | Open networks, weak encryption (WEP/WPA), WIPS status |
| **Traffic Shaping** | Bandwidth limits, QoS priorities |

*Additional platform auditors will include their own security check matrices*

---

## 🔧 Configuration

### API Key Management

Each auditor specifies where credentials should be configured:

```python
# Current: Hardcoded in script (line 40)
API_KEY = "your_key_here"

# Future: Environment variables support planned
# export MERAKI_API_KEY="your_key_here"
```

### Customizing Audits

Audit rules can be modified in each script's `perform_audit()` function.

---

## 🛡 Important Notes

- ✅ **All scripts are read-only** – No configuration changes are made
- 🔄 **First run setup** – Scripts may auto-install dependencies
- 💾 **Local filesystem recommended** – For VM shared folders, use local paths for `.venv`
- 🪟 **Windows compatibility** – May require path and command adjustments

---

## 📖 References

- [Cisco Meraki API Documentation](https://developer.cisco.com/meraki/)
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [Colorama Documentation](https://pypi.org/project/colorama/)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💡 Credits

**Developed by [Aamer Shah](https://github.com/AamerShah)**

Special thanks to:
- Python community for `venv` and library ecosystem
- Cisco DevNet for comprehensive API documentation
- Open-source contributors

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions, issues, or feature requests, please open an issue on [GitHub](https://github.com/AamerShah/Auditor-Scripts/issues).

---

<div align="center">
  
**⭐ Star this repo if you find it useful!**

Made with ❤️ by [Aamer Shah](https://github.com/AamerShah)

</div>
