#!/usr/bin/env bash
# cleanup.sh - Cleanup script for Phantom Folio

# Strict mode
set -euo pipefail

# Constants and styles
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Spinner animation
spinner() {
  local pid=$1
  local delay=0.1
  local spinstr='|/-\'
  
  # Save cursor position
  tput sc
  
  while ps a | awk '{print $1}' | grep -q "$pid"; do
    local temp=${spinstr#?}
    printf " [%c]  " "$spinstr"
    local spinstr=$temp${spinstr%"$temp"}
    # Return to saved cursor position and clear line
    tput rc
    tput el
    sleep $delay
  done
  
  # Clear spinner
  printf "    \b\b\b\b"
  wait $pid
  return $?
}

# Utility to print section headers
print_section() {
  echo -e "\n${BOLD}${BLUE}=== $1 ===${NC}\n"
}

# Utility to print status updates
print_status() {
  echo -e "${YELLOW}$1${NC}"
}

# Utility to print success messages
print_success() {
  echo -e "${GREEN}✓ $1${NC}"
}

# Utility to print error messages
print_error() {
  echo -e "${RED}✗ $1${NC}"
}

# Function to confirm action
confirm() {
  local prompt="$1"
  local default="$2"
  
  while true; do
    if [ "$default" = "Y" ]; then
      echo -ne "${YELLOW}${prompt} [Y/n]${NC} "
      read -r yn
      [ -z "$yn" ] && yn="Y"
    else
      echo -ne "${YELLOW}${prompt} [y/N]${NC} "
      read -r yn
      [ -z "$yn" ] && yn="N"
    fi
    
    case $yn in
      [Yy]* ) return 0;;
      [Nn]* ) return 1;;
      * ) echo "Please answer yes or no.";;
    esac
  done
}

# Main cleanup function
main() {
  print_section "Phantom Folio Cleanup"
  
  # Check if Docker is running
  if ! docker info &>/dev/null; then
    print_error "Docker daemon is not running"
    echo -e "${YELLOW}Cannot perform cleanup without Docker running.${NC}"
    exit 1
  fi
  
  # Check if containers are running
  if ! docker compose ps -q 2>/dev/null | grep -q .; then
    print_status "No running containers found"
  else
    # Step 1: List running containers
    print_status "The following containers are currently running:"
    docker compose ps
    echo ""
    
    # Step 2: Stop containers
    print_status "Stopping all services..."
    docker compose down &
    spinner $!
    print_success "All services stopped successfully"
  fi
  
  # Step 3: Ask about data removal
  local remove_data=false
  if confirm "Would you like to remove all data directories?" "N"; then
    remove_data=true
    
    print_status "Removing data directories..."
    echo -e "${YELLOW}This will delete:${NC}"
    echo -e "  - ${HOME}/phantom-folio-data/library (Documents)"
    echo -e "  - ${HOME}/phantom-folio-data/db (Database)"
    echo -e "  - ${HOME}/phantom-folio-data/temp (Temporary files)"
    echo -e "  - ${HOME}/phantom-folio-data/models (OCR models)"
    echo ""
    
    if confirm "Are you SURE you want to permanently delete all data?" "N"; then
      rm -rf "${HOME}/phantom-folio-data"
      print_success "All data directories removed"
    else
      print_status "Data removal cancelled"
      remove_data=false
    fi
  fi
  
  # Step 4: Ask about Docker cleanup
  local docker_cleanup=false
  if confirm "Would you like to clean up unused Docker resources?" "N"; then
    docker_cleanup=true
    
    print_status "Removing unused Docker volumes..."
    docker volume prune -f &
    spinner $!
    
    if confirm "Would you like to remove unused Docker images as well?" "N"; then
      print_status "Removing unused Docker images..."
      docker image prune -a -f &
      spinner $!
    fi
    
    print_success "Docker resources cleaned up"
  fi
  
  # Summary
  print_section "Cleanup Summary"
  
  echo -e "${BOLD}Actions taken:${NC}"
  echo -e "  - Services stopped: ${GREEN}Yes${NC}"
  echo -e "  - Data removed: $([ "$remove_data" = true ] && echo "${GREEN}Yes${NC}" || echo "${YELLOW}No${NC}")"
  echo -e "  - Docker resources cleaned: $([ "$docker_cleanup" = true ] && echo "${GREEN}Yes${NC}" || echo "${YELLOW}No${NC}")"
  echo ""
  
  if [ "$remove_data" = false ]; then
    echo -e "${YELLOW}Note: Data directories remain intact at:${NC}"
    echo -e "  - ${HOME}/phantom-folio-data/library"
    echo -e "  - ${HOME}/phantom-folio-data/db"
    echo -e "  - ${HOME}/phantom-folio-data/temp"
    echo -e "  - ${HOME}/phantom-folio-data/models"
    echo ""
    echo -e "${YELLOW}To remove all data, run:${NC}"
    echo -e "  rm -rf ${HOME}/phantom-folio-data"
  fi
  
  print_success "Cleanup completed successfully"
}

# Execute main function
main "$@"