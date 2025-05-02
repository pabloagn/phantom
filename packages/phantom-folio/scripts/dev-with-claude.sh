#!/usr/bin/env bash
# Development environment with Claude Code enabled

# Run nix-shell with Claude Code flag
nix-shell --pure --arg withClaude true
