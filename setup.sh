#!/bin/bash
# Setup script for Crochet Pattern Checker

echo "🚀 Setting up Crochet Pattern Checker..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install the package in development mode
echo "📦 Installing package..."
pip install -e .

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To test PDF support:"
echo "  PYTHONPATH=src python3 -c \"from crochet_checker.utils import read_pattern_file; print('✅ PDF support ready!')\""
echo ""
echo "To start the API server:"
echo "  uvicorn crochet_checker.api:app --host 0.0.0.0 --port 8000"
