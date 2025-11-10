# Fix: Cypress "spawn Xvfb ENOENT" Error

## Problem

When running Cypress E2E tests in Jenkins, you may encounter:
```
Error: spawn Xvfb ENOENT
```

This happens because Cypress needs a display server to run browsers in a headless environment, and Xvfb (X Virtual Framebuffer) is not installed.

## Solution

### Option 1: Install Xvfb (Recommended)

Install Xvfb and required dependencies:

```bash
sudo apt-get update
sudo apt-get install -y xvfb x11-utils x11-xserver-utils libx11-dev libxcomposite-dev libxdamage-dev libxext-dev libxfixes-dev libxrandr-dev libxrender-dev libxtst-dev libxss1 libgconf-2-4
```

Or use the provided script:
```bash
./scripts/install-xvfb.sh
```

### Option 2: Use Cypress Headless Mode (No Xvfb Required)

The Jenkinsfile has been updated to automatically fall back to Cypress headless mode if Xvfb is not available. This doesn't require Xvfb installation.

## How It Works Now

The updated Jenkinsfile will:

1. **Check if Xvfb is installed**
   - If yes: Start Xvfb and run Cypress with it
   - If no: Use Cypress `--headless` flag (no Xvfb needed)

2. **Automatic fallback**: If Xvfb is not found, Cypress will run in headless mode automatically

## Manual Testing

### Test with Xvfb:
```bash
# Start Xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1280x1024x24 &
XVFB_PID=$!

# Run Cypress
cd frontend
npx cypress run --e2e --browser electron

# Cleanup
kill $XVFB_PID
```

### Test without Xvfb (headless):
```bash
cd frontend
npx cypress run --e2e --browser electron --headless
```

## Jenkins Configuration

The Jenkinsfile now handles both scenarios:

- **With Xvfb**: Automatically starts Xvfb before running tests
- **Without Xvfb**: Falls back to `--headless` mode

No additional Jenkins configuration needed!

## Verify Installation

After installing Xvfb, verify it's working:

```bash
which Xvfb
Xvfb --help
```

## Additional Dependencies

If you still encounter issues, you may need additional packages:

```bash
sudo apt-get install -y \
    libgtk-3-0 \
    libgbm-dev \
    libnss3 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils
```

## Troubleshooting

### Error: "Cannot connect to X server"
- **Solution**: Make sure Xvfb is running before Cypress
- The Jenkinsfile now handles this automatically

### Error: "Display not found"
- **Solution**: Set `DISPLAY=:99` before running Cypress
- The Jenkinsfile now sets this automatically

### Cypress still fails after installing Xvfb
- **Solution**: The Jenkinsfile will automatically fall back to `--headless` mode
- This should work without Xvfb

## Summary

✅ **Fixed**: Jenkinsfile now automatically handles Xvfb setup or falls back to headless mode
✅ **No manual configuration needed**: Works with or without Xvfb
✅ **Install Xvfb for better compatibility**: Run `./scripts/install-xvfb.sh`

The error should no longer occur. If it does, the pipeline will automatically use headless mode as a fallback.

