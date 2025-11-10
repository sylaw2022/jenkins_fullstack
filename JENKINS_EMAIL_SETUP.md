# Jenkins Email Configuration Guide for Yahoo Mail

Complete guide to configure Jenkins email notifications using `groklord@yahoo.com` for the GROKLORD Fullstack Application.

## Overview

This project is configured to send email notifications to **groklord@yahoo.com** for:
- ❌ Build failures
- ⚠️ Unstable builds (warnings)
- 🛑 Aborted builds
- ❌ Test failures (Backend, Frontend, API, E2E)
- ⚠️ SonarQube quality gate failures

---

## Step 1: Install Email Extension Plugin

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Click on **Available** tab
3. Search for: **Email Extension Plugin**
4. Check the box and click **Install without restart** or **Download now and install after restart**
5. **Restart Jenkins** when prompted:
   ```bash
   sudo systemctl restart jenkins
   ```

---

## Step 2: Generate Yahoo App Password

Yahoo requires an **App Password** for SMTP authentication (not your regular password).

### Generate Yahoo App Password:

1. **Sign in to Yahoo Account Security**:
   - Go to: https://login.yahoo.com/account/security
   - Sign in with your Yahoo account

2. **Enable 2-Step Verification** (if not already enabled):
   - Click on **2-Step Verification**
   - Follow the prompts to enable it
   - You'll need a phone number

