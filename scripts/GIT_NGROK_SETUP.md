# Exposing Git Repositories via ngrok

This guide explains how to expose your local git repositories at `/home/sylaw/git/repositories` to the internet using ngrok.

## Prerequisites

1. **ngrok account** (free tier is sufficient)
   - Sign up at [https://dashboard.ngrok.com](https://dashboard.ngrok.com)
   - Get your authtoken from [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

2. **Install ngrok** (if not already installed):
   ```bash
   # Using snap (recommended)
   sudo snap install ngrok
   
   # Or download manually from https://ngrok.com/download
   ```

3. **Configure ngrok authtoken**:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

## Method 1: HTTP Server (Recommended)

This method uses a Python HTTP server with git-http-backend, which is more secure and compatible with most git clients.

### Usage

```bash
cd /home/sylaw/jenkins_fullstack
./scripts/start-git-ngrok.sh
```

### How it works

1. Starts a Python HTTP server on port 8080 that uses `git-http-backend`
2. Exposes the server via ngrok HTTP tunnel
3. Provides a public URL that can be used to clone/push repositories

### Accessing Repositories

Once ngrok is running, you'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8080
```

You can then clone repositories using:
```bash
git clone https://abc123.ngrok-free.app/jenkins_fullstack.git
```

### Repository URLs

- **jenkins_fullstack**: `https://YOUR_NGROK_URL/jenkins_fullstack.git`
- **sylaw_repo**: `https://YOUR_NGROK_URL/sylaw_repo.git`
- **sylaw_repo1**: `https://YOUR_NGROK_URL/sylaw_repo1.git`

## Method 2: Git Daemon (Simple, Less Secure)

This method uses git-daemon, which is simpler but allows read/write access without authentication.

### Usage

```bash
cd /home/sylaw/jenkins_fullstack
./scripts/start-git-ngrok-simple.sh
```

### How it works

1. Starts `git-daemon` on port 9418 (git protocol)
2. Exposes the daemon via ngrok TCP tunnel
3. Provides a public URL for git:// protocol

### Accessing Repositories

Once ngrok is running, you'll see output like:
```
Forwarding  tcp://0.tcp.ngrok.io:12345 -> localhost:9418
```

You can then clone repositories using:
```bash
git clone git://0.tcp.ngrok.io:12345/jenkins_fullstack.git
```

**Note**: The port number (12345) will be different each time you start ngrok.

### Security Warning

⚠️ **git-daemon allows read/write access without authentication**. Only use this method in trusted environments or for temporary access.

## Stopping the Services

Press `Ctrl+C` in the terminal where the script is running. The cleanup function will automatically:
- Stop the git server/daemon
- Stop ngrok tunnel

## Troubleshooting

### ngrok not found
```bash
# Install ngrok
sudo snap install ngrok

# Or download from https://ngrok.com/download
```

### Port already in use
The scripts will automatically try to kill existing processes on the ports. If that fails:
```bash
# For HTTP server (port 8080)
lsof -ti:8080 | xargs kill -9

# For git-daemon (port 9418)
lsof -ti:9418 | xargs kill -9
```

### git-http-backend not found
```bash
# Install git
sudo apt-get install git
```

### Permission denied
```bash
# Make scripts executable
chmod +x scripts/start-git-ngrok.sh
chmod +x scripts/start-git-ngrok-simple.sh
chmod +x scripts/git-server.py
```

### ngrok authtoken error
```bash
# Configure authtoken
ngrok config add-authtoken YOUR_AUTHTOKEN
```

## Using with Render.com

Once your git repository is exposed via ngrok, you can use the ngrok URL in Render.com:

1. **Get the ngrok URL** from the script output
2. **In Render.com**, when connecting a repository:
   - Select "Other Git Provider" or "Public Git Repository"
   - Enter the ngrok URL (e.g., `https://abc123.ngrok-free.app/jenkins_fullstack.git`)

**Note**: The ngrok URL changes each time you restart ngrok (unless you have a paid plan with static domains). For production use, consider:
- Using a paid ngrok plan with static domains
- Pushing to GitHub/GitLab/Bitbucket instead
- Setting up a permanent git server

## Logs

- **Git HTTP Server logs**: `/tmp/git-server.log`
- **Git daemon logs**: `/tmp/git-daemon.log`
- **ngrok logs**: Check the ngrok web interface at `http://localhost:4040`

## Security Considerations

1. **Temporary Access**: ngrok free tier provides temporary URLs that change on restart
2. **No Authentication**: The current setup doesn't include authentication
3. **Public Access**: Anyone with the ngrok URL can access your repositories
4. **Read/Write Access**: Both methods allow push access

For production use, consider:
- Adding authentication (HTTP basic auth, SSH keys)
- Using HTTPS with certificates
- Restricting access to specific IPs
- Using a permanent hosting solution (GitHub, GitLab, etc.)

