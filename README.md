# 🦅 NetRaptor - Advanced Wireless Penetration Testing Tool

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)
[![Ethical Hacking](https://img.shields.io/badge/usage-Ethical%20Hacking%20Only-red.svg)](#legal-disclaimer)
[![GitHub Stars](https://img.shields.io/github/stars/Lokidres/NetRaptor.svg)](https://github.com/Lokidres/NetRaptor/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Lokidres/NetRaptor.svg)](https://github.com/Lokidres/NetRaptor/network)

**NetRaptor** is a comprehensive, professional-grade wireless network security auditing framework designed for authorized penetration testing and security research. Built with precision and power, NetRaptor swoops down on wireless vulnerabilities with deadly accuracy.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              ███╗   ██╗███████╗████████╗                    ║
║                              ████╗  ██║██╔════╝╚══██╔══╝                    ║
║                              ██╔██╗ ██║█████╗     ██║                       ║
║                              ██║╚██╗██║██╔══╝     ██║                       ║
║                              ██║ ╚████║███████╗   ██║                       ║
║                              ╚═╝  ╚═══╝╚══════╝   ╚═╝                       ║
║           ██████╗  █████╗ ██████╗ ████████╗ ██████╗ ██████╗                 ║
║           ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗                ║
║           ██████╔╝███████║██████╔╝   ██║   ██║   ██║██████╔╝                ║
║           ██╔══██╗██╔══██║██╔═══╝    ██║   ██║   ██║██╔══██╗                ║
║           ██║  ██║██║  ██║██║        ██║   ╚██████╔╝██║  ██║                ║
║           ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║              Advanced Wireless Penetration Testing Framework                ║
║                         Author: Lokidres | MIT License                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 🎯 **Features**

### **🛡️ Core Capabilities**
- 🔍 **Advanced Network Discovery** - Multi-method wireless network scanning with fallback mechanisms
- 🔐 **WPA/WPA2 Security Audit** - Comprehensive encryption analysis and vulnerability assessment
- 📡 **WPS Vulnerability Assessment** - Detection and PIN brute force attacks
- 🤝 **Handshake Capture & Cracking** - WPA/WPA2 password recovery with progress tracking
- ⚡ **Deauthentication Attacks** - Client disconnection techniques with smart targeting
- 👥 **Evil Twin Detection** - Rogue access point identification and analysis
- 📱 **Bluetooth Device Discovery** - Nearby device enumeration and profiling
- 💉 **Packet Injection Testing** - Wireless adapter capability verification

### **⚡ Advanced Features**
- 🎛️ **Professional CLI Interface** - Flag-based operation system like enterprise tools
- 📊 **Real-time Progress Tracking** - Live attack monitoring with detailed metrics
- 📈 **Comprehensive Reporting** - JSON and HTML output formats with visual charts
- 🔧 **Monitor Mode Management** - Automated wireless adapter configuration with fallbacks
- 🛠️ **Error Recovery Systems** - Robust failure handling and graceful degradation
- 🎯 **Multi-target Support** - Batch operation capabilities for efficiency

## 📋 **Prerequisites**

### **Operating System**
- Linux-based operating system (Kali Linux, Ubuntu, Parrot OS, etc.)
- Root privileges (sudo access required)

### **Hardware Requirements**
- Wireless network adapter with monitor mode support
- USB Wi-Fi adapter recommended for dedicated monitoring

### **Software Dependencies**
```bash
# Core packages (automatically checked by NetRaptor)
sudo apt-get update
sudo apt-get install aircrack-ng reaver hostapd dnsmasq

# Optional packages for enhanced functionality
sudo apt-get install hcxtools bluetooth bluez-utils

# Python 3.7+ (usually pre-installed)
python3 --version
```

## 🚀 **Installation**

### **1. Clone Repository**
```bash
git clone https://github.com/Lokidres/NetRaptor.git
cd NetRaptor
```

### **2. Quick Install (Recommended)**
```bash
# Automated installation with dependency check
chmod +x install.sh
sudo ./install.sh
```

### **3. Manual Installation**
```bash
# Install dependencies manually
sudo apt-get install -y aircrack-ng reaver hostapd dnsmasq hcxtools bluetooth bluez-utils
```

### **4. Verify Installation**
```bash
# Test NetRaptor
sudo python3 netraptor.py --help
```

## 📖 **Usage Guide**

### **Basic Syntax**
```bash
sudo python3 netraptor.py [OPTIONS] <FLAGS>
```

### **🔍 Core Operations**

#### **Network Discovery & Analysis**
```bash
# Basic network scan
sudo python3 netraptor.py --scan

# Extended scan with security analysis
sudo python3 netraptor.py --scan --wpa-audit --evil-twin

# Comprehensive audit (all features)
sudo python3 netraptor.py --scan --wpa-audit --wps-test --evil-twin --bluetooth
```

#### **📡 WPS Security Testing**
```bash
# WPS vulnerability scan
sudo python3 netraptor.py --wps-test

# WPS PIN brute force attack
sudo python3 netraptor.py --wps-attack AA:BB:CC:DD:EE:FF --channel 6

# Combined WPS assessment and attack
sudo python3 netraptor.py --wps-test --wps-attack AA:BB:CC:DD:EE:FF --channel 6
```

#### **🔐 WPA/WPA2 Handshake Operations**
```bash
# Capture handshake
sudo python3 netraptor.py --handshake AA:BB:CC:DD:EE:FF --channel 6

# Crack captured handshake
sudo python3 netraptor.py --crack-handshake handshake_file.cap --wordlist rockyou.txt

# Full workflow: capture then crack
sudo python3 netraptor.py --handshake AA:BB:CC:DD:EE:FF --channel 6
sudo python3 netraptor.py --crack-handshake handshake_*.cap --wordlist /usr/share/wordlists/rockyou.txt
```

#### **⚡ Deauthentication Attacks**
```bash
# Disconnect clients from target network
sudo python3 netraptor.py --deauth AA:BB:CC:DD:EE:FF --channel 11

# Verbose deauth with detailed output
sudo python3 netraptor.py --deauth AA:BB:CC:DD:EE:FF --channel 11 --verbose
```

#### **🔧 Advanced Operations**
```bash
# Test packet injection capability
sudo python3 netraptor.py --injection-test -i wlan0

# Setup monitor mode only
sudo python3 netraptor.py --monitor-only -i wlan0

# Custom timeout and interface
sudo python3 netraptor.py --scan -i wlan1 -t 60

# Generate specific report format
sudo python3 netraptor.py --scan --output html
```

## 🎛️ **Command Reference**

### **Interface Options**
| Flag | Description | Example |
|------|-------------|---------|
| `-i, --interface` | Specify wireless interface | `-i wlan0` |
| `-t, --timeout` | Set operation timeout (seconds) | `-t 60` |

### **Core Features**
| Flag | Description | Requirements |
|------|-------------|--------------|
| `--scan` | Basic wireless network discovery | None |
| `--wpa-audit` | WPA/WPA2 security analysis | Requires `--scan` first |
| `--wps-test` | WPS vulnerability scanning | Monitor mode, reaver |
| `--wps-attack <BSSID>` | WPS PIN brute force | Monitor mode, reaver, `--channel` |
| `--deauth <BSSID>` | Deauthentication attack | Monitor mode, `--channel` |
| `--handshake <BSSID>` | Capture WPA handshake | Monitor mode, `--channel` |
| `--crack-handshake <file>` | Crack handshake file | aircrack-ng, `--wordlist` |
| `--evil-twin` | Detect rogue access points | Requires `--scan` first |
| `--bluetooth` | Bluetooth device discovery | bluetooth, bluez-utils |
| `--injection-test` | Test packet injection | Monitor mode |

### **Advanced Options**
| Flag | Description | Default |
|------|-------------|---------|
| `--channel <num>` | Target channel for attacks | Required for attacks |
| `--wordlist <file>` | Custom wordlist path | Auto-detect common lists |
| `--output <format>` | Report format (json/html/both) | both |
| `--monitor-only` | Only enable monitor mode | - |
| `--verbose` | Enable debug output | - |

## 📊 **Output & Reporting**

### **Console Output**
NetRaptor provides real-time feedback with color-coded status messages:
- 🔵 **Blue**: Informational messages and progress updates
- 🟢 **Green**: Successful operations and achievements
- 🟡 **Yellow**: Warnings and non-critical issues
- 🔴 **Red**: Errors and critical failures

### **Generated Reports**
- **JSON Report**: Machine-readable data format for automation
- **HTML Report**: Visual presentation with charts and graphs
- **Attack Results**: Separate files for successful attacks and captures

### **File Naming Convention**
```
netraptor_audit_YYYYMMDD_HHMMSS.json
netraptor_audit_YYYYMMDD_HHMMSS.html
handshake_<BSSID>_YYYYMMDD_HHMMSS.cap
wps_attack_results_YYYYMMDD_HHMMSS.json
cracked_password_YYYYMMDD_HHMMSS.json
```

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **Monitor Mode Failures**
```bash
# Issue: Monitor mode setup fails
# Solution: Try different methods
sudo airmon-ng check kill
sudo systemctl stop NetworkManager
sudo python3 netraptor.py --monitor-only -i wlan0
```

#### **No Networks Found**
```bash
# Issue: Scan returns no results
# Solution: Check interface and increase timeout
sudo iwconfig  # Verify interface status
sudo python3 netraptor.py --scan -t 60 --verbose
```

#### **Permission Errors**
```bash
# Issue: Permission denied errors
# Solution: Ensure proper privileges
sudo su  # Switch to root user
sudo python3 netraptor.py --scan
```

#### **Missing Dependencies**
```bash
# Issue: Required tools not found
# Solution: Install missing packages
sudo apt-get update
sudo apt-get install aircrack-ng reaver hostapd dnsmasq
```

### **Performance Optimization**

#### **Improve Scan Results**
- Use dedicated USB Wi-Fi adapter for better range
- Position adapter for optimal signal reception
- Increase scan timeout for comprehensive results
- Use monitor mode when possible for full feature access

#### **Speed Up Attacks**
- Use targeted wordlists for faster handshake cracking
- Optimize WPS attack timing based on AP behavior
- Run attacks during high client activity periods
- Use multiple attack vectors simultaneously when appropriate

## 🎭 **NetRaptor vs Other Tools**

| Feature | NetRaptor | Aircrack-ng | Reaver | Wifite |
|---------|-----------|-------------|--------|--------|
| **Unified Interface** | ✅ | ❌ | ❌ | ✅ |
| **Real-time Progress** | ✅ | ❌ | ✅ | ❌ |
| **Multiple Attacks** | ✅ | ❌ | ❌ | ✅ |
| **Evil Twin Detection** | ✅ | ❌ | ❌ | ❌ |
| **Professional Reports** | ✅ | ❌ | ❌ | ❌ |
| **Bluetooth Integration** | ✅ | ❌ | ❌ | ❌ |
| **Auto-Recovery** | ✅ | ❌ | ❌ | ✅ |

## 🔒 **Legal Disclaimer**

### **⚠️ IMPORTANT LEGAL NOTICE**

NetRaptor is designed **EXCLUSIVELY** for:
- ✅ **Authorized penetration testing**
- ✅ **Security research on owned networks**
- ✅ **Educational purposes in controlled environments**
- ✅ **Professional security assessments with written permission**

### **🚫 PROHIBITED USES**
- ❌ **Unauthorized network access**
- ❌ **Attacking networks without explicit permission**
- ❌ **Commercial use without proper authorization**
- ❌ **Any illegal or malicious activities**

### **📜 Legal Responsibility**
Users are **solely responsible** for:
- Obtaining proper authorization before testing
- Complying with local, state, and federal laws
- Using the tool ethically and responsibly
- Any consequences of misuse

**The developers assume NO responsibility for misuse of this tool.**

## 🤝 **Contributing**

We welcome contributions from the security community! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### **How to Contribute**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### **Areas for Contribution**
- New attack vectors and techniques
- Performance optimizations
- Documentation improvements
- Bug fixes and stability improvements
- Translation efforts

## 📚 **Educational Resources**

### **Learning Materials**
- [Wireless Security Fundamentals](https://www.sans.org/white-papers/1137/)
- [Ethical Hacking Methodology](https://www.ec-council.org/ethical-hacking/)
- [Penetration Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### **Recommended Courses**
- Certified Ethical Hacker (CEH)
- Offensive Security Certified Professional (OSCP)
- SANS Wireless Security Courses

## 🐛 **Bug Reports & Feature Requests**

### **Reporting Issues**
- Use [GitHub Issues](https://github.com/Lokidres/NetRaptor/issues) for bug reports
- Provide detailed reproduction steps
- Include system information and error logs
- Check existing issues before creating new ones

### **Feature Requests**
- Use [GitHub Discussions](https://github.com/Lokidres/NetRaptor/discussions) for feature ideas
- Describe the use case and expected behavior
- Consider contributing the feature yourself!

## 📞 **Support**

### **Getting Help**
- 📖 **Documentation**: Check this README first
- 🐛 **Bug Reports**: Use GitHub Issues
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Contact**: [Create an issue for support requests]

### **Community**
- Join our security community discussions
- Share your experiences and learn from others
- Contribute to the project development

## 🏆 **Acknowledgments**

### **Special Thanks**
- **Aircrack-ng Suite** - Core wireless security tools foundation
- **Reaver Project** - WPS attack implementation inspiration
- **Security Community** - Continuous feedback and improvements
- **Open Source Contributors** - Making security tools accessible to all

### **Built With**
- Python 3.7+ - Core programming language
- Aircrack-ng - Wireless security suite
- Reaver - WPS attack framework
- Linux - Primary operating system platform

## 📈 **Project Statistics**

![GitHub last commit](https://img.shields.io/github/last-commit/Lokidres/NetRaptor)
![GitHub issues](https://img.shields.io/github/issues/Lokidres/NetRaptor)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Lokidres/NetRaptor)
![GitHub contributors](https://img.shields.io/github/contributors/Lokidres/NetRaptor)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2024 Lokidres
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 🌟 **Star History**

[![Star History Chart](https://api.star-history.com/svg?repos=Lokidres/NetRaptor&type=Date)](https://star-history.com/#Lokidres/NetRaptor&Date)

---

**⭐ Star this repository if you find NetRaptor useful!**

**🔄 Fork and contribute to help improve wireless security testing!**

**🦅 Hunt vulnerabilities with precision - NetRaptor never misses its target!**

*Made with ❤️ by [Lokidres](https://github.com/Lokidres) | Last updated: December 2024*