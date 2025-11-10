#!/bin/bash
# Script to push repository to GitHub

REPO_NAME="jenkins_fullstack"
GITHUB_USER="groklord"
GITHUB_EMAIL="groklord@yahoo.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Push to GitHub ===${NC}\n"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Check if GitHub token is provided
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}GitHub Personal Access Token not found in environment${NC}"
    echo ""
    echo "GitHub no longer accepts passwords for authentication."
    echo "You need to create a Personal Access Token:"
    echo ""
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Click 'Generate new token' -> 'Generate new token (classic)'"
    echo "3. Give it a name (e.g., 'jenkins_fullstack_push')"
    echo "4. Select scopes: repo (all)"
    echo "5. Click 'Generate token'"
    echo "6. Copy the token"
    echo ""
    echo "Then run:"
    echo "  export GITHUB_TOKEN=your_token_here"
    echo "  ./scripts/push-to-github.sh"
    echo ""
    read -p "Do you want to continue with manual token entry? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    read -sp "Enter your GitHub Personal Access Token: " GITHUB_TOKEN
    echo
fi

# Configure git user if not already set
if [ -z "$(git config user.name)" ]; then
    git config user.name "$GITHUB_USER"
fi
if [ -z "$(git config user.email)" ]; then
    git config user.email "$GITHUB_EMAIL"
fi

# Check if GitHub remote exists
if git remote get-url github >/dev/null 2>&1; then
    echo -e "${GREEN}GitHub remote already configured${NC}"
    GITHUB_URL=$(git remote get-url github)
else
    # Create repository on GitHub
    echo -e "${YELLOW}Creating repository on GitHub...${NC}"
    
    # Check if repository already exists
    REPO_EXISTS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_USER/$REPO_NAME" | grep -q '"name"' && echo "yes" || echo "no")
    
    if [ "$REPO_EXISTS" = "no" ]; then
        echo "Creating new repository: $GITHUB_USER/$REPO_NAME"
        CREATE_RESPONSE=$(curl -s -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/user/repos" \
            -d "{\"name\":\"$REPO_NAME\",\"private\":false,\"description\":\"Jenkins Fullstack Application with CI/CD\"}")
        
        if echo "$CREATE_RESPONSE" | grep -q '"name"'; then
            echo -e "${GREEN}Repository created successfully${NC}"
        else
            echo -e "${RED}Error creating repository:${NC}"
            echo "$CREATE_RESPONSE" | grep -o '"message":"[^"]*"' || echo "$CREATE_RESPONSE"
            exit 1
        fi
    else
        echo -e "${GREEN}Repository already exists on GitHub${NC}"
    fi
    
    # Add GitHub remote
    GITHUB_URL="https://$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
    git remote add github "$GITHUB_URL" 2>/dev/null || git remote set-url github "$GITHUB_URL"
    echo -e "${GREEN}GitHub remote configured${NC}"
fi

# Push to GitHub
echo -e "${YELLOW}Pushing to GitHub...${NC}"
if git push -u github main; then
    echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
    echo ""
    echo "Repository URL: https://github.com/$GITHUB_USER/$REPO_NAME"
else
    echo -e "${RED}Error pushing to GitHub${NC}"
    exit 1
fi

