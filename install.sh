#!/bin/bash

# NetRaptor - Advanced Wireless Penetration Testing Tool
# Installation Script for Linux Systems
# Author: Lokidres
# GitHub: https://github.com/Lokidres/NetRaptor
# Requires: sudo privileges

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                 NETRAPTOR                                    ║"
echo "║                     Advanced Wireless Penetration Testing Tool              ║"
echo "║                              Installation Script                             ║"
echo "║                         Author: Lokidres | MIT License                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root. This is fine for installation."
else
    print_status "Checking sudo privileges..."
    if ! sudo -n true 2>/dev/null; then
        print_error "This script requires sudo privileges. Please run with sudo or as root."
        exit 1
    fi
fi

# Detect Linux distribution
print_status "Detecting Linux distribution..."

if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    VERSION=$VERSION_ID
else
    print_error "Cannot detect Linux distribution. Unsupported system."
    exit 1
fi

print_success "Detected: $PRETTY_NAME"

# Check Python version
print_status "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
        print_success "Python $PYTHON_VERSION detected (compatible)"
    else
        print_error "Python 3.7+ required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.7+"
    exit 1
fi

# Update package lists
print_status "Updating package lists..."
case $DISTRO in
    ubuntu|debian|kali|parrot)
        sudo apt-get update -qq
        ;;
    fedora|rhel|centos)
        sudo dnf update -q -y
        ;;
    arch|manjaro)
        sudo pacman -Sy --noconfirm
        ;;
    *)
        print_warning "Unknown distribution. Attempting with apt-get..."
        sudo apt-get update -qq || {
            print_error "Package update failed. Please install dependencies manually."
            exit 1
        }
        ;;
esac

print_success "Package lists updated"

# Install core dependencies
print_status "Installing core wireless security tools..."

install_packages() {
    case $DISTRO in
        ubuntu|debian|kali|parrot)
            print_status "Installing packages with apt-get..."
            sudo apt-get install -y \
                aircrack-ng \
                reaver \
                hostapd \
                dnsmasq \
                bluetooth \
                bluez-utils \
                wireless-tools \
                net-tools \
                iw \
                rfkill
            ;;
        fedora|rhel|centos)
            print_status "Installing packages with dnf..."
            sudo dnf install -y \
                aircrack-ng \
                reaver \
                hostapd \
                dnsmasq \
                bluez-tools \
                wireless-tools \
                net-tools \
                iw \
                rfkill
            ;;
        arch|manjaro)
            print_status "Installing packages with pacman..."
            sudo pacman -S --noconfirm \
                aircrack-ng \
                reaver \
                hostapd \
                dnsmasq \
                bluez-utils \
                wireless_tools \
                net-tools \
                iw \
                rfkill
            ;;
        *)
            print_error "Unsupported distribution for automatic installation."
            print_status "Please install the following packages manually:"
            echo "  - aircrack-ng"
            echo "  - reaver" 
            echo "  - hostapd"
            echo "  - dnsmasq"
            echo "  - bluetooth tools"
            return 1
            ;;
    esac
}

# Install packages
if install_packages; then
    print_success "Core packages installed successfully"
else
    print_error "Failed to install some packages"
    exit 1
fi

# Install optional packages
print_status "Installing optional packages..."

install_optional() {
    case $DISTRO in
        ubuntu|debian|kali|parrot)
            # Try to install hcxtools (may not be available in all repos)
            if apt-cache search hcxtools | grep -q hcxtools; then
                sudo apt-get install -y hcxtools || print_warning "hcxtools installation failed (optional)"
            else
                print_warning "hcxtools not available in repositories (optional)"
            fi
            
            # Install additional useful tools
            sudo apt-get install -y \
                macchanger \
                ettercap-text-only \
                nmap \
                tshark 2>/dev/null || print_warning "Some optional tools failed to install"
            ;;
        fedora|rhel|centos)
            sudo dnf install -y \
                macchanger \
                ettercap \
                nmap \
                wireshark-cli 2>/dev/null || print_warning "Some optional tools failed to install"
            ;;
        arch|manjaro)
            sudo pacman -S --noconfirm \
                macchanger \
                ettercap \
                nmap \
                wireshark-cli 2>/dev/null || print_warning "Some optional tools failed to install"
            ;;
    esac
}

