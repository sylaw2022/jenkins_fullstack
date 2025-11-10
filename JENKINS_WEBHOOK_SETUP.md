# Jenkins Auto-Build Setup (GitHub Webhooks)

This guide explains how to configure Jenkins to automatically trigger builds when you push code to GitHub.

## Why Jenkins Didn't Auto-Build

Jenkins doesn't automatically build on Git push by default. You need to configure one of these options:

1. **GitHub Webhooks** (Recommended) - GitHub notifies Jenkins immediately when code is pushed
2. **Poll SCM** (Fallback) - Jenkins checks the repository periodically for changes

---

## Option 1: GitHub Webhooks (Recommended - Instant Triggers)

### Step 1: Install GitHub Plugin in Jenkins

1. Go to Jenkins dashboard: `http://localhost:8081`
2. Click **Manage Jenkins** → **Manage Plugins**
3. Go to **Available** tab
4. Search for: `GitHub plugin`
5. Check the box and click **Install without restart** (or **Download now and install after restart**)
6. Wait for installation to complete
7. Restart Jenkins if prompted:
   ```bash
   sudo systemctl restart jenkins
   ```

### Step 2: Configure Jenkins to Accept Webhooks

1. Go to **Manage Jenkins** → **Configure System**
2. Scroll to **GitHub** section
3. Click **Add GitHub Server**
4. Configure:
   - **Name**: `GitHub`
   - **API URL**: `https://api.github.com` (default)
   - **Credentials**: Click **Add** → **Jenkins**
     - **Kind**: `Secret text`
     - **Secret**: Your GitHub Personal Access Token (starts with `ghp_`)
     - **ID**: `github-token`
     - **Description**: `GitHub Personal Access Token`
     - Click **Add**
   - Select the credentials you just created
   - Check **Manage hooks** (allows Jenkins to automatically configure webhooks)
5. Click **Test connection** - should show "Credentials verified"
6. Click **Save**

### Step 3: Configure Your Pipeline Job

1. Go to your pipeline job (e.g., `groklord-fullstack`)
2. Click **Configure**
3. Scroll to **Build Triggers** section
4. Check **GitHub hook trigger for GITScm polling**
5. Click **Save**

### Step 4: Configure GitHub Webhook

1. Go to your GitHub repository: `https://github.com/sylaw2022/jenkins_fullstack`
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `http://YOUR_JENKINS_IP:8081/github-webhook/`
     - If Jenkins is on localhost: `http://localhost:8081/github-webhook/`
     - If Jenkins is accessible from internet: `http://YOUR_PUBLIC_IP:8081/github-webhook/`
     - **Note**: For localhost, you'll need to use a service like ngrok (see below)
   - **Content type**: `application/json`
   - **Secret**: (optional, leave empty for now)
   - **Which events**: Select **Just the push event**
   - **Active**: ✓ Checked
4. Click **Add webhook**

### Step 5: Test the Webhook

1. Make a small change to your repository:
   ```bash
   echo "# Test" >> README.md
   git add README.md
   git commit -m "Test webhook"
   git push github main
   ```

2. Check Jenkins:
   - Go to Jenkins dashboard
   - You should see a new build automatically triggered
   - Check the build console for "Started by GitHub push"

---

## Option 2: Poll SCM (Fallback - Periodic Checks)

If webhooks don't work (e.g., Jenkins is behind a firewall), use Poll SCM:

1. Go to your pipeline job → **Configure**
2. Scroll to **Build Triggers** section
3. Check **Poll SCM**
4. Enter schedule: `H/5 * * * *` (checks every 5 minutes)
   - Or `H/2 * * * *` (checks every 2 minutes)
   - Or `* * * * *` (checks every minute - not recommended)
5. Click **Save**

**Note**: Poll SCM is less efficient and has a delay (up to the poll interval).

---

## Option 3: Expose Jenkins via ngrok (For Local Jenkins)

If Jenkins is running locally and you want to use GitHub webhooks:

### Step 1: Install ngrok (if not already installed)

```bash
# Download ngrok
cd ~/bin
curl -O https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
chmod +x ngrok
```

### Step 2: Configure ngrok with authtoken

```bash
~/bin/ngrok config add-authtoken YOUR_NGROK_AUTHTOKEN
```

### Step 3: Start ngrok tunnel

```bash
# In a separate terminal
~/bin/ngrok http 8081
```

### Step 4: Get ngrok URL

The ngrok output will show:
```
Forwarding  https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8081
```

### Step 5: Configure GitHub Webhook

Use the ngrok HTTPS URL:
- **Payload URL**: `https://xxxx-xx-xx-xx-xx.ngrok-free.app/github-webhook/`

**Note**: ngrok free tier URLs change each time you restart ngrok. For production, use a static domain or keep ngrok running.

---

## Troubleshooting

### Webhook Not Triggering Builds

1. **Check Jenkins Logs**:
   ```bash
   sudo journalctl -u jenkins -f
   ```

2. **Check GitHub Webhook Delivery**:
   - Go to GitHub repository → **Settings** → **Webhooks**
   - Click on your webhook
   - Check **Recent Deliveries** tab
   - Look for errors (red X) or successful deliveries (green checkmark)

3. **Verify Jenkins is Accessible**:
   ```bash
   curl -I http://localhost:8081/github-webhook/
   # Should return 200 or 405 (Method Not Allowed is OK for GET)
   ```

4. **Check Pipeline Configuration**:
   - Ensure **GitHub hook trigger for GITScm polling** is checked
   - Ensure **Pipeline script from SCM** is selected
   - Ensure repository URL is correct

5. **Test Manually**:
   - Go to Jenkins → Your Job → **Build Now**
   - If manual build works, the issue is with webhook configuration

### Common Issues

**Issue**: "GitHub hook trigger for GITScm polling" option not visible
- **Solution**: Install **GitHub plugin** in Jenkins

**Issue**: Webhook shows "Failed to connect"
- **Solution**: 
  - Jenkins must be accessible from the internet (or use ngrok)
  - Check firewall settings
  - Verify Jenkins is running: `sudo systemctl status jenkins`

**Issue**: Webhook delivers but no build triggered
- **Solution**:
  - Check if **GitHub hook trigger** is enabled in job configuration
  - Check Jenkins logs for errors
  - Verify repository URL matches GitHub repository

---

## Quick Setup Script

Run this script to check your current configuration:

```bash
#!/bin/bash
echo "Checking Jenkins configuration..."

# Check if Jenkins is running
if systemctl is-active --quiet jenkins; then
    echo "✅ Jenkins is running"
else
    echo "❌ Jenkins is not running"
    echo "Start with: sudo systemctl start jenkins"
fi

# Check Jenkins port
echo "Jenkins URL: http://localhost:8081"

# Check if GitHub plugin might be installed
echo ""
echo "Next steps:"
echo "1. Go to http://localhost:8081"
echo "2. Manage Jenkins → Manage Plugins → Install 'GitHub plugin'"
echo "3. Configure your pipeline job → Build Triggers → Check 'GitHub hook trigger'"
echo "4. Add webhook in GitHub repository settings"
```

---

## Summary

**For automatic builds on push:**
1. ✅ Install GitHub plugin in Jenkins
2. ✅ Enable "GitHub hook trigger" in pipeline job
3. ✅ Add webhook in GitHub repository settings
4. ✅ Ensure Jenkins is accessible (or use ngrok for local)

**Alternative (if webhooks don't work):**
- Use **Poll SCM** with schedule `H/5 * * * *` (checks every 5 minutes)

