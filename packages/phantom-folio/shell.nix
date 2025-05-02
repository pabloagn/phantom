# shell.nix - Development environment for Phantom Folio
{ pkgs ? import <nixpkgs> { config = { allowUnfree = true; }; },
  withClaude ? false }:
let
  # Custom Python with required packages
  pythonEnv = pkgs.python310.withPackages (ps: with ps; [
    pip
    setuptools
    wheel
    virtualenv
    # PDF processing libraries
    pdfminer-six
    pypdf
    pillow
    # Other useful packages for development
    ipython
    pytest
    black
    flake8
    mypy
  ]);
in
pkgs.mkShell {
  name = "phantom-folio-dev";
  buildInputs = with pkgs; [
    # Core system tools
    pythonEnv
    docker
    docker-compose
    
    # Node.js for Claude Code (included conditionally in shellHook)
    nodejs_18
    
    # Optional dependencies for Claude Code (included always as they're useful)
    ripgrep   # Enhanced file search
    gh        # GitHub CLI for PR workflows
    
    # PDF processing dependencies
    poppler_utils
    tesseract
    opencv
    leptonica
    ghostscript
    imagemagick
    python310Packages.pymupdf  # PyMuPDF/fitz
    python310Packages.pillow   # PIL/Pillow
    python310Packages.pytesseract
    
    # Additional utilities
    coreutils
    gnugrep
    gnused
    wget
    curl
    jq
    ncurses # for terminal utilities
    
    # Development tools
    git
    vim
    tmux
  ];
  
  # Environment variables
  shellHook = ''
    # Terminal colors for better UX
    export BLUE='\033[0;34m'
    export GREEN='\033[0;32m'
    export YELLOW='\033[0;33m'
    export RED='\033[0;31m'
    export NC='\033[0m' # No Color
    
    # Project root directory
    export PROJECT_ROOT=$(pwd)
    export PATH=$PROJECT_ROOT/scripts:$PATH
    
    # Create logs directory for application logs
    mkdir -p $PROJECT_ROOT/logs
    
    # Set up Python virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
      echo -e "''${BLUE}Creating Python virtual environment...''${NC}"
      python -m venv .venv
      source .venv/bin/activate
      pip install --upgrade pip setuptools wheel
    else
      source .venv/bin/activate
    fi
    
    # Install Python dependencies if requirements.txt exists
    if [ -f requirements.txt ]; then
      echo -e "''${BLUE}Installing Python dependencies...''${NC}"
      pip install -r requirements.txt
    fi
    
    # Install Claude Code if enabled via flag
    if ${builtins.toString withClaude}; then
      if ! command -v claude &> /dev/null; then
        echo -e "''${BLUE}Installing Claude Code...''${NC}"
        npm install -g @anthropic-ai/claude-code
      else
        CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
        echo -e "''${GREEN}Claude Code is already installed (version: $CLAUDE_VERSION)''${NC}"
      fi
      echo -e "''${GREEN}Claude Code support enabled''${NC}"
    fi
    
    # Make scripts executable
    if [ -f "scripts/setup.sh" ]; then
      chmod +x scripts/setup.sh
    fi
    if [ -f "scripts/cleanup.sh" ]; then
      chmod +x scripts/cleanup.sh
    fi
    
    # Make dev convenience scripts executable
    if [ -d "scripts" ]; then
      chmod +x scripts/*.sh 2>/dev/null || true
    fi
    
    # Set up auto-cleanup on shell exit
    cleanup() {
      echo -e "''${YELLOW}Nix shell is exiting. Checking for running containers...''${NC}"
      if docker compose ps -q 2>/dev/null | grep -q .; then
        echo -e "''${YELLOW}Stopping containers...''${NC}"
        ./cleanup.sh
      fi
      echo -e "''${GREEN}Environment cleaned up.''${NC}"
    }
    trap cleanup EXIT
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
      echo -e "''${RED}Warning: Docker daemon is not running.''${NC}"
      echo -e "''${YELLOW}Please start Docker before running setup.sh''${NC}"
    else
      echo -e "''${GREEN}Docker daemon is running.''${NC}"
    fi
    
    # Display welcome message
    echo -e "''${GREEN}======================================''${NC}"
    echo -e "''${GREEN}  Phantom Folio Development Environment  ''${NC}"
    echo -e "''${GREEN}======================================''${NC}"
    echo ""
    echo -e "''${BLUE}Available commands:''${NC}"
    echo -e "  ''${YELLOW}./setup.sh''${NC} - Set up infrastructure"
    echo -e "  ''${YELLOW}./cleanup.sh''${NC} - Clean up resources"
    echo -e "  ''${YELLOW}python -m phantom_folio''${NC} - Run the application"
    
    if ${builtins.toString withClaude}; then
      echo -e "  ''${YELLOW}claude''${NC} - Start Claude Code for AI coding assistance"
      echo ""
      echo -e "''${BLUE}Claude Code:''${NC}"
      echo -e "  ''${YELLOW}Authentication:''${NC} Run 'claude' and follow the OAuth process"
      echo -e "  ''${YELLOW}Usage:''${NC} Type your coding questions or commands after starting Claude"
      echo -e "  ''${YELLOW}Help:''${NC} Type '/help' after starting Claude for available commands"
      echo -e "  ''${YELLOW}Bug reporting:''${NC} Use '/bug' within Claude to report issues"
    else
      echo -e "  ''${YELLOW}./scripts/dev-with-claude.sh''${NC} - Restart shell with Claude Code support"
    fi
    
    echo ""
    echo -e "''${BLUE}Development directories:''${NC}"
    echo -e "  ''${YELLOW}./phantom_folio/''${NC} - Application source code"
    echo -e "  ''${YELLOW}./scripts/''${NC} - Utility scripts"
    echo -e "  ''${YELLOW}./data/''${NC} - Data files"
    echo -e "  ''${YELLOW}./logs/''${NC} - Log files"
    echo ""
    echo -e "''${GREEN}Environment ready!''${NC}"
  '';
}