install_optional

# Verify installations
print_status "Verifying installations..."

check_command() {
    if command -v "$1" &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is NOT installed"
        return 1
    fi
}

# Check core tools
MISSING_TOOLS=0

print_status "Checking core tools..."
for tool in airmon-ng airodump-ng aireplay-ng aircrack-ng reaver wash hostapd dnsmasq; do
    if ! check_command "$tool"; then
        ((MISSING_TOOLS++))
    fi
done

print_status "Checking system tools..."
for tool in iwconfig iwlist iw rfkill; do
    if ! check_command "$tool"; then
        ((MISSING_TOOLS++))
    fi
done

# Check bluetooth tools
print_status "Checking bluetooth tools..."
for tool in bluetoothctl hciconfig hcitool; do
    if ! check_command "$tool"; then
        print_warning "$tool not found (bluetooth features may not work)"
    fi
done

# Create desktop shortcut (optional)
create_shortcut() {
    read -p "Create desktop shortcut? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        DESKTOP_FILE="$HOME/Desktop/netraptor.desktop"
        CURRENT_DIR=$(pwd)
        
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=NetRaptor
Comment=Advanced wireless penetration testing framework
Exec=sudo python3 $CURRENT_DIR/netraptor.py
Icon=network-wireless
Terminal=true
Categories=Security;Network;
EOF
        
        chmod +x "$DESKTOP_FILE"
        print_success "Desktop shortcut created"
    fi
}

# Set up permissions for wireless operations
print_status "Setting up wireless permissions..."
sudo usermod -a -G netdev "$USER" 2>/dev/null || print_warning "Could not add user to netdev group"

# Final status
echo
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                              INSTALLATION COMPLETE                          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"

if [ $MISSING_TOOLS -eq 0 ]; then
    print_success "All core tools installed successfully!"
    echo
    print_status "You can now run NetRaptor with:"
    echo -e "  ${GREEN}sudo python3 netraptor.py --help${NC}"
    echo
    print_status "Example usage:"
    echo -e "  ${GREEN}sudo python3 netraptor.py --scan${NC}"
    echo -e "  ${GREEN}sudo python3 netraptor.py --scan --wpa-audit --wps-test${NC}"
    
    # Ask about desktop shortcut
    echo
    create_shortcut
    
else
    print_warning "$MISSING_TOOLS core tools are missing. Please install them manually."
    print_status "Manual installation commands:"
    echo "  Ubuntu/Debian: sudo apt-get install aircrack-ng reaver hostapd dnsmasq"
    echo "  Fedora/RHEL:   sudo dnf install aircrack-ng reaver hostapd dnsmasq"
    echo "  Arch Linux:    sudo pacman -S aircrack-ng reaver hostapd dnsmasq"
fi

echo
print_status "Installation script completed!"
print_warning "Remember: This tool is for authorized penetration testing only!"
print_warning "Always obtain proper permission before testing any networks!"

# Check for wireless interfaces
echo
print_status "Available wireless interfaces:"
if command -v iwconfig &> /dev/null; then
    iwconfig 2>/dev/null | grep -E "^[a-z]" | cut -d' ' -f1 | while read iface; do
        if iwconfig "$iface" 2>/dev/null | grep -q "IEEE 802.11"; then
            echo -e "  ${GREEN}✓${NC} $iface"
        fi
    done
else
    print_warning "iwconfig not available - cannot check wireless interfaces"
fi

echo
print_success "NetRaptor installation completed! 🦅"
print_warning "Remember: NetRaptor is for authorized penetration testing only!"
print_warning "Always obtain proper permission before testing any networks!"
print_status "GitHub: https://github.com/Lokidres/NetRaptor"