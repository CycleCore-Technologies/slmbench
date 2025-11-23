# Copyright 2025 CycleCore Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python3
"""
HuggingFace Authentication Wizard
==================================

Secure credential management for CycleCore Maaza model uploads.

Usage:
    python3 hf_auth_wizard.py
    
Features:
- Secure token input (hidden)
- Token validation
- Persistent storage in HF standard location
- Ready for model upload

Author: CycleCore Technologies
License: Apache 2.0
"""

import os
import sys
import getpass
from pathlib import Path
from huggingface_hub import HfApi, login

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print wizard header"""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}🚀 CycleCore Maaza Models - HuggingFace Authentication Wizard{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}{'='*70}{Colors.ENDC}\n")

def print_success(msg):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")

def print_error(msg):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    """Print info message"""
    print(f"{Colors.OKBLUE}ℹ️  {msg}{Colors.ENDC}")

def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")

def check_existing_auth():
    """Check if already authenticated"""
    try:
        api = HfApi()
        user_info = api.whoami()
        return user_info
    except Exception:
        return None

def get_token_securely():
    """Prompt user for HF token securely"""
    print(f"\n{Colors.BOLD}Step 1: Get Your HuggingFace Token{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'─'*70}{Colors.ENDC}")
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Click 'New token' (or use existing token)")
    print("3. Name: 'CycleCore-Maaza-Upload'")
    print("4. Type: 'Write' (required for model uploads)")
    print("5. Copy the token")
    print(f"{Colors.OKBLUE}{'─'*70}{Colors.ENDC}\n")
    
    # Get token with hidden input
    try:
        token = getpass.getpass(f"{Colors.BOLD}Enter your HuggingFace token (input hidden): {Colors.ENDC}")
        return token.strip()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Authentication cancelled by user.{Colors.ENDC}")
        sys.exit(0)

def validate_and_login(token):
    """Validate token and log in"""
    print(f"\n{Colors.BOLD}Step 2: Validating Token{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'─'*70}{Colors.ENDC}")
    
    try:
        # Attempt login
        print("Authenticating with HuggingFace...", end=" ", flush=True)
        login(token=token, add_to_git_credential=False)
        
        # Verify authentication
        api = HfApi()
        user_info = api.whoami()
        
        print(f"{Colors.OKGREEN}Success!{Colors.ENDC}")
        print_success(f"Authenticated as: {user_info['name']}")
        
        if 'orgs' in user_info and user_info['orgs']:
            print(f"{Colors.OKBLUE}Organizations:{Colors.ENDC}")
            for org in user_info['orgs']:
                org_name = org.get('name', 'Unknown')
                print(f"  • {org_name}")
        
        return True
        
    except Exception as e:
        print(f"{Colors.FAIL}Failed!{Colors.ENDC}")
        print_error(f"Authentication failed: {str(e)}")
        print_info("Please check your token and try again.")
        return False

def show_next_steps():
    """Show what to do next"""
    print(f"\n{Colors.BOLD}Step 3: Ready to Upload!{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'─'*70}{Colors.ENDC}")
    print_success("Authentication complete! You can now upload models.")
    print(f"\n{Colors.BOLD}Next steps:{Colors.ENDC}")
    print("1. Run the upload script:")
    print(f"   {Colors.OKCYAN}python /home/rain/SLMBench/scripts/upload_to_huggingface.py{Colors.ENDC}")
    print("\n2. Or upload manually:")
    print(f"   {Colors.OKCYAN}cd /home/rain/SLMBench{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}huggingface-cli upload CycleCore/Maaza-MLM-135M-JSON-v1 models/mlm_135m_json/final_model/{Colors.ENDC}")
    print(f"\n3. Upload logo to CycleCore org profile:")
    print(f"   {Colors.OKCYAN}/home/rain/SLMBench/assets/logos/cyclecore-logo-400x400.png{Colors.ENDC}")
    print(f"\n{Colors.OKBLUE}{'─'*70}{Colors.ENDC}\n")

def main():
    """Main wizard flow"""
    print_header()
    
    # Check if already authenticated
    print(f"{Colors.BOLD}Checking existing authentication...{Colors.ENDC}")
    existing_auth = check_existing_auth()
    
    if existing_auth:
        print_success(f"Already authenticated as: {existing_auth['name']}")
        print_info("You can proceed directly to model upload.")
        
        response = input(f"\n{Colors.BOLD}Re-authenticate with a different token? (y/N): {Colors.ENDC}").lower()
        if response != 'y':
            show_next_steps()
            return
        print()
    
    # Get token from user
    token = get_token_securely()
    
    if not token:
        print_error("No token provided. Exiting.")
        sys.exit(1)
    
    # Validate and login
    success = validate_and_login(token)
    
    if success:
        show_next_steps()
        
        # Ask if user wants to upload now
        print(f"{Colors.BOLD}Upload models now?{Colors.ENDC}")
        response = input(f"Run upload script? (Y/n): {Colors.ENDC}").lower()
        
        if response != 'n':
            print(f"\n{Colors.OKCYAN}Starting upload...{Colors.ENDC}\n")
            import subprocess
            subprocess.run([sys.executable, "/home/rain/SLMBench/scripts/upload_to_huggingface.py"])
    else:
        print_error("Authentication failed. Please try again.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Wizard cancelled by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

