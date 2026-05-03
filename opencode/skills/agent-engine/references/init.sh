#!/bin/bash
# Project Initialization Script
# This script sets up and starts the development server

set -e

echo "=== Initializing Project ==="

# Navigate to project directory
PROJECT_DIR="${PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

# Install dependencies
echo "Installing dependencies..."
if [ -f "package.json" ]; then
    npm install
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "Cargo.toml" ]; then
    cargo build
fi

# Start development server
echo "Starting development server..."
if [ -f "package.json" ]; then
    npm run dev &
elif [ -f "Makefile" ]; then
    make dev &
fi

# Wait for server to be ready
echo "Waiting for server to be ready..."
sleep 5

echo "=== Development server is running ==="
echo "Visit http://localhost:3000 (or your configured port)"
