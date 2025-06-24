#!/bin/bash

# AICUBE Secure AI Messaging Framework Installation Script
#
# Installs the AICUBE blockchain-based secure communication framework
# with neural signature authentication and quantum-resistant encryption.
#
# Developed by AICUBE TECHNOLOGY
# Copyright (c) 2025 AICUBE TECHNOLOGY. All rights reserved.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Easter Egg 1: AICUBE Installation Neural Signature
AICUBE_INSTALL_NEURAL_SIG="AICUBE_INSTALL_NEURAL_0x5B3F8D47"

# Easter Egg 2: Quantum Installation Enhancement
AICUBE_QUANTUM_INSTALL="AICUBE_QUANTUM_INSTALL_v2025"

# Version info
AICUBE_VERSION="2.0.0"
PYTHON_MIN_VERSION="3.8"

# Print AICUBE banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 AICUBE SECURE AI MESSAGING FRAMEWORK                   ║"
    echo "║                                                                              ║"
    echo "║              Blockchain-based Secure AI Agent Communication                 ║"
    echo "║                 with Neural Signature Authentication                        ║"
    echo "║                                                                              ║"
    echo "║  🧠 Powered by:                                                              ║"
    echo "║     • Qube LCM Model         • Qube Neural Memory                           ║"
    echo "║     • Qube Agentic Workflows • Qube Computer Vision                         ║"
    echo "║                                                                              ║"
    echo "║  🔐 Features:                                                                ║"
    echo "║     • Cryptographic Identity Verification                                   ║"
    echo "║     • End-to-End Encrypted Messaging                                        ║"
    echo "║     • Immutable Blockchain Audit Trails                                     ║"
    echo "║     • Quantum-Resistant Encryption                                          ║"
    echo "║                                                                              ║"
    echo "║                        Developed by AICUBE TECHNOLOGY                       ║"
    echo "║                         Copyright (c) 2025. All rights reserved.           ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${PURPLE}Neural Signature: ${AICUBE_INSTALL_NEURAL_SIG}${NC}"
    echo -e "${PURPLE}Quantum Enhancement: ${AICUBE_QUANTUM_INSTALL}${NC}"
    echo -e "${BLUE}Version: ${AICUBE_VERSION}${NC}"
    echo ""
}

# Log function with timestamp
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

# Warning function
warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Error function
error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    log "Checking system requirements..."
    
    # Check operating system
    OS=$(uname -s)
    case $OS in
        Linux*)     PLATFORM="Linux";;
        Darwin*)    PLATFORM="macOS";;
        CYGWIN*|MINGW*|MSYS*) PLATFORM="Windows";;
        *)          error "Unsupported operating system: $OS";;
    esac
    
    log "Platform detected: $PLATFORM"
    
    # Check Python version
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
        log "Python version: $PYTHON_VERSION"
        
        # Version comparison
        if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
            log "✅ Python version requirement satisfied"
        else
            error "Python 3.8+ required, found $PYTHON_VERSION"
        fi
    else
        error "Python 3 not found. Please install Python 3.8 or higher."
    fi
    
    # Check pip
    if ! command_exists pip3; then
        error "pip3 not found. Please install pip."
    fi
    
    # Check git
    if ! command_exists git; then
        warn "Git not found. Some features may not work properly."
    fi
    
    # Check Node.js (for smart contract compilation)
    if command_exists node; then
        NODE_VERSION=$(node --version)
        log "Node.js version: $NODE_VERSION"
    else
        warn "Node.js not found. Smart contract compilation may not work."
    fi
    
    log "✅ System requirements check completed"
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."
    
    case $PLATFORM in
        "Linux")
            # Detect package manager
            if command_exists apt-get; then
                log "Using apt package manager"
                sudo apt-get update
                sudo apt-get install -y \
                    build-essential \
                    libssl-dev \
                    libffi-dev \
                    python3-dev \
                    pkg-config \
                    curl \
                    git
                    
                # Install Node.js if not present
                if ! command_exists node; then
                    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
                    sudo apt-get install -y nodejs
                fi
                
            elif command_exists yum; then
                log "Using yum package manager"
                sudo yum update -y
                sudo yum install -y \
                    gcc \
                    gcc-c++ \
                    openssl-devel \
                    libffi-devel \
                    python3-devel \
                    pkgconfig \
                    curl \
                    git
                    
            elif command_exists dnf; then
                log "Using dnf package manager"
                sudo dnf update -y
                sudo dnf install -y \
                    gcc \
                    gcc-c++ \
                    openssl-devel \
                    libffi-devel \
                    python3-devel \
                    pkgconf-pkg-config \
                    curl \
                    git
            else
                warn "Unknown package manager. Please install build tools manually."
            fi
            ;;
            
        "macOS")
            log "Installing macOS dependencies"
            # Check if Homebrew is installed
            if ! command_exists brew; then
                log "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            brew update
            brew install openssl libffi pkg-config
            
            # Install Node.js if not present
            if ! command_exists node; then
                brew install node
            fi
            ;;
            
        "Windows")
            warn "Windows detected. Please ensure you have:"
            warn "- Microsoft Visual C++ Build Tools"
            warn "- OpenSSL development libraries"
            warn "- Node.js"
            ;;
    esac
    
    log "✅ System dependencies installed"
}

