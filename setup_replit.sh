#!/bin/bash
# Replit Setup Script for ClaimsIQ Platform

echo "🚀 Setting up ClaimsIQ Platform for Replit..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Initialize Reflex app
echo "🔧 Initializing Reflex..."
reflex init

# Export database if needed
echo "📊 Setting up database..."
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  Warning: DATABASE_URL not set. Using SQLite fallback."
    export DATABASE_URL="sqlite:///claimsiq.db"
fi

# Run database migrations/setup
echo "🗄️  Loading sample data..."
python scripts/load_sample_data.py 2>/dev/null || echo "⚠️  Sample data script not found or failed"

echo "✅ Setup complete!"
echo ""
echo "To start the app:"
echo "  reflex run --env prod --frontend-port 5000 --backend-port 8001"
