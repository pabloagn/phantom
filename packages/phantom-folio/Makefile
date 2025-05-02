# Makefile for Phantom Folio

.PHONY: dev dev-with-claude setup cleanup help

# Default target
help:
	@echo "Phantom Folio Development"
	@echo ""
	@echo "Available targets:"
	@echo "  make dev           - Start development environment (without Claude Code)"
	@echo "  make dev-with-claude - Start development environment with Claude Code enabled"
	@echo "  make setup         - Initialize project infrastructure"
	@echo "  make cleanup       - Stop services and clean up resources"
	@echo "  make help          - Show this help"

# Start development environment
dev:
	@./scripts/dev.sh

# Start development environment with Claude Code
dev-with-claude:
	@./scripts/dev-with-claude.sh

# Initialize project infrastructure
setup:
	@./setup.sh

# Clean up project resources
cleanup:
	@./cleanup.sh
