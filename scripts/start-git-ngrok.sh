#!/bin/bash
# Script to expose local git repositories to internet using ngrok

GIT_REPO_DIR="/home/sylaw/git/repositories"
GIT_SERVER_PORT=8080
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_SERVER_SCRIPT="$SCRIPT_DIR/git-server.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Git Repository ngrok Exposer ===${NC}\n"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}Error: ngrok is not installed${NC}"
    echo "Installing ngrok..."
    
    # Try to install ngrok
    if command -v snap &> /dev/null; then
        echo "Installing ngrok via snap..."
        sudo snap install ngrok
    elif command -v curl &> /dev/null; then
        echo "Downloading ngrok..."
        NGROK_VERSION="3.3.1"
        ARCH=$(uname -m)
        if [ "$ARCH" = "x86_64" ]; then
            NGROK_ARCH="amd64"
        elif [ "$ARCH" = "aarch64" ]; then
            NGROK_ARCH="arm64"
        else
            echo -e "${RED}Unsupported architecture: $ARCH${NC}"
            exit 1
        fi
        
        NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v${NGROK_VERSION}-linux-${NGROK_ARCH}.tgz"
        curl -L "$NGROK_URL" -o /tmp/ngrok.tgz
        tar -xzf /tmp/ngrok.tgz -C /tmp
        sudo mv /tmp/ngrok /usr/local/bin/
        rm /tmp/ngrok.tgz
        echo -e "${GREEN}ngrok installed successfully${NC}"
    else
        echo -e "${RED}Please install ngrok manually:${NC}"
        echo "  Visit: https://ngrok.com/download"
        echo "  Or use: snap install ngrok"
        exit 1
    fi
fi

# Check if git repository directory exists
if [ ! -d "$GIT_REPO_DIR" ]; then
    echo -e "${RED}Error: Git repository directory not found: $GIT_REPO_DIR${NC}"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Make git-server.py executable
chmod +x "$GIT_SERVER_SCRIPT"

# Check if git-http-backend exists
if [ ! -f "/usr/lib/git-core/git-http-backend" ]; then
    echo -e "${RED}Error: git-http-backend not found${NC}"
    echo "Please install git: sudo apt-get install git"
    exit 1
fi

# Check if port is already in use
if lsof -Pi :$GIT_SERVER_PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Warning: Port $GIT_SERVER_PORT is already in use${NC}"
    echo "Killing existing process..."
    kill $(lsof -t -i:$GIT_SERVER_PORT) 2>/dev/null
    sleep 2
fi

# Start git HTTP server in background
echo -e "${GREEN}Starting git HTTP server on port $GIT_SERVER_PORT...${NC}"
python3 "$GIT_SERVER_SCRIPT" > /tmp/git-server.log 2>&1 &
GIT_SERVER_PID=$!

# Wait for server to start
sleep 2

# Check if server started successfully
if ! kill -0 $GIT_SERVER_PID 2>/dev/null; then
    echo -e "${RED}Error: Failed to start git HTTP server${NC}"
    echo "Check logs: cat /tmp/git-server.log"
    exit 1
fi

echo -e "${GREEN}Git HTTP server started (PID: $GIT_SERVER_PID)${NC}"

# Start ngrok
echo -e "${GREEN}Starting ngrok tunnel...${NC}"
echo -e "${YELLOW}Note: If this is your first time, you may need to:${NC}"
echo -e "${YELLOW}  1. Sign up at https://dashboard.ngrok.com${NC}"
echo -e "${YELLOW}  2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken${NC}"
echo -e "${YELLOW}  3. Run: ngrok config add-authtoken YOUR_TOKEN${NC}"
echo ""

# Start ngrok in foreground (user can see the URL)
ngrok http $GIT_SERVER_PORT

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    kill $GIT_SERVER_PID 2>/dev/null
    pkill -f "ngrok http" 2>/dev/null
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Trap Ctrl+C
trap cleanup EXIT INT TERM

