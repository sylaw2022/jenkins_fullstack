# Jenkins Pipeline Credentials Configuration

This document provides the exact credential information you need to configure your Jenkins pipeline for this project.

## How to Get Your GitHub Personal Access Token

If you need to retrieve your GitHub Personal Access Token:

1. **From your local git config** (if already configured):
   ```bash
   git config --get remote.github.url | grep -o 'ghp_[^@]*'
   ```

2. **Or create a new token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: `jenkins-fullstack`
   - Select scope: `repo` (all)
   - Click "Generate token"
   - Copy the token (starts with `ghp_`)

**Your current token** (stored locally): Check your git remote configuration or use the command above.

---

## Repository Information

### GitHub Repository (Recommended)
- **Repository URL**: `https://github.com/sylaw2022/jenkins_fullstack.git`
- **Repository Type**: Public (no credentials needed) OR Private (credentials required)
- **Default Branch**: `main`
- **GitHub Username**: `sylaw2022`

### Local Repository (Alternative)
- **Repository Path**: `/home/sylaw/git/repositories/jenkins_fullstack.git`
- **Repository Type**: Local bare repository
- **Default Branch**: `main`

---

## Option 1: Using GitHub Repository (Recommended)

### If Repository is PUBLIC:
**No credentials needed!** Just use:
- **Repository URL**: `https://github.com/sylaw2022/jenkins_fullstack.git`
- **Credentials**: Leave empty (None)

### If Repository is PRIVATE:
You need to add GitHub credentials in Jenkins:

#### Step 1: Create Credentials in Jenkins

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **System** → **Global credentials (unrestricted)** → **Add Credentials**
3. Fill in the form:
   - **Kind**: `Username with password`
   - **Username**: `sylaw2022`
   - **Password**: `YOUR_GITHUB_PERSONAL_ACCESS_TOKEN` (GitHub Personal Access Token - see below)
   - **ID**: `github-credentials` (optional, but recommended)
   - **Description**: `GitHub Access Token for jenkins_fullstack`
4. Click **OK**

#### Step 2: Use Credentials in Pipeline

In your pipeline configuration:
- **Repository URL**: `https://github.com/sylaw2022/jenkins_fullstack.git`
- **Credentials**: Select `github-credentials` (or the ID you used)

---

## Option 2: Using Local Repository

### No Credentials Needed (if permissions are correct)

1. **Repository URL**: `/home/sylaw/git/repositories/jenkins_fullstack.git`
2. **Credentials**: Leave empty (None)

### Ensure Jenkins User Has Access

Run this command to give Jenkins user access to the repository:

```bash
# Add Jenkins user to the repository group
sudo usermod -a -G $(stat -c '%G' /home/sylaw/git/repositories) jenkins

# Or set proper permissions
sudo chmod -R 755 /home/sylaw/git/repositories
sudo chown -R $(stat -c '%U:%G' /home/sylaw/git/repositories) /home/sylaw/git/repositories
```

---

## Complete Pipeline Configuration

### For GitHub Repository:

```
Pipeline Definition:
├── Pipeline script from SCM: ✓
├── SCM: Git
├── Repository URL: https://github.com/sylaw2022/jenkins_fullstack.git
├── Credentials: github-credentials (if private) OR None (if public)
├── Branches to build: */main
├── Script Path: Jenkinsfile
└── Lightweight checkout: ☐ (Unchecked)
```

### For Local Repository:

```
Pipeline Definition:
├── Pipeline script from SCM: ✓
├── SCM: Git
├── Repository URL: /home/sylaw/git/repositories/jenkins_fullstack.git
├── Credentials: None
├── Branches to build: */main
├── Script Path: Jenkinsfile
└── Lightweight checkout: ☐ (Unchecked)
```

---

## Credential Details Summary

### GitHub Personal Access Token
- **Token**: `YOUR_GITHUB_PERSONAL_ACCESS_TOKEN` (Get from: https://github.com/settings/tokens)
- **Username**: `sylaw2022`
- **Type**: Personal Access Token (classic)
- **Scopes**: `repo` (full repository access)

**Note**: Your actual token is stored securely in your local git config. To retrieve it:
```bash
git config --get remote.github.url | grep -o 'ghp_[^@]*'
```

### How to Use in Jenkins:

1. **Credential Type**: Username with password
2. **Username**: `sylaw2022`
3. **Password**: `YOUR_GITHUB_PERSONAL_ACCESS_TOKEN` (see instructions below)
4. **ID**: `github-credentials` (recommended for easy reference)

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Token Security**:
   - The GitHub token has full repository access
   - Keep it secure and don't share it publicly
   - If compromised, revoke it immediately at: https://github.com/settings/tokens

2. **Jenkins Credentials**:
   - Credentials are stored encrypted in Jenkins
   - Only users with proper permissions can view them
   - Use credential IDs for easy reference

3. **Best Practices**:
   - Use separate tokens for different purposes
   - Set token expiration dates
   - Regularly rotate tokens
   - Use minimal required permissions

---

## Troubleshooting

### Issue: "Repository not found" or "Authentication failed"

**Solutions:**
1. Verify the repository URL is correct
2. Check if credentials are selected (for private repos)
3. Verify the GitHub token is valid and not expired
4. Test the token manually:
   ```bash
   curl -H "Authorization: token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" \
        https://api.github.com/repos/sylaw2022/jenkins_fullstack
   ```

### Issue: "Permission denied" (Local Repository)

**Solutions:**
```bash
# Check permissions
ls -la /home/sylaw/git/repositories/jenkins_fullstack.git

# Fix permissions
sudo chmod -R 755 /home/sylaw/git/repositories
sudo chown -R jenkins:jenkins /home/sylaw/git/repositories

# Or add Jenkins to the group
sudo usermod -a -G $(stat -c '%G' /home/sylaw/git/repositories) jenkins
```

### Issue: "Branch not found"

**Solutions:**
- Verify the branch name is `main` (not `master`)
- Check: `git branch -a` to see available branches
- Update "Branches to build" to match your branch name

---

## Quick Setup Checklist

- [ ] Decide: GitHub (recommended) or Local repository
- [ ] If GitHub and private: Create credentials in Jenkins
- [ ] Configure pipeline with correct repository URL
- [ ] Select credentials (if needed)
- [ ] Set branch to `*/main`
- [ ] Set Script Path to `Jenkinsfile`
- [ ] Uncheck "Lightweight checkout"
- [ ] Save and test the pipeline

---

## Example: Creating Credentials in Jenkins UI

1. **Navigate**: Manage Jenkins → Manage Credentials
2. **Click**: System → Global credentials (unrestricted) → Add Credentials
3. **Fill Form**:
   ```
   Kind: Username with password
   Scope: Global
   Username: sylaw2022
   Password: YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
   ID: github-credentials
   Description: GitHub Access Token for jenkins_fullstack
   ```
4. **Click**: OK
5. **Use in Pipeline**: Select `github-credentials` from dropdown

---

**Note**: If your repository is public, you don't need any credentials. Just use the GitHub URL without selecting credentials.

