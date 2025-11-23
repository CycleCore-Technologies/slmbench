#!/bin/bash
###############################################################################
# HuggingFace Login and Upload Script
# CycleCore Maaza Models v1.0.0
###############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print header
echo -e "\n${BOLD}${CYAN}======================================================================${NC}"
echo -e "${BOLD}${CYAN}🚀 CycleCore Maaza Models - HuggingFace Upload${NC}"
echo -e "${BOLD}${CYAN}======================================================================${NC}\n"

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  HF_TOKEN environment variable not set${NC}"
    echo -e "\n${BOLD}To use this script:${NC}"
    echo -e "1. Get your token from: ${BLUE}https://huggingface.co/settings/tokens${NC}"
    echo -e "2. Run: ${CYAN}export HF_TOKEN='your_token_here'${NC}"
    echo -e "3. Run: ${CYAN}bash $0${NC}"
    echo -e "\n${BOLD}Or run in one line:${NC}"
    echo -e "${CYAN}HF_TOKEN='your_token_here' bash $0${NC}\n"
    exit 1
fi

# Login to HuggingFace
echo -e "${BOLD}Step 1: Authenticating with HuggingFace...${NC}"
echo "$HF_TOKEN" | hf auth login --token "$HF_TOKEN" --add-to-git-credential 2>/dev/null || {
    # Fallback: write token to file directly
    mkdir -p ~/.cache/huggingface
    echo "$HF_TOKEN" > ~/.cache/huggingface/token
}

# Verify authentication
echo -e "${BLUE}Verifying authentication...${NC}"
USER_INFO=$(hf auth whoami 2>&1)
if echo "$USER_INFO" | grep -q "Not logged in"; then
    echo -e "${RED}❌ Authentication failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Authenticated successfully!${NC}"
echo -e "${BLUE}$USER_INFO${NC}\n"

# Run upload script
echo -e "${BOLD}Step 2: Uploading models...${NC}"
echo -e "${CYAN}──────────────────────────────────────────────────────────────────────${NC}\n"

python3 /home/rain/SLMBench/scripts/upload_to_huggingface.py

echo -e "\n${BOLD}${GREEN}🎉 Upload process complete!${NC}"
echo -e "\n${BOLD}Next steps:${NC}"
echo -e "1. Upload logo to CycleCore org: ${CYAN}/home/rain/SLMBench/assets/logos/cyclecore-logo-400x400.png${NC}"
echo -e "2. Verify models at: ${BLUE}https://huggingface.co/CycleCore${NC}"
echo -e "3. Update README.md with HuggingFace links\n"

