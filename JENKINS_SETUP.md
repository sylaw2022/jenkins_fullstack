# Jenkins Setup Guide for GROKLORD Fullstack Application

Complete step-by-step guide to set up Jenkins CI/CD for this project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Jenkins Installation](#jenkins-installation)
3. [Initial Jenkins Configuration](#initial-jenkins-configuration)
4. [Install Required Plugins](#install-required-plugins)
5. [Configure System Tools](#configure-system-tools)
6. [Configure Email Notifications](#configure-email-notifications)
7. [Create Jenkins Pipeline Job](#create-jenkins-pipeline-job)
8. [Configure Repository Access](#configure-repository-access)
9. [Optional: SonarQube Integration](#optional-sonarqube-integration)
10. [Run Your First Build](#run-your-first-build)
11. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu/Debian recommended)
- **Java**: OpenJDK 17 or higher
- **Node.js**: Version 18 (will be installed via Jenkins)
- **Git**: Installed and configured
- **Memory**: At least 4GB RAM recommended
- **Disk Space**: At least 10GB free

### Software to Install

```bash
# Update system
sudo apt-get update

# Install Java (if not already installed)
sudo apt-get install -y openjdk-17-jdk

# Install Git (if not already installed)
sudo apt-get install -y git

# Verify installations
java -version
git --version
```

---

## Jenkins Installation

### Step 1: Install Jenkins

```bash
# Add Jenkins repository key
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# Add Jenkins repository
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Update package list
sudo apt-get update

# Install Jenkins
sudo apt-get install -y jenkins

# Start Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Check status
sudo systemctl status jenkins
```

### Step 2: Configure Jenkins Port (if needed)

If port 8080 is already in use (e.g., by git server), change Jenkins port:

```bash
# Edit Jenkins configuration
sudo nano /etc/default/jenkins

# Change HTTP_PORT=8080 to HTTP_PORT=8081
# Save and exit (Ctrl+X, Y, Enter)

# Also update systemd service
sudo mkdir -p /etc/systemd/system/jenkins.service.d/
sudo tee /etc/systemd/system/jenkins.service.d/override.conf <<EOF
[Service]
Environment="JENKINS_PORT=8081"
EOF

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart jenkins
```

### Step 3: Access Jenkins Web Interface

1. **Open browser** and navigate to:
   - `http://localhost:8080` (default)
   - `http://localhost:8081` (if you changed the port)
   - Or `http://your-server-ip:8080`

2. **Get initial admin password**:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```

3. **Copy the password** and paste it into the Jenkins unlock page

4. **Install suggested plugins** (recommended)

5. **Create admin user**:
   - Username: `admin` (or your choice)
   - Password: (choose a strong password)
   - Full name: Your Name
   - Email: `groklord@yahoo.com`

6. **Save and finish**

---

## Initial Jenkins Configuration

### Step 1: Configure Global Settings

1. Go to **Manage Jenkins** → **Configure System**

2. **Configure Jenkins URL**:
   - Jenkins URL: `http://localhost:8080` (or your server IP/domain)

3. **Number of executors**: Set to 2-4 (depending on your system)

4. Click **Save**

### Step 2: Configure Security

1. Go to **Manage Jenkins** → **Configure Global Security**

2. **Enable security** (if not already enabled)

3. **Authorization**: Choose "Matrix-based security" or "Logged-in users can do anything"

4. **CSRF Protection**: Enable

5. Click **Save**

---

## Install Required Plugins

### Step 1: Install Plugins via Plugin Manager

1. Go to **Manage Jenkins** → **Manage Plugins**

2. Click on **Available** tab

3. Search and install the following plugins:

   **Essential Plugins:**
   - ✅ **Pipeline** (usually pre-installed)
   - ✅ **Git** (usually pre-installed)
   - ✅ **NodeJS Plugin** (for Node.js support)
   - ✅ **Email Extension Plugin** (for email notifications)
   - ✅ **HTML Publisher Plugin** (for test reports)
   - ✅ **JUnit Plugin** (for test results)
   - ✅ **Cobertura Plugin** (for code coverage)

   **Optional but Recommended:**
   - ✅ **SonarQube Scanner** (for code quality analysis)
   - ✅ **Blue Ocean** (modern UI for pipelines)
   - ✅ **Workspace Cleanup Plugin** (clean workspace after build)

4. Click **Install without restart** or **Download now and install after restart**

5. **Restart Jenkins** when prompted:
   ```bash
   sudo systemctl restart jenkins
   ```

### Step 2: Verify Plugin Installation

1. Go to **Manage Jenkins** → **Manage Plugins** → **Installed** tab
2. Verify all plugins are installed and enabled

---

## Configure System Tools

### Step 1: Configure Node.js

1. Go to **Manage Jenkins** → **Global Tool Configuration**

2. Scroll to **NodeJS** section

3. Click **Add NodeJS**

4. Configure:
   - **Name**: `NodeJS-18`
   - **Version**: Select `18.x` (or latest LTS)
   - **Global npm packages**: (leave empty or add: `newman` for API testing)

5. Click **Save**

### Step 2: Configure Git (if needed)

1. In **Global Tool Configuration**, scroll to **Git**

2. Ensure Git is configured:
   - **Name**: `Default`
   - **Path to Git executable**: `/usr/bin/git` (or auto-detect)

3. Click **Save**

---

## Configure Email Notifications

### Step 1: Configure SMTP Server

1. Go to **Manage Jenkins** → **Configure System**

2. Scroll to **Extended E-mail Notification** section

3. Configure SMTP settings:
   - **SMTP server**: 
     - For Gmail: `smtp.gmail.com`
     - For Yahoo: `smtp.mail.yahoo.com`
     - For Outlook: `smtp-mail.outlook.com`
   - **SMTP Port**: `587` (TLS) or `465` (SSL)
   - **Use SSL**: Check if using port 465
   - **Use TLS**: Check if using port 587
   - **Username**: Your email address
   - **Password**: Your email app password (not regular password)
   - **Default user e-mail suffix**: `@yahoo.com` (optional)

4. **Test configuration**:
   - Click **Test configuration by sending test e-mail**
   - Enter recipient: `groklord@yahoo.com`
   - Click **Test**

5. Scroll to **E-mail Notification** section (default):
   - Configure similar settings for basic email notifications

6. Click **Save**

### Step 2: Email App Password (for Gmail/Yahoo)

**For Gmail:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Generate App Password
4. Use the app password in Jenkins

**For Yahoo:**
1. Go to Account Security → Generate app password
2. Use the app password in Jenkins

---

## Create Jenkins Pipeline Job

### Step 1: Create New Pipeline Job

1. Click **New Item** on Jenkins dashboard

2. Enter item name: `groklord-fullstack` (or your preferred name)

3. Select **Pipeline**

4. Click **OK**

### Step 2: Configure Pipeline

1. **General Settings**:
   - **Description**: "GROKLORD Fullstack Application CI/CD Pipeline"
   - **GitHub project**: (optional) Add your GitHub repository URL

2. **Build Triggers** (optional):
   - **Poll SCM**: `H/5 * * * *` (check every 5 minutes)
   - **GitHub hook trigger**: (if using webhooks)

3. **Pipeline Definition**:
   - Select **Pipeline script from SCM**
   - **SCM**: Git
   - **Repository URL**: 
     - For GitHub: `https://github.com/sylaw2022/jenkins_fullstack.git`
     - For local: `/home/sylaw/git/repositories/jenkins_fullstack.git`
   - **Credentials**: (if repository is private, add credentials)
   - **Branches to build**: `*/main` (or your default branch)
   - **Script Path**: `Jenkinsfile`
   - **Lightweight checkout**: Uncheck (needed for full workspace)

4. Click **Save**

---

## Configure Repository Access

### Option 1: Public Repository (GitHub)

If your repository is public, no credentials needed. Just use the HTTPS URL.

### Option 2: Private Repository or Local Git

1. Go to **Manage Jenkins** → **Manage Credentials**

2. Click **System** → **Global credentials** → **Add Credentials**

3. For **GitHub**:
   - **Kind**: Username with password
   - **Username**: Your GitHub username
   - **Password**: Your GitHub Personal Access Token
   - **ID**: `github-credentials` (optional)
   - **Description**: "GitHub Access Token"

4. For **Local Git Repository**:
   - No credentials needed if Jenkins user has read access
   - Ensure Jenkins user can access the repository:
     ```bash
     sudo usermod -a -G $(stat -c '%G' /home/sylaw/git/repositories) jenkins
     ```

5. Click **OK**

6. In pipeline configuration, select the credentials from dropdown

---

## Optional: SonarQube Integration

### Step 1: Install SonarQube Server

(Follow SonarQube installation guide if not already installed)

### Step 2: Configure SonarQube in Jenkins

1. Go to **Manage Jenkins** → **Configure System**

2. Scroll to **SonarQube servers** section

3. Click **Add SonarQube**

4. Configure:
   - **Name**: `SonarQube`
   - **Server URL**: `http://localhost:9000` (or your SonarQube URL)
   - **Server authentication token**: Add your SonarQube token

5. Click **Save**

### Step 3: Configure SonarQube Scanner

1. Go to **Manage Jenkins** → **Global Tool Configuration**

2. Scroll to **SonarQube Scanner** section

3. Click **Add SonarQube Scanner**

4. Configure:
   - **Name**: `SonarQube Scanner`
   - **Version**: Latest

5. Click **Save**

### Step 4: Add SonarQube Credentials (Optional)

1. Go to **Manage Jenkins** → **Manage Credentials**

2. Add credentials:
   - **Kind**: Secret text
   - **Secret**: Your SonarQube token
   - **ID**: `sonar-token`
   - **Description**: "SonarQube Authentication Token"

---

## Run Your First Build

### Step 1: Trigger Build

1. Go to your pipeline job: `groklord-fullstack`

2. Click **Build Now**

3. Watch the build progress in **Build History**

4. Click on the build number to see console output

### Step 2: View Results

1. **Console Output**: See detailed build logs

2. **Test Results**: View test results (if tests ran)

3. **Coverage Report**: View code coverage (if configured)

4. **Artifacts**: Download build artifacts

5. **Email Notification**: Check your email for build status

### Step 3: Verify Pipeline Stages

Your pipeline includes these stages:

1. ✅ **Checkout** - Clones repository
2. ✅ **Install Dependencies** - Installs npm packages
3. ✅ **Test** - Runs unit tests
4. ✅ **Build** - Builds frontend
5. ✅ **API Tests** - Runs Postman/Newman tests
6. ✅ **E2E Tests** - Runs Cypress tests
7. ✅ **SonarQube Analysis** - Code quality check (optional)
8. ✅ **Archive Artifacts** - Saves build outputs

---

## Pipeline Configuration Details

### Environment Variables

The pipeline uses these environment variables (configured in Jenkinsfile):

- `NODE_VERSION`: '18'
- `BACKEND_DIR`: 'backend'
- `FRONTEND_DIR`: 'frontend'
- `EMAIL_RECIPIENT`: 'groklord@yahoo.com'

### Email Notifications

The pipeline sends emails for:
- ❌ Build failures
- ⚠️ Unstable builds
- 🛑 Aborted builds
- ❌ Test failures
- ⚠️ SonarQube quality gate failures

### Test Execution

- **Backend Tests**: Jest (if configured)
- **Frontend Tests**: Jest + React Testing Library
- **API Tests**: Postman/Newman
- **E2E Tests**: Cypress

---

## Troubleshooting

### Issue: Jenkins won't start

**Solution:**
```bash
# Check status
sudo systemctl status jenkins

# Check logs
sudo journalctl -u jenkins.service -n 100

# Check port conflict
lsof -i :8080
lsof -i :8081

# Fix port if needed (see Installation section)
```

### Issue: Build fails at "Checkout" stage

**Solutions:**
- Verify repository URL is correct
- Check credentials if repository is private
- Ensure Jenkins user has access to local repository
- Check Git is installed: `which git`

### Issue: Node.js not found

**Solutions:**
- Install NodeJS plugin
- Configure Node.js in Global Tool Configuration
- Ensure Node.js version matches NODE_VERSION in Jenkinsfile

### Issue: Email notifications not working

**Solutions:**
- Verify SMTP settings
- Check email app password (not regular password)
- Test email configuration
- Check Jenkins logs for email errors

### Issue: Tests failing

**Solutions:**
- Check test files exist
- Verify npm packages are installed
- Check test configuration
- Review test output in console

### Issue: SonarQube analysis fails

**Solutions:**
- Verify SonarQube server is running
- Check SonarQube URL and token
- Ensure SonarQube Scanner is configured
- Check `sonar-project.properties` file exists

### Issue: Permission denied errors

**Solutions:**
```bash
# Add Jenkins user to necessary groups
sudo usermod -a -G docker jenkins  # if using Docker
sudo usermod -a -G $(stat -c '%G' /path/to/repo) jenkins

# Fix directory permissions
sudo chown -R jenkins:jenkins /var/lib/jenkins
```

---

## Quick Reference Commands

### Jenkins Service Management

```bash
# Start Jenkins
sudo systemctl start jenkins

# Stop Jenkins
sudo systemctl stop jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# Check status
sudo systemctl status jenkins

# View logs
sudo journalctl -u jenkins.service -f
```

### Access Jenkins

- **Web Interface**: `http://localhost:8080` (or 8081)
- **Admin Password**: `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`
- **Jenkins Home**: `/var/lib/jenkins`
- **Logs**: `/var/log/jenkins/jenkins.log`

### Useful Jenkins URLs

- Dashboard: `http://localhost:8080`
- Manage Jenkins: `http://localhost:8080/manage`
- Plugin Manager: `http://localhost:8080/pluginManager`
- System Configuration: `http://localhost:8080/configure`
- Global Tool Configuration: `http://localhost:8080/configureTools`

---

## Next Steps

After successful setup:

1. ✅ **Run your first build** and verify all stages pass
2. ✅ **Check email notifications** are working
3. ✅ **Review test results** and coverage reports
4. ✅ **Configure webhooks** (optional) for automatic builds on git push
5. ✅ **Set up branch strategies** if using multiple branches
6. ✅ **Configure deployment** stages (if needed)

---

## Support

For issues or questions:

1. Check Jenkins logs: `/var/log/jenkins/jenkins.log`
2. Review build console output
3. Check this guide's troubleshooting section
4. Review project README.md

---

**Happy Building! 🚀**

