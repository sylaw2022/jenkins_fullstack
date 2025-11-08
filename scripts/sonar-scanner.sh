#!/bin/bash

# SonarQube Scanner Script
# This script runs SonarQube analysis locally

set -e

# Load environment variables if .sonarqube.env exists
if [ -f .sonarqube.env ]; then
    source .sonarqube.env
fi

# Check if SonarQube Scanner is installed
if ! command -v sonar-scanner &> /dev/null; then
    echo "❌ SonarQube Scanner not found!"
    echo "Install it with: npm install -g sonarqube-scanner"
    echo "Or download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/"
    exit 1
fi

# Check required environment variables
if [ -z "$SONAR_HOST_URL" ]; then
    echo "❌ SONAR_HOST_URL not set!"
    echo "Set it in .sonarqube.env or export it:"
    echo "export SONAR_HOST_URL=http://localhost:9000"
    exit 1
fi

if [ -z "$SONAR_TOKEN" ]; then
    echo "❌ SONAR_TOKEN not set!"
    echo "Set it in .sonarqube.env or export it:"
    echo "Generate token from SonarQube: User > My Account > Security > Generate Token"
    exit 1
fi

echo "🔍 Running SonarQube analysis..."
echo "📊 SonarQube Server: $SONAR_HOST_URL"
echo "🔑 Project Key: jenkins-fullstack"
echo ""

# Run SonarQube Scanner
sonar-scanner \
    -Dsonar.projectKey=jenkins-fullstack \
    -Dsonar.sources=backend/src,frontend/src,backend/server.js \
    -Dsonar.host.url="$SONAR_HOST_URL" \
    -Dsonar.login="$SONAR_TOKEN"

echo ""
echo "✅ SonarQube analysis completed!"
echo "📈 View results at: $SONAR_HOST_URL/dashboard?id=jenkins-fullstack"

