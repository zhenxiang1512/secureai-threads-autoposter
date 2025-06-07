#!/bin/bash

# GitHub Setup Script for SecureAI Threads Auto Poster
# This script helps you set up the repository on GitHub

echo "🚀 Setting up SecureAI Threads Auto Poster on GitHub..."
echo "=================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create initial commit if needed
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    echo "📝 Creating initial commit..."
    git add .
    git commit -m "Initial commit: SecureAI Threads Auto Poster setup"
    echo "✅ Initial commit created"
fi

echo ""
echo "🔧 Next Steps:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Copy the repository URL (e.g., https://github.com/yourusername/secureai-threads)"
echo "3. Run: git remote add origin YOUR_GITHUB_REPO_URL"
echo "4. Run: git branch -M main"
echo "5. Run: git push -u origin main"
echo ""
echo "🔐 GitHub Secrets Setup:"
echo "After pushing to GitHub, go to:"
echo "Repository → Settings → Secrets and variables → Actions"
echo ""
echo "Add these secrets with your actual values:"
echo "- THREADS_APP_ID"
echo "- THREADS_APP_SECRET" 
echo "- THREADS_USER_ID"
echo "- THREADS_LONG_LIVED_TOKEN"
echo ""
echo "🎯 Testing:"
echo "- Go to Actions tab → 'Test Threads API' → 'Run workflow' to test"
echo "- The auto-posting will run daily at 10:00 AM Malaysia time"
echo ""
echo "📚 For detailed instructions, see the README.md file"