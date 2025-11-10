#!/bin/bash
# Simple script to expose git repositories using git-daemon and ngrok

GIT_REPO_DIR="/home/sylaw/git/repositories"
GIT_DAEMON_PORT=9418

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Git Repository ngrok Exposer (Simple - git-daemon) ===${NC}\n"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}Error: ngrok is not installed${NC}"
    echo "Please install ngrok first:"
    echo "  snap install ngrok"
    echo "  Or visit: https://ngrok.com/download"
    exit 1
fi

# Check if git repository directory exists
if [ ! -d "$GIT_REPO_DIR" ]; then
    echo -e "${RED}Error: Git repository directory not found: $GIT_REPO_DIR${NC}"
    exit 1
fi

# Check if port is already in use
if lsof -Pi :$GIT_DAEMON_PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Warning: Port $GIT_DAEMON_PORT is already in use${NC}"
    echo "Killing existing process..."
    kill $(lsof -t -i:$GIT_DAEMON_PORT) 2>/dev/null
    sleep 2
fi

# Start git-daemon
echo -e "${GREEN}Starting git-daemon on port $GIT_DAEMON_PORT...${NC}"
git daemon --reuseaddr --base-path="$GIT_REPO_DIR" --export-all --verbose --enable=receive-pack "$GIT_REPO_DIR" > /tmp/git-daemon.log 2>&1 &
GIT_DAEMON_PID=$!

# Wait for daemon to start
sleep 2

# Check if daemon started successfully
if ! kill -0 $GIT_DAEMON_PID 2>/dev/null; then
    echo -e "${RED}Error: Failed to start git-daemon${NC}"
    echo "Check logs: cat /tmp/git-daemon.log"
    exit 1
fi

echo -e "${GREEN}Git daemon started (PID: $GIT_DAEMON_PID)${NC}"
echo -e "${YELLOW}Note: git-daemon allows read/write access. Use with caution!${NC}"

# Start ngrok
echo -e "${GREEN}Starting ngrok tunnel...${NC}"
echo -e "${YELLOW}Note: If this is your first time, you may need to:${NC}"
echo -e "${YELLOW}  1. Sign up at https://dashboard.ngrok.com${NC}"
echo -e "${YELLOW}  2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken${NC}"
echo -e "${YELLOW}  3. Run: ngrok config add-authtoken YOUR_TOKEN${NC}"
echo ""

# Start ngrok in foreground
ngrok tcp $GIT_DAEMON_PORT

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    kill $GIT_DAEMON_PID 2>/dev/null
    pkill -f "ngrok tcp" 2>/dev/null
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Trap Ctrl+C
trap cleanup EXIT INT TERM