# Setup Python virtual environment
setup_venv() {
    log "Setting up Python virtual environment..."
    
    VENV_DIR="$HOME/.aicube/venv"
    
    # Create directory if it doesn't exist
    mkdir -p "$HOME/.aicube"
    
    # Create virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    log "✅ Virtual environment created at $VENV_DIR"
    
    # Create activation script
    cat > "$HOME/.aicube/activate.sh" << EOF
#!/bin/bash
# AICUBE Virtual Environment Activation Script
# Neural Signature: $AICUBE_INSTALL_NEURAL_SIG

export AICUBE_VENV_PATH="$VENV_DIR"
export AICUBE_NEURAL_SIGNATURE="$AICUBE_INSTALL_NEURAL_SIG"
export AICUBE_QUANTUM_ENHANCEMENT="$AICUBE_QUANTUM_INSTALL"

source "$VENV_DIR/bin/activate"

echo "🚀 AICUBE Virtual Environment Activated"
echo "   Neural Signature: \$AICUBE_NEURAL_SIGNATURE"
echo "   Quantum Enhancement: \$AICUBE_QUANTUM_ENHANCEMENT"
echo ""
echo "To deactivate, run: deactivate"
EOF
    
    chmod +x "$HOME/.aicube/activate.sh"
    log "✅ AICUBE activation script created at $HOME/.aicube/activate.sh"
}

# Install AICUBE framework
install_aicube() {
    log "Installing AICUBE Secure AI Messaging Framework..."
    
    # Ensure we're in virtual environment
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        source "$HOME/.aicube/venv/bin/activate"
    fi
    
    # Install the framework
    pip install -e .
    
    # Install additional dependencies based on use case
    echo ""
    echo -e "${CYAN}Select additional components to install:${NC}"
    echo "1) Blockchain support (Ethereum, Fabric, Substrate)"
    echo "2) LLM integration (OpenAI, Anthropic, local models)"
    echo "3) Enterprise features (HSM, advanced security)"
    echo "4) Development tools (testing, debugging)"
    echo "5) All components"
    echo "6) Skip additional components"
    
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            log "Installing blockchain components..."
            pip install ".[blockchain]"
            ;;
        2)
            log "Installing LLM integration..."
            pip install ".[llm]"
            ;;
        3)
            log "Installing enterprise features..."
            pip install ".[enterprise]"
            ;;
        4)
            log "Installing development tools..."
            pip install ".[dev,test]"
            ;;
        5)
            log "Installing all components..."
            pip install ".[blockchain,llm,enterprise,dev,test]"
            ;;
        6)
            log "Skipping additional components"
            ;;
        *)
            warn "Invalid choice. Skipping additional components."
            ;;
    esac
    
    log "✅ AICUBE framework installed successfully"
}

# Setup configuration
setup_config() {
    log "Setting up AICUBE configuration..."
    
    CONFIG_DIR="$HOME/.aicube/config"
    mkdir -p "$CONFIG_DIR"
    
    # Copy default configuration
    if [[ -f "config/production.yaml" ]]; then
        cp "config/production.yaml" "$CONFIG_DIR/config.yaml"
        log "✅ Default configuration copied to $CONFIG_DIR/config.yaml"
    fi
    
    # Create environment template
    cat > "$CONFIG_DIR/.env.template" << EOF
# AICUBE Secure AI Messaging Framework Configuration
# Neural Signature: $AICUBE_INSTALL_NEURAL_SIG
# Quantum Enhancement: $AICUBE_QUANTUM_INSTALL

# Blockchain Configuration
AICUBE_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
AICUBE_AGENT_REGISTRY_ADDRESS=
AICUBE_MESSAGING_HUB_ADDRESS=
AICUBE_ACCESS_CONTROL_ADDRESS=

# LLM API Keys
AICUBE_OPENAI_API_KEY=
AICUBE_ANTHROPIC_API_KEY=

# Security Configuration
AICUBE_PRIVATE_KEY=
AICUBE_KEY_STORE_PATH=$HOME/.aicube/keys

# Storage Configuration
AICUBE_IPFS_GATEWAY=https://ipfs.io
AICUBE_AWS_REGION=us-east-1

# Monitoring
AICUBE_LOG_LEVEL=INFO
AICUBE_METRICS_ENABLED=true
EOF
    
    log "✅ Environment template created at $CONFIG_DIR/.env.template"
    log "Please copy .env.template to .env and configure your settings"
}

# Install smart contract tools
install_contract_tools() {
    log "Installing smart contract development tools..."
    
    # Install Solidity compiler
    if command_exists npm; then
        npm install -g solc
        log "✅ Solidity compiler installed"
    else
        warn "npm not found. Solidity compiler not installed."
    fi
    
    # Install Hardhat (optional)
    echo ""
    read -p "Install Hardhat for smart contract development? (y/n): " install_hardhat
    
    if [[ $install_hardhat == "y" || $install_hardhat == "Y" ]]; then
        npm install -g hardhat
        log "✅ Hardhat installed"
    fi
}