3. **Generate App Password**:
   - Go to: https://login.yahoo.com/account/security/app-passwords
   - Or: Account Security → Generate app password
   - Select **Mail** as the app
   - Select **Other** as the device (or your device name)
   - Click **Generate**
   - **Copy the 16-character password** (you'll see it only once!)
   - Example format: `abcd-efgh-ijkl-mnop`

**Important**: Save this app password securely. You'll need it for Jenkins configuration.

---

## Step 3: Configure SMTP Settings in Jenkins

### Step 3.1: Extended E-mail Notification (Recommended)

1. Go to **Manage Jenkins** → **Configure System**

2. Scroll down to **Extended E-mail Notification** section

3. Configure the following settings:

   **SMTP Server Configuration:**
   ```
   SMTP server: smtp.mail.yahoo.com
   Default user e-mail suffix: @yahoo.com
   Use SMTP Authentication: ✓ (Checked)
   User Name: groklord@yahoo.com
   Password: [Your Yahoo App Password - 16 characters]
   Use SSL: ☐ (Unchecked)
   Use TLS: ✓ (Checked)
   SMTP Port: 587
   ```

   **Advanced Settings:**
   ```
   Reply To List: groklord@yahoo.com
   Content Type: HTML (text/html)
   Default Subject: ${PROJECT_NAME} - Build #${BUILD_NUMBER} - ${BUILD_STATUS}!
   Default Content: [Leave default or customize]
   ```

4. **Test the Configuration**:
   - Scroll down and find **Test configuration by sending test e-mail**
   - Enter recipient: `groklord@yahoo.com`
   - Click **Test configuration**
   - Check your email inbox for the test message
   - If successful, you'll see a green success message

5. Click **Save**

### Step 3.2: E-mail Notification (Default - Optional)

1. In the same **Configure System** page, scroll to **E-mail Notification** section

2. Configure basic email settings:
   ```
   SMTP server: smtp.mail.yahoo.com
   Default user e-mail suffix: @yahoo.com
   Use SMTP Authentication: ✓ (Checked)
   User Name: groklord@yahoo.com
   Password: [Your Yahoo App Password]
   Use SSL: ☐ (Unchecked)
   SMTP Port: 587
   Reply-To Address: groklord@yahoo.com
   ```

3. Click **Save**

---

## Step 4: Verify Email Configuration

### Test Email Configuration:

1. **From Jenkins UI**:
   - Go to **Manage Jenkins** → **Configure System**
   - Scroll to **Extended E-mail Notification**
   - Click **Test configuration by sending test e-mail**
   - Enter: `groklord@yahoo.com`
   - Click **Test configuration**
   - Check your email

2. **From Pipeline** (after setup):
   - Run a build that triggers email notification
   - Check your inbox for the notification

---

## Step 5: Current Project Email Configuration

The Jenkinsfile is already configured to send emails to `groklord@yahoo.com`:

```groovy
environment {
    EMAIL_RECIPIENT = 'groklord@yahoo.com'
}
```

### Email Notifications Sent For:

1. **Build Failures** - When entire pipeline fails
2. **Backend Test Failures** - When backend unit tests fail
3. **Frontend Test Failures** - When frontend unit tests fail
4. **Build Failures** - When build stage fails
5. **API Test Failures** - When Postman/Newman tests fail
6. **E2E Test Failures** - When Cypress tests fail
7. **SonarQube Quality Gate Failures** - When code quality checks fail
8. **Unstable Builds** - When build completes with warnings
9. **Aborted Builds** - When build is manually aborted

---

## Yahoo SMTP Settings Summary

| Setting | Value |
|---------|-------|
| **SMTP Server** | `smtp.mail.yahoo.com` |
| **SMTP Port** | `587` (TLS) or `465` (SSL) |
| **Security** | TLS (recommended) or SSL |
| **Authentication** | Required (App Password) |
| **Username** | `groklord@yahoo.com` |
| **Password** | Yahoo App Password (16 characters) |
| **From Address** | `groklord@yahoo.com` |
| **Reply-To** | `groklord@yahoo.com` |

---

## Troubleshooting

### Issue: "Authentication failed"

**Solutions:**
1. ✅ Verify you're using **App Password**, not your regular Yahoo password
2. ✅ Ensure 2-Step Verification is enabled on your Yahoo account
3. ✅ Check the app password is correct (16 characters, format: `xxxx-xxxx-xxxx-xxxx`)
4. ✅ Verify username is exactly: `groklord@yahoo.com`

### Issue: "Connection timeout" or "Cannot connect to SMTP server"

**Solutions:**
1. ✅ Verify SMTP server: `smtp.mail.yahoo.com`
2. ✅ Check port: `587` for TLS or `465` for SSL
3. ✅ Ensure TLS is checked (for port 587) or SSL is checked (for port 465)
4. ✅ Check firewall settings
5. ✅ Try port 465 with SSL instead of 587 with TLS

### Issue: "Emails not received"

**Solutions:**
1. ✅ Check spam/junk folder
2. ✅ Verify recipient email: `groklord@yahoo.com`
3. ✅ Check Jenkins logs: `/var/log/jenkins/jenkins.log`
4. ✅ Test email configuration from Jenkins UI
5. ✅ Verify email is sent (check build console for email sending logs)

### Issue: "Test email works but build emails don't"

**Solutions:**
1. ✅ Verify `EMAIL_RECIPIENT` is set correctly in Jenkinsfile
2. ✅ Check build console for email sending errors
3. ✅ Ensure Email Extension Plugin is installed and enabled
4. ✅ Check if email notifications are enabled in post-build actions

### Issue: "SSL/TLS errors"

**Solutions:**
1. ✅ For port 587: Use TLS (not SSL)
2. ✅ For port 465: Use SSL (not TLS)
3. ✅ Try switching between ports if one doesn't work
4. ✅ Check if your network blocks these ports

---

## Alternative: Using Gmail (if Yahoo doesn't work)

If you prefer to use Gmail instead:

### Gmail SMTP Settings:
```
SMTP server: smtp.gmail.com
SMTP Port: 587 (TLS) or 465 (SSL)
Username: your-email@gmail.com
Password: Gmail App Password (generate from Google Account)
Use TLS: ✓ (for port 587)
Use SSL: ✓ (for port 465)
```

### Generate Gmail App Password:
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate App Password
4. Use the 16-character password in Jenkins

---

## Quick Configuration Checklist

- [ ] Email Extension Plugin installed
- [ ] Yahoo 2-Step Verification enabled
- [ ] Yahoo App Password generated
- [ ] SMTP server: `smtp.mail.yahoo.com`
- [ ] SMTP Port: `587` (TLS) or `465` (SSL)
- [ ] Username: `groklord@yahoo.com`
- [ ] Password: Yahoo App Password (16 characters)
- [ ] TLS checked (for port 587)
- [ ] Test email sent successfully
- [ ] Email received in inbox
- [ ] Configuration saved

---

## Email Notification Examples

### Success Email:
```
Subject: groklord-fullstack - Build #42 - SUCCESS!

✅ Build completed successfully!
Job: groklord-fullstack
Build Number: 42
Status: SUCCESS
Branch: main
```

### Failure Email:
```
Subject: groklord-fullstack - Build #43 - FAILURE!

❌ Build failed!
Job: groklord-fullstack
Build Number: 43
Status: FAILURE
Branch: main
View Console: [Link]
```

### Test Failure Email:
```
Subject: ❌ Backend Tests FAILED: groklord-fullstack - Build #44

Backend unit tests have failed.
Check the build console for detailed error information.
```

---

## Advanced Configuration (Optional)

### Custom Email Templates

You can customize email templates in:
- **Manage Jenkins** → **Configure System** → **Extended E-mail Notification**
- Click **Advanced** to customize default subject and content

### Multiple Recipients

To send to multiple recipients, modify the Jenkinsfile:
```groovy
environment {
    EMAIL_RECIPIENT = 'groklord@yahoo.com,another@email.com'
}
```

### Conditional Email Notifications

The pipeline already includes conditional email notifications for:
- Test failures
- Build failures
- SonarQube quality gate failures
- Unstable builds

---

## Security Best Practices

1. ✅ **Never commit app passwords** to git
2. ✅ **Use App Passwords** instead of regular passwords
3. ✅ **Store credentials securely** in Jenkins credentials store
4. ✅ **Rotate app passwords** periodically
5. ✅ **Use TLS/SSL** for encrypted email transmission

---

## Verification Steps

After configuration, verify everything works:

1. **Test Configuration**:
   - Send test email from Jenkins UI
   - Verify email received

2. **Run Test Build**:
   - Trigger a build that will fail (or succeed)
   - Check email notifications are sent

3. **Check Email Content**:
   - Verify HTML formatting works
   - Check links to build console work
   - Verify attachments (if configured) are included

---

## Support

If you encounter issues:

1. Check Jenkins logs: `/var/log/jenkins/jenkins.log`
2. Check build console output for email errors
3. Verify Yahoo account settings
4. Test SMTP connection manually:
   ```bash
   telnet smtp.mail.yahoo.com 587
   ```

---

**Configuration Complete!** 🎉

Your Jenkins pipeline will now send email notifications to `groklord@yahoo.com` for all build events.

