#!/usr/bin/env bash
# packages/phantom-core/scripts/setup-dev.sh
# Sets up the essential development environment after cloning.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "🚀 Setting up Phantom development environment..."
echo "   Working directory: $(pwd)" # Confirm we are in /workspace

# 1. Check for necessary tools (Node, npm are assumed present in container)
echo "🔎 Checking prerequisites..."
command -v node >/dev/null 2>&1 || { echo >&2 "❌ Node.js not found. Aborting."; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo >&2 "❌ npm not found. Aborting."; exit 1; }
echo "✅ Prerequisites met."

# 2. Install dependencies (might be redundant if postCreateCommand ran, but safe)
echo "📦 Installing/Verifying project dependencies..."
pnpm install --loglevel error # Use --loglevel error to reduce noise
echo "✅ Dependencies installed/verified."

# 3. Copy environment files if they don't exist
if [ ! -f ".env" ]; then
  echo "📄 Copying .env.example to .env..."
  cp .env.example .env
  echo "❗ IMPORTANT: Please review and update the .env file with your settings."
else
  echo "📄 .env file already exists. Skipping copy."
fi

# Check if docker/.env.example exists before copying
if [ -f "docker/.env.example" ]; then
  if [ ! -f "docker/.env" ]; then
    echo "📄 Copying docker/.env.example to docker/.env..."
    cp docker/.env.example docker/.env
    echo "❗ IMPORTANT: Please review and update the docker/.env file with your Docker service settings."
  else
    echo "📄 docker/.env file already exists. Skipping copy."
  fi
else
    echo "ℹ️ docker/.env.example not found. Skipping Docker env setup."
fi


# 4. Build necessary initial assets (Design Tokens)
# Ensure the build:tokens script exists and works.
if pnpm run build:tokens --loglevel error; then
  echo "✅ Design tokens built successfully."
else
  echo >&2 "❌ Failed to build design tokens. Check 'scripts/build-tokens.js' and its dependencies. Aborting setup."
  exit 1
fi

# 5. Optional: Run initial checks (Uncomment if desired, but might be slow for setup)
# echo "✨ Running initial format check..."
# if npm run format:check --loglevel error; then
#   echo "✅ Code formatting looks good."
# else
#   echo >&2 "❌ Code formatting issues found. Run 'npm run format' to fix."
#   # Decide if this should be a fatal error for setup
#   # exit 1
# fi
# echo "✨ Running initial type check..."
# if npm run typecheck --loglevel error; then
#   echo "✅ TypeScript checks passed."
# else
#   echo >&2 "❌ TypeScript errors found. Check the output above."
#   # Decide if this should be a fatal error for setup
#   # exit 1
# fi


echo "🎉 Development environment setup script complete!"
echo "   You can now run commands like 'pnpm run dev' (for docs) or start other services."

exit 0