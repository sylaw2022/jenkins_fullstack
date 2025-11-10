#!/bin/bash
# Script to check Jenkins webhook configuration and provide setup instructions

echo "=========================================="
echo "Jenkins Auto-Build Configuration Checker"
echo "=========================================="
echo ""

# Check if Jenkins is running
echo "1. Checking Jenkins service..."
if systemctl is-active --quiet jenkins; then
    echo "   ✅ Jenkins service is running"
else
    echo "   ❌ Jenkins service is NOT running"
    echo "   Start with: sudo systemctl start jenkins"
    exit 1
fi

# Check Jenkins port
JENKINS_PORT=$(grep HTTP_PORT /etc/default/jenkins 2>/dev/null | cut -d'=' -f2 || echo "8081")
echo "2. Jenkins port: ${JENKINS_PORT}"
echo "   Jenkins URL: http://localhost:${JENKINS_PORT}"

# Check if Jenkins is accessible
echo ""
echo "3. Testing Jenkins accessibility..."
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:${JENKINS_PORT}" | grep -q "200\|403"; then
    echo "   ✅ Jenkins is accessible"
else
    echo "   ⚠️  Jenkins might not be accessible (this is OK if it's starting up)"
fi

# Check webhook endpoint
echo ""
echo "4. Testing webhook endpoint..."
WEBHOOK_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${JENKINS_PORT}/github-webhook/" 2>/dev/null)
if [ "$WEBHOOK_RESPONSE" = "200" ] || [ "$WEBHOOK_RESPONSE" = "405" ] || [ "$WEBHOOK_RESPONSE" = "403" ]; then
    echo "   ✅ Webhook endpoint exists (HTTP ${WEBHOOK_RESPONSE})"
else
    echo "   ⚠️  Webhook endpoint might not be configured (HTTP ${WEBHOOK_RESPONSE})"
fi

# Check GitHub repository
echo ""
echo "5. Checking Git remote configuration..."
if git remote get-url github &>/dev/null; then
    GITHUB_URL=$(git remote get-url github)
    echo "   ✅ GitHub remote found: ${GITHUB_URL}"
    
    # Extract repository name
    REPO_NAME=$(echo "$GITHUB_URL" | sed 's/.*github.com[:/]\([^.]*\).*/\1/')
    echo "   Repository: ${REPO_NAME}"
else
    echo "   ⚠️  GitHub remote not found"
    echo "   Current remotes:"
    git remote -v
fi

echo ""
echo "=========================================="
echo "Configuration Status"
echo "=========================================="
echo ""
echo "To enable automatic builds on Git push:"
echo ""
echo "1. Install GitHub Plugin:"
echo "   - Go to: http://localhost:${JENKINS_PORT}"
echo "   - Manage Jenkins → Manage Plugins"
echo "   - Search for 'GitHub plugin' and install"
echo ""
echo "2. Configure Pipeline Job:"
echo "   - Go to your pipeline job"
echo "   - Click Configure"
echo "   - Build Triggers → Check 'GitHub hook trigger for GITScm polling'"
echo "   - Save"
echo ""
echo "3. Add GitHub Webhook:"
if [ -n "$REPO_NAME" ]; then
    echo "   - Go to: https://github.com/${REPO_NAME}/settings/hooks"
    echo "   - Click 'Add webhook'"
    echo "   - Payload URL: http://YOUR_PUBLIC_IP:${JENKINS_PORT}/github-webhook/"
    echo "   - Content type: application/json"
    echo "   - Events: Just the push event"
    echo "   - Active: ✓"
else
    echo "   - Go to your GitHub repository → Settings → Webhooks"
    echo "   - Add webhook with URL: http://YOUR_PUBLIC_IP:${JENKINS_PORT}/github-webhook/"
fi
echo ""
echo "4. Alternative: Use Poll SCM (if webhooks don't work):"
echo "   - In pipeline job → Build Triggers → Poll SCM"
echo "   - Schedule: H/5 * * * *  (checks every 5 minutes)"
echo ""
echo "=========================================="
echo "For detailed instructions, see:"
echo "  JENKINS_WEBHOOK_SETUP.md"
echo "=========================================="

