# Jenkins Email Test Configuration Failed - Troubleshooting Guide

## Quick Diagnosis

If the email test configuration failed in Jenkins, follow these steps:

---

## Step 1: Check Error Message

The error message will tell you what's wrong:

### "Authentication failed"
- **Problem**: Wrong password or not using App Password
- **Solution**: See [Authentication Issues](#authentication-issues) below

### "Connection timeout" or "Cannot connect to SMTP server"
- **Problem**: Network/firewall issue or wrong SMTP settings
- **Solution**: See [Connection Issues](#connection-issues) below

### "SSL/TLS handshake failed"
- **Problem**: Wrong SSL/TLS configuration
- **Solution**: See [SSL/TLS Issues](#ssltls-issues) below

### "Test email sent successfully" but no email received
- **Problem**: Email delivery issue
- **Solution**: See [Email Delivery Issues](#email-delivery-issues) below

---

## Authentication Issues

### Problem: "Authentication failed" or "Invalid credentials"

**Most Common Causes:**

1. **Using regular password instead of App Password**
   - ❌ Wrong: Using your Yahoo account password
   - ✅ Correct: Using Yahoo App Password (16 characters)

2. **2-Step Verification not enabled**
   - Yahoo requires 2-Step Verification to generate App Passwords
   - Enable it first: https://login.yahoo.com/account/security

3. **Wrong App Password format**
   - App Password should be 16 characters
   - Format: `xxxx-xxxx-xxxx-xxxx` (with or without dashes)
   - Example: `abcd-efgh-ijkl-mnop`

**Fix Steps:**

1. **Generate New Yahoo App Password:**
   ```
   1. Go to: https://login.yahoo.com/account/security/app-passwords
   2. Sign in with your Yahoo account
   3. Select "Mail" as the app
   4. Select "Other" as the device
   5. Click "Generate"
   6. Copy the 16-character password immediately (you'll only see it once!)
   ```

2. **Update Jenkins Configuration:**
   ```
   - Go to: Manage Jenkins → Configure System
   - Scroll to "Extended E-mail Notification"
   - Enter the App Password in the "Password" field
   - Make sure "Use SMTP Authentication" is checked
   - Click "Save"
   ```

3. **Test Again:**
   - Click "Test configuration by sending test e-mail"
   - Enter: `groklord@yahoo.com`
   - Click "Test configuration"

---

## Connection Issues

### Problem: "Connection timeout" or "Cannot connect to SMTP server"

**Common Causes:**

1. **Wrong SMTP server**
   - ❌ Wrong: `smtp.yahoo.com`
   - ✅ Correct: `smtp.mail.yahoo.com`

2. **Wrong port**
   - Port 587: Use with TLS
   - Port 465: Use with SSL
   - Don't mix them up!

3. **Firewall blocking ports**
   - Ports 587 and 465 may be blocked
   - Check firewall settings

**Fix Steps:**

1. **Verify SMTP Settings:**
   ```
   SMTP server: smtp.mail.yahoo.com
   SMTP Port: 587 (with TLS) OR 465 (with SSL)
   ```

2. **Test Connection:**
   ```bash
   # Test port 587
   telnet smtp.mail.yahoo.com 587
   
   # Test port 465
   telnet smtp.mail.yahoo.com 465
   ```

3. **Try Alternative Port:**
   - If port 587 doesn't work, try 465 with SSL
   - If port 465 doesn't work, try 587 with TLS

4. **Check Firewall:**
   ```bash
   # Check if ports are blocked
   sudo ufw status
   # Or
   sudo iptables -L
   ```

---

## SSL/TLS Issues

### Problem: "SSL/TLS handshake failed" or "Certificate errors"

**Common Causes:**

1. **Wrong SSL/TLS setting for port**
   - Port 587: Must use TLS (not SSL)
   - Port 465: Must use SSL (not TLS)

2. **Both SSL and TLS checked**
   - Only check ONE: either SSL OR TLS, not both

**Fix Steps:**

1. **For Port 587:**
   ```
   SMTP Port: 587
   Use SSL: ☐ (Unchecked)
   Use TLS: ✓ (Checked)
   ```

2. **For Port 465:**
   ```
   SMTP Port: 465
   Use SSL: ✓ (Checked)
   Use TLS: ☐ (Unchecked)
   ```

3. **Test Both Configurations:**
   - Try port 587 with TLS first
   - If that fails, try port 465 with SSL

---

## Email Delivery Issues

### Problem: "Test email sent successfully" but no email received

**Common Causes:**

1. **Email in spam folder**
   - Check spam/junk folder
   - Mark as "Not Spam" if found

2. **Wrong recipient email**
   - Verify email address: `groklord@yahoo.com`
   - Check for typos

3. **Yahoo email filters**
   - Check Yahoo Mail filters
   - Check blocked senders list

**Fix Steps:**

1. **Check Spam Folder:**
   - Log in to Yahoo Mail
   - Check Spam/Junk folder
   - Look for emails from Jenkins

2. **Verify Email Address:**
   - Make sure recipient is exactly: `groklord@yahoo.com`
   - No typos or extra spaces

3. **Check Yahoo Mail Settings:**
   - Go to: https://mail.yahoo.com
   - Settings → Filters
   - Make sure Jenkins emails aren't being filtered

---

## Step-by-Step Fix Procedure

### Complete Reset and Reconfiguration

1. **Clear Current Configuration:**
   ```
   - Go to: Manage Jenkins → Configure System
   - Scroll to "Extended E-mail Notification"
   - Clear all fields
   - Click "Save"
   ```

2. **Reconfigure from Scratch:**
   ```
   SMTP server: smtp.mail.yahoo.com
   Default user e-mail suffix: @yahoo.com
   Use SMTP Authentication: ✓ Checked
   User Name: groklord@yahoo.com
   Password: [Yahoo App Password - 16 characters]
   Use SSL: ☐ Unchecked
   Use TLS: ✓ Checked
   SMTP Port: 587
   Reply To List: groklord@yahoo.com
   Content Type: HTML (text/html)
   ```

3. **Test Configuration:**
   ```
   - Scroll to "Test configuration by sending test e-mail"
   - Enter: groklord@yahoo.com
   - Click "Test configuration"
   - Wait for result
   ```

4. **If Still Fails, Try Port 465:**
   ```
   SMTP Port: 465
   Use SSL: ✓ Checked
   Use TLS: ☐ Unchecked
   (Keep all other settings the same)
   ```

5. **Check Jenkins Logs:**
   ```bash
   sudo tail -f /var/log/jenkins/jenkins.log
   # Look for email-related errors
   ```

---

## Alternative: Use Gmail Instead

If Yahoo continues to have issues, you can use Gmail:

### Gmail SMTP Settings:
```
SMTP server: smtp.gmail.com
SMTP Port: 587 (TLS) or 465 (SSL)
Username: your-email@gmail.com
Password: Gmail App Password (16 characters)
Use TLS: ✓ (for port 587)
Use SSL: ✓ (for port 465)
```

### Generate Gmail App Password:
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate App Password
4. Use the 16-character password in Jenkins

---

## Verification Checklist

After fixing, verify:

- [ ] Email Extension Plugin is installed
- [ ] 2-Step Verification is enabled on Yahoo account
- [ ] Yahoo App Password is generated (16 characters)
- [ ] SMTP server: `smtp.mail.yahoo.com`
- [ ] SMTP Port: `587` (TLS) or `465` (SSL)
- [ ] Correct SSL/TLS setting for chosen port
- [ ] Username: `groklord@yahoo.com`
- [ ] Password: Yahoo App Password (not regular password)
- [ ] "Use SMTP Authentication" is checked
- [ ] Test email sent successfully
- [ ] Email received in inbox (check spam folder too)

---

## Still Having Issues?

1. **Check Jenkins Logs:**
   ```bash
   sudo tail -100 /var/log/jenkins/jenkins.log | grep -i email
   ```

2. **Run Diagnostic Script:**
   ```bash
   ./scripts/test-jenkins-email.sh
   ```

3. **Try Manual SMTP Test:**
   ```bash
   # Install mailutils for testing
   sudo apt-get install mailutils
   
   # Test sending email (requires proper configuration)
   echo "Test" | mail -s "Test" groklord@yahoo.com
   ```

4. **Contact Support:**
   - Check Jenkins community forums
   - Review Email Extension Plugin documentation
   - Check Yahoo Mail SMTP documentation

---

## Quick Reference: Yahoo SMTP Settings

| Setting | Value |
|---------|-------|
| **SMTP Server** | `smtp.mail.yahoo.com` |
| **Port 587** | Use with TLS |
| **Port 465** | Use with SSL |
| **Username** | `groklord@yahoo.com` |
| **Password** | Yahoo App Password (16 chars) |
| **Authentication** | Required (App Password) |
| **2-Step Verification** | Must be enabled |

---

**Remember**: Always use Yahoo App Password, never your regular Yahoo account password!

