#!/bin/bash

# Netlify Build Script for Flask Application
echo "🚀 Starting Netlify build for Ad Optimization Platform..."

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Verify installations
echo "✅ Verifying key packages..."
python -c "import flask, pandas, sklearn, sqlalchemy; print('✓ All packages installed successfully')"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static datasets reports

# Build complete
echo "🎉 Build completed successfully!"
echo "📍 Publish directory: static/"
echo "🔧 Functions directory: netlify/functions/"