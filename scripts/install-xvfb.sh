#!/bin/bash
# Script to install Xvfb and dependencies for headless browser testing

echo "Installing Xvfb and dependencies for Cypress headless testing..."

sudo apt-get update
sudo apt-get install -y xvfb x11-utils x11-xserver-utils libx11-dev libxcomposite-dev libxdamage-dev libxext-dev libxfixes-dev libxrandr-dev libxrender-dev libxtst-dev libxss1 libgconf-2-4

echo ""
echo "✅ Xvfb installation complete!"
echo ""
echo "To verify installation:"
echo "  which Xvfb"
echo "  Xvfb --help"
echo ""
echo "Xvfb will be used by Cypress for headless browser testing in Jenkins."