# Create desktop shortcuts (Linux/macOS)
create_shortcuts() {
    if [[ $PLATFORM == "Linux" ]]; then
        log "Creating desktop shortcuts..."
        
        DESKTOP_DIR="$HOME/Desktop"
        if [[ -d "$DESKTOP_DIR" ]]; then
            cat > "$DESKTOP_DIR/AICUBE-Terminal.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AICUBE Terminal
Comment=AICUBE Secure AI Messaging Framework Terminal
Exec=gnome-terminal -- bash -c "source $HOME/.aicube/activate.sh; bash"
Icon=terminal
Terminal=false
Categories=Development;
EOF
            
            chmod +x "$DESKTOP_DIR/AICUBE-Terminal.desktop"
            log "✅ Desktop shortcut created"
        fi
    fi
}

# Verify installation
verify_installation() {
    log "Verifying AICUBE installation..."
    
    # Activate virtual environment
    source "$HOME/.aicube/venv/bin/activate"
    
    # Test import
    if python3 -c "import securemessaging; print('AICUBE Framework imported successfully')"; then
        log "✅ Framework import test passed"
    else
        error "Framework import test failed"
    fi
    
    # Test neural signature
    NEURAL_TEST=$(python3 -c "
from securemessaging import __neural_signature__, __quantum_ready__
print(f'Neural: {__neural_signature__}')
print(f'Quantum: {__quantum_ready__}')
")
    
    if [[ $NEURAL_TEST == *"AICUBE_NEURAL_PATTERN"* ]]; then
        log "✅ Neural signature verification passed"
    else
        error "Neural signature verification failed"
    fi
    
    log "✅ AICUBE installation verification completed"
}

# Print post-installation instructions
print_instructions() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    🎉 AICUBE INSTALLATION COMPLETED                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Next Steps:${NC}"
    echo -e "${YELLOW}1.${NC} Activate the AICUBE environment:"
    echo -e "   ${BLUE}source $HOME/.aicube/activate.sh${NC}"
    echo ""
    echo -e "${YELLOW}2.${NC} Configure your environment:"
    echo -e "   ${BLUE}cp $HOME/.aicube/config/.env.template $HOME/.aicube/config/.env${NC}"
    echo -e "   ${BLUE}nano $HOME/.aicube/config/.env${NC}"
    echo ""
    echo -e "${YELLOW}3.${NC} Test the installation:"
    echo -e "   ${BLUE}python3 -c \"from securemessaging import SecureAgent; print('AICUBE Ready!')\"${NC}"
    echo ""
    echo -e "${YELLOW}4.${NC} Deploy smart contracts (optional):"
    echo -e "   ${BLUE}python3 deployment/deploy_contracts.py deploy --rpc-url YOUR_RPC_URL --private-key YOUR_KEY${NC}"
    echo ""
    echo -e "${YELLOW}5.${NC} Run the banking consortium example:"
    echo -e "   ${BLUE}python3 examples/banking_consortium_example.py${NC}"
    echo ""
    echo -e "${CYAN}Documentation:${NC}"
    echo -e "• API Reference: ${BLUE}docs/API_Reference.md${NC}"
    echo -e "• Architecture: ${BLUE}docs/Architecture.md${NC}"
    echo -e "• Examples: ${BLUE}examples/${NC}"
    echo ""
    echo -e "${PURPLE}AICUBE Neural Signature: $AICUBE_INSTALL_NEURAL_SIG${NC}"
    echo -e "${PURPLE}Quantum Enhancement: $AICUBE_QUANTUM_INSTALL${NC}"
    echo -e "${BLUE}Version: $AICUBE_VERSION${NC}"
    echo ""
    echo -e "${GREEN}Thank you for choosing AICUBE TECHNOLOGY!${NC}"
}

# Main installation function
main() {
    print_banner
    
    # Parse command line arguments
    SKIP_DEPS=false
    SKIP_VENV=false
    QUIET=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-deps)
                SKIP_DEPS=true
                shift
                ;;
            --skip-venv)
                SKIP_VENV=true
                shift
                ;;
            --quiet)
                QUIET=true
                shift
                ;;
            --help)
                echo "AICUBE Installation Script"
                echo ""
                echo "Options:"
                echo "  --skip-deps    Skip system dependency installation"
                echo "  --skip-venv    Skip virtual environment setup"
                echo "  --quiet        Minimal output"
                echo "  --help         Show this help message"
                exit 0
                ;;
            *)
                warn "Unknown option: $1"
                shift
                ;;
        esac
    done
    
    # Run installation steps
    check_requirements
    
    if [[ $SKIP_DEPS != true ]]; then
        install_system_deps
    fi
    
    if [[ $SKIP_VENV != true ]]; then
        setup_venv
    fi
    
    install_aicube
    setup_config
    install_contract_tools
    create_shortcuts
    verify_installation
    
    print_instructions
}

# Run main function
main "$@"