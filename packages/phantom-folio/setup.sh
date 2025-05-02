#!/usr/bin/env bash
# setup.sh - Setup script for Phantom Folio

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

# Progress bar for waiting operations
progress_bar() {
  local title=$1
  local duration=$2
  local width=50
  local percent=0
  local elapsed=0
  local step=$((duration / width))
  
  echo -e "${YELLOW}$title${NC}"
  
  printf "["
  for i in $(seq 1 $width); do
    printf " "
  done
  printf "] 0%%"
  
  for i in $(seq 1 $width); do
    sleep $step
    elapsed=$((elapsed + step))
    percent=$((elapsed * 100 / duration))
    
    # Return to start of progress bar
    printf "\r["
    
    # Print filled portion
    for j in $(seq 1 $i); do
      printf "="
    done
    
    # Print unfilled portion
    for j in $(seq 1 $((width - i))); do
      printf " "
    done
    
    printf "] %d%%" $percent
  done
  
  printf "\n"
}

# Function to check if a port is in use
check_port() {
  local port=$1
  local service=$2
  
  # Check if port is in use
  if command -v nc >/dev/null 2>&1; then
    if nc -z localhost $port >/dev/null 2>&1; then
      print_error "Port $port ($service) is already in use!"
      echo -e "  ${YELLOW}Please free up this port before continuing.${NC}"
      return 1
    fi
  elif command -v lsof >/dev/null 2>&1; then
    if lsof -i :$port >/dev/null 2>&1; then
      print_error "Port $port ($service) is already in use!"
      echo -e "  ${YELLOW}Please free up this port before continuing.${NC}"
      return 1
    fi
  else
    echo -e "${YELLOW}Warning: Unable to check if port $port is in use (nc or lsof not found).${NC}"
  fi
  
  return 0
}

# Function to wait for a container to be healthy
wait_for_container() {
  local container=$1
  local service_name=$2
  local max_attempts=$3
  local attempt=0
  
  echo -e "${YELLOW}Waiting for $service_name to be ready...${NC}"
  
  while [ $attempt -lt $max_attempts ]; do
    if docker ps | grep -q "$container" && \
       docker inspect --format='{{.State.Running}}' "$container" 2>/dev/null | grep -q "true"; then
      
      # If container has health check, wait for it to be healthy
      if docker inspect --format='{{if .Config.Healthcheck}}{{.State.Health.Status}}{{else}}none{{end}}' "$container" 2>/dev/null | grep -q "healthy"; then
        print_success "$service_name is ready"
        return 0
      elif docker inspect --format='{{if .Config.Healthcheck}}{{.State.Health.Status}}{{else}}none{{end}}' "$container" 2>/dev/null | grep -q "none"; then
        # Container doesn't have health check but is running
        print_success "$service_name is ready"
        return 0
      fi
    fi
    
    attempt=$((attempt+1))
    printf "  Attempt %d/%d: " $attempt $max_attempts
    
    # Show status indicators
    if docker ps | grep -q "$container"; then
      local status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null)
      
      if [ "$status" = "running" ]; then
        local health=$(docker inspect --format='{{if .Config.Healthcheck}}{{.State.Health.Status}}{{else}}none{{end}}' "$container" 2>/dev/null)
        
        if [ "$health" = "none" ]; then
          echo -e "${YELLOW}Running (no health check)${NC}"
        else
          echo -e "${YELLOW}Running, health: $health${NC}"
        fi
      else
        echo -e "${YELLOW}Status: $status${NC}"
      fi
    else
      echo -e "${YELLOW}Not created yet${NC}"
    fi
    
    sleep 2
  done
  
  print_error "$service_name failed to start properly after $max_attempts attempts"
  echo -e "${YELLOW}Container logs:${NC}"
  docker logs $container | tail -10
  return 1
}

# Main setup function
main() {
	print_section "Phantom Folio Setup"
  
  # Step 1: Check prerequisites
  print_status "Checking prerequisites..."
  
  # Check Docker
  if ! command -v docker >/dev/null 2>&1; then
    print_error "Docker is not installed or not in PATH"
    echo -e "  ${YELLOW}Please install Docker first.${NC}"
    exit 1
  fi
  
  # Check Docker Compose
  if ! command -v docker compose >/dev/null 2>&1; then
    print_error "Docker Compose is not installed or not in PATH"
    echo -e "  ${YELLOW}Please install Docker Compose first.${NC}"
    exit 1
  fi
  
  # Check if Docker daemon is running
  if ! docker info >/dev/null 2>&1; then
    print_error "Docker daemon is not running"
    echo -e "  ${YELLOW}Please start the Docker daemon first.${NC}"
    exit 1
  fi
  
  print_success "All prerequisites satisfied"
  
  # Step 2: Check required ports
  print_status "Checking required ports..."
  
  # List of required ports and their services
  local ports=(
    "8000:API Server"
    "8080:Web Interface"
    "5432:Database"
    "6379:Redis"
  )
  
  # Check each port
  local port_error=0
  for port_info in "${ports[@]}"; do
    local port=$(echo $port_info | cut -d':' -f1)
    local service=$(echo $port_info | cut -d':' -f2)
    
    if ! check_port "$port" "$service"; then
      port_error=1
    fi
  done
  
  if [ $port_error -eq 1 ]; then
    print_error "One or more required ports are not available"
    exit 1
  fi
  
  print_success "All required ports are available"
  
  # Step 3: Create project directories
  print_status "Creating project directories..."
  
  # Create directory structure
  mkdir -p "${HOME}/phantom-folio-data/library"
  mkdir -p "${HOME}/phantom-folio-data/db"
  mkdir -p "${HOME}/phantom-folio-data/temp"
  mkdir -p "${HOME}/phantom-folio-data/models"
  mkdir -p "${HOME}/phantom-folio-data/models/tessdata"
  
  print_success "Project directories created"
  
  # Step 4: Set up Docker environment
  print_status "Setting up Docker environment..."
  
  # Stop any existing containers first
  if docker compose ps -q 2>/dev/null | grep -q .; then
    print_status "Stopping existing containers..."
    docker compose down >/dev/null 2>&1 &
    spinner $!
  fi


	# Build and pull required images
	print_status "Building and pulling Docker images (this may take a few minutes)..."

	# First pull standard images
	print_status "Pulling standard images (PostgreSQL, Redis)..."
	if ! docker compose pull db redis; then
	  print_error "Failed to pull standard Docker images"
	  exit 1
	fi

	# Then build custom images
	print_status "Building custom images (web, ocr-worker)..."
	if ! docker compose build web ocr-worker; then
	  print_error "Failed to build custom Docker images"
	  exit 1
	fi

	print_success "Docker images prepared successfully"

  # Step 5: Start containers
  print_section "Starting Phantom Folio Services"
  
  print_status "Launching containers..."
  docker compose up -d
  
  # Step 6: Wait for services to be ready
  print_status "Waiting for services to initialize..."
  
  # Wait for PostgreSQL
  wait_for_container "phantom-folio-db" "Database" 30
  
  # Wait for Redis
  wait_for_container "phantom-folio-redis" "Redis" 15
  
  # Wait for OCR Worker
  wait_for_container "phantom-folio-ocr-worker" "OCR Worker" 45
  
  # Wait for Web service
  wait_for_container "phantom-folio-web" "Web Interface" 30
  
  # Step 7: Initialize database
  print_status "Initializing database..."
  docker compose exec -T db psql -U postgres -c "CREATE DATABASE phantom_folio;" 2>/dev/null || echo -e "${YELLOW}Database already exists, skipping creation.${NC}"
  
  # Add a small delay to ensure everything is ready
  progress_bar "Finalizing setup..." 5
  
  # Step 8: Display service information
  print_section "Phantom Folio is Ready!"
  
  echo -e "${BOLD}${GREEN}Services:${NC}"
  echo -e "  ${BOLD}Web Interface:${NC} http://localhost:8080"
  echo -e "  ${BOLD}API Server:${NC} http://localhost:8000"
  echo -e "  ${BOLD}Database:${NC} localhost:5432 (PostgreSQL)"
  echo -e "  ${BOLD}Redis:${NC} localhost:6379"
  echo ""
  
  echo -e "${BOLD}${GREEN}Data Directories:${NC}"
  echo -e "  ${BOLD}Document Library:${NC} ${HOME}/phantom-folio-data/library"
  echo -e "  ${BOLD}Database Files:${NC} ${HOME}/phantom-folio-data/db"
  echo -e "  ${BOLD}Temporary Files:${NC} ${HOME}/phantom-folio-data/temp"
  echo -e "  ${BOLD}Models:${NC} ${HOME}/phantom-folio-data/models"
  echo ""
  
  echo -e "${BOLD}${GREEN}Container Status:${NC}"
  docker compose ps
  echo ""
  
  echo -e "${BOLD}${BLUE}Quick Commands:${NC}"
  echo -e "  ${YELLOW}docker compose logs -f${NC} - View logs from all services"
  echo -e "  ${YELLOW}docker compose logs -f [service]${NC} - View logs from a specific service"
  echo -e "  ${YELLOW}docker compose restart [service]${NC} - Restart a specific service"
  echo -e "  ${YELLOW}./cleanup.sh${NC} - Stop all services and clean up resources"
  echo -e "  ${YELLOW}python -m phantom_folio${NC} - Run the application"
  echo ""
  
  echo -e "${BOLD}${GREEN}Phantom Folio is now ready to use!${NC}"
}

# Execute main function
main "$@"
