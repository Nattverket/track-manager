#!/bin/bash
# Run all tests for track-manager

set -e

echo "🧪 Running track-manager tests..."
echo ""

# Check if pytest is installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "❌ pytest not installed"
    echo "   Install with: pip install -r requirements.txt"
    exit 1
fi

# Run tests
python3 -m pytest "$@"
