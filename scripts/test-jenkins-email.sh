#!/bin/bash
# Script to test Jenkins email configuration and diagnose issues

echo "=========================================="
echo "Jenkins Email Configuration Tester"
echo "=========================================="
echo ""

# Check if running as root (for some checks)
if [ "$EUID" -eq 0 ]; then
    SUDO=""
else
    SUDO="sudo"
fi

echo "1. Checking Email Extension Plugin..."
if [ -d "/var/lib/jenkins/plugins/email-ext" ]; then
    echo "   ✅ Email Extension Plugin appears to be installed"
else
    echo "   ⚠️  Email Extension Plugin may not be installed"
    echo "   Install from: Manage Jenkins → Manage Plugins → Email Extension Plugin"
fi

echo ""
echo "2. Checking Jenkins logs for email errors..."
if [ -f "/var/log/jenkins/jenkins.log" ]; then
    echo "   Recent email-related errors:"
    $SUDO tail -100 /var/log/jenkins/jenkins.log | grep -i "email\|smtp\|mail" | tail -5 || echo "   No recent email errors found"
else
    echo "   ⚠️  Jenkins log file not found at /var/log/jenkins/jenkins.log"
fi

echo ""
echo "3. Testing SMTP connection to Yahoo..."
echo "   Testing smtp.mail.yahoo.com:587..."

if command -v telnet > /dev/null 2>&1; then
    timeout 5 telnet smtp.mail.yahoo.com 587 <<EOF 2>&1 | head -3
quit
EOF
    if [ $? -eq 0 ]; then
        echo "   ✅ Port 587 is accessible"
    else
        echo "   ⚠️  Cannot connect to port 587 (may be blocked by firewall)"
    fi
else
    echo "   ⚠️  telnet not installed, skipping connection test"
    echo "   Install with: sudo apt-get install telnet"
fi

echo ""
echo "4. Testing SMTP connection to Yahoo (port 465)..."
if command -v telnet > /dev/null 2>&1; then
    timeout 5 telnet smtp.mail.yahoo.com 465 <<EOF 2>&1 | head -3
quit
EOF
    if [ $? -eq 0 ]; then
        echo "   ✅ Port 465 is accessible"
    else
        echo "   ⚠️  Cannot connect to port 465 (may be blocked by firewall)"
    fi
fi

echo ""
echo "5. Checking common email configuration issues..."
echo ""
echo "   Common problems and solutions:"
echo ""
echo "   ❌ Authentication Failed:"
echo "      → Use Yahoo App Password (not regular password)"
echo "      → Enable 2-Step Verification on Yahoo account"
echo "      → Generate app password: https://login.yahoo.com/account/security/app-passwords"
echo ""
echo "   ❌ Connection Timeout:"
echo "      → Verify SMTP server: smtp.mail.yahoo.com"
echo "      → Try port 465 with SSL instead of 587 with TLS"
echo "      → Check firewall settings"
echo ""
echo "   ❌ SSL/TLS Errors:"
echo "      → Port 587: Use TLS (not SSL)"
echo "      → Port 465: Use SSL (not TLS)"
echo "      → Don't check both SSL and TLS"
echo ""
echo "   ❌ Test Email Works But Build Emails Don't:"
echo "      → Check EMAIL_RECIPIENT in Jenkinsfile"
echo "      → Verify Email Extension Plugin is enabled"
echo "      → Check build console for email errors"
echo ""

echo "=========================================="
echo "Configuration Checklist"
echo "=========================================="
echo ""
echo "Verify these settings in Jenkins:"
echo ""
echo "Extended E-mail Notification:"
echo "  [ ] SMTP server: smtp.mail.yahoo.com"
echo "  [ ] SMTP Port: 587 (TLS) or 465 (SSL)"
echo "  [ ] Use SMTP Authentication: ✓ Checked"
echo "  [ ] User Name: groklord@yahoo.com"
echo "  [ ] Password: Yahoo App Password (16 characters)"
echo "  [ ] Use TLS: ✓ (for port 587) OR Use SSL: ✓ (for port 465)"
echo "  [ ] Default user e-mail suffix: @yahoo.com"
echo ""
echo "Yahoo Account:"
echo "  [ ] 2-Step Verification enabled"
echo "  [ ] App Password generated"
echo "  [ ] App Password format: xxxx-xxxx-xxxx-xxxx (16 characters)"
echo ""
echo "Test Configuration:"
echo "  [ ] Go to: Manage Jenkins → Configure System"
echo "  [ ] Scroll to Extended E-mail Notification"
echo "  [ ] Click 'Test configuration by sending test e-mail'"
echo "  [ ] Enter: groklord@yahoo.com"
echo "  [ ] Click 'Test configuration'"
echo "  [ ] Check email inbox (and spam folder)"
echo ""

echo "=========================================="
echo "Quick Fix Commands"
echo "=========================================="
echo ""
echo "If email test fails, try these:"
echo ""
echo "1. Check Jenkins logs:"
echo "   sudo tail -f /var/log/jenkins/jenkins.log"
echo ""
echo "2. Restart Jenkins:"
echo "   sudo systemctl restart jenkins"
echo ""
echo "3. Verify Email Extension Plugin:"
echo "   - Go to: Manage Jenkins → Manage Plugins"
echo "   - Check 'Installed' tab for 'Email Extension Plugin'"
echo ""
echo "4. Try alternative port:"
echo "   - If port 587 fails, try 465 with SSL"
echo "   - If port 465 fails, try 587 with TLS"
echo ""

echo "=========================================="
echo "For detailed instructions, see:"
echo "  JENKINS_EMAIL_SETUP.md"
echo "=========================================="

