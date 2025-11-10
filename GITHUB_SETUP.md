# Push to GitHub Setup Guide

This guide explains how to push the jenkins_fullstack application to GitHub.

## Important: GitHub Authentication

**GitHub no longer accepts passwords for Git operations.** You must use a **Personal Access Token** instead.

## Step 1: Create a GitHub Personal Access Token

1. **Go to GitHub Settings**:
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**:
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a descriptive name: `jenkins_fullstack_push`
   - Set expiration (recommended: 90 days or custom)
   - Select scopes:
     - ✅ **repo** (all) - This gives full control of private repositories
     - Or at minimum: `repo:status`, `repo_deployment`, `public_repo`

3. **Generate and Copy Token**:
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again!)
   - It will look like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Push to GitHub

### Option A: Using the Script (Recommended)

```bash
cd /home/sylaw/jenkins_fullstack

# Set your GitHub token
export GITHUB_TOKEN=your_token_here

# Run the push script
./scripts/push-to-github.sh
```

The script will:
- Create the repository on GitHub (if it doesn't exist)
- Configure the GitHub remote
- Push all commits to GitHub

### Option B: Manual Setup

```bash
cd /home/sylaw/jenkins_fullstack

# Configure git (if not already done)
git config user.name "groklord"
git config user.email "groklord@yahoo.com"

# Create repository on GitHub first (via web interface or API)
# Then add remote:
git remote add github https://YOUR_TOKEN@github.com/groklord/jenkins_fullstack.git

# Or use token in URL:
git remote add github https://ghp_xxxxxxxxxxxx@github.com/groklord/jenkins_fullstack.git

# Push to GitHub
git push -u github main
```

### Option C: Using GitHub CLI (if installed)

```bash
# Install GitHub CLI (if not installed)
# Ubuntu/Debian:
sudo apt install gh

# Authenticate
gh auth login

# Create repository and push
gh repo create jenkins_fullstack --public --source=. --remote=github --push
```

## Step 3: Verify

After pushing, verify your repository is on GitHub:
- Visit: https://github.com/groklord/jenkins_fullstack
- You should see all your files and commit history

## Using with Render.com

Once your repository is on GitHub, you can:

1. **Connect to Render.com**:
   - Go to Render.com dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select the `jenkins_fullstack` repository
   - Render will automatically detect `render.yaml` and deploy

2. **Update Repository URL**:
   - Your `render.yaml` will work automatically
   - Render.com will pull from GitHub on every push

## Security Notes

⚠️ **Important Security Practices**:

1. **Never commit tokens to git**:
   - Add `.env` files to `.gitignore`
   - Use environment variables in Render.com

2. **Token Storage**:
   - Don't hardcode tokens in scripts
   - Use environment variables: `export GITHUB_TOKEN=...`
   - Consider using a password manager for tokens

3. **Token Permissions**:
   - Use the minimum required permissions
   - Revoke tokens if compromised
   - Set expiration dates

4. **Repository Visibility**:
   - Public repositories are visible to everyone
   - Private repositories require authentication

## Troubleshooting

### Error: "remote: Invalid username or password"

**Solution**: You're using a password. Switch to a Personal Access Token.

### Error: "Repository not found"

**Solution**: 
- Make sure the repository exists on GitHub
- Check the repository name matches
- Verify your token has `repo` permissions

### Error: "Permission denied"

**Solution**:
- Verify your token has the correct permissions
- Check if the token has expired
- Regenerate the token if needed

### Error: "Repository already exists"

**Solution**: The repository already exists. You can:
- Delete it on GitHub and recreate
- Or just add the remote and push

## Next Steps

After pushing to GitHub:

1. ✅ **Connect to Render.com** for automatic deployments
2. ✅ **Set up GitHub Actions** for CI/CD (optional)
3. ✅ **Add collaborators** if working in a team
4. ✅ **Configure branch protection** rules
5. ✅ **Set up webhooks** for Jenkins (if using)

---

**Repository URL**: https://github.com/groklord/jenkins_fullstack

