#!/bin/bash
# Script to install Xvfb on Jenkins server to fix Cypress E2E tests
# Run this script on the Jenkins server (where Jenkins is running)

echo "=========================================="
echo "Installing Xvfb for Cypress E2E Tests"
echo "=========================================="
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  This script needs sudo privileges to install packages"
    echo "Run with: sudo $0"
    exit 1
fi

echo "1. Updating package list..."
apt-get update -qq

echo "2. Installing Xvfb and dependencies..."
apt-get install -y \
    xvfb \
    x11-utils \
    x11-xserver-utils \
    libx11-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxext-dev \
    libxfixes-dev \
    libxrandr-dev \
    libxrender-dev \
    libxtst-dev \
    libxss1 \
    libgconf-2-4 \
    libgtk-3-0 \
    libgbm-dev \
    libnss3 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils

echo ""
echo "3. Verifying installation..."
if command -v Xvfb > /dev/null 2>&1; then
    echo "   ✅ Xvfb installed successfully"
    Xvfb --help | head -3
else
    echo "   ❌ Xvfb installation failed"
    exit 1
fi

echo ""
echo "4. Testing Xvfb..."
export DISPLAY=:99
Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 &
XVFB_PID=$!
sleep 2

if ps -p $XVFB_PID > /dev/null; then
    echo "   ✅ Xvfb started successfully (PID: $XVFB_PID)"
    kill $XVFB_PID 2>/dev/null
else
    echo "   ⚠️  Xvfb test failed, but installation may still work"
fi

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Xvfb is now installed and ready for Cypress E2E tests."
echo "The next Jenkins build should work without the Xvfb error."
echo ""
echo "To verify, run:"
echo "  which Xvfb"
echo "  Xvfb --help"

