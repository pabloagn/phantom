#!/usr/bin/env bash

# .devcontainer/post-create.sh

set -e # Exit immediately if a command exits with a non-zero status.
echo "--- Running Post Create Script ---"

# Install Node.js dependencies from the root
echo "Installing Node.js dependencies..."
pnpm install --frozen-lockfile

# Create a local version of pnpm
echo "Setting up local pnpm..."
npm install -g @pnpm/exe
pnpm setup

# Install turbo globally within the container for better performance
echo "Setting up turbo..."
pnpm add -g turbo

# Install Python dependencies for each package with pyproject.toml
echo "Installing Python dependencies..."
for dir in ./packages/*/; do
  if [ -f "${dir}pyproject.toml" ]; then
    echo "Found pyproject.toml in ${dir}, installing dependencies..."
    cd "${dir}"
    # Ensure Poetry uses the virtualenv within the project if possible
    poetry config virtualenvs.in-project true --local || true
    # Install dependencies using Poetry
    poetry install --no-root --sync
    # Navigate back to the root
    cd ../..
  fi
done

# Create .npmrc to ensure consistent behavior between environments
echo "Creating .npmrc file for consistent behavior..."
cat > .npmrc <<EOL
node-linker=hoisted
shamefully-hoist=true
EOL

echo "--- Post Create Script Finished ---"