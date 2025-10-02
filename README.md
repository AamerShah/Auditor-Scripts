# Auditor-Scripts
# ![Audit Logo](https://upload.wikimedia.org/wikipedia/commons/1/19/Shield_icon.png) Network & Security Auditor Suite

[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/release/yourusername/network-auditor-suite.svg)](https://github.com/yourusername/network-auditor-suite/releases)

---

## 🚀 Overview

This repository contains **multiple network and security auditing scripts**.  
Each script connects to its target system, fetches configuration or state information, and performs security audits based on best practices.

Currently included:

1. **Meraki Auditor** (`meraki_conf.py`) – fetches Meraki network configs and performs CIS-like audits.  
2. *(Future auditors for other platforms can be added here)*

**Outputs (per auditor):**  
- JSON configuration dump  
- CSV security audit report  
- Colored terminal summaries of findings  

---

## 🎨 Features

- Interactive selection of organizations/networks (Meraki)  
- Option to **dump all networks** sequentially (Meraki)  
- **Colored terminal UI** for clarity (info, warnings, errors)  
- Full **read-only audit** (safe for production)  
- Automatic **dependency checks and installations** (`meraki`, `colorama`)  
- Optional **virtual environment creation** (`.venv`) per auditor  
- Modular code structure: easy to extend with new auditing scripts  

---

## ⚡ Requirements

- Python 3.13+  
- Dependencies (each auditor may have its own):
  ```bash
  pip install meraki colorama
