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
Upload Maaza models to HuggingFace Hub
Usage: python upload_to_huggingface.py
"""

import os
from huggingface_hub import HfApi, create_repo
from pathlib import Path

# Configuration
MODELS = [
    {
        "name": "Maaza-MLM-135M-JSON-v1",
        "path": "/home/rain/SLMBench/models/mlm_135m_json/final_model",
        "repo_id": "CycleCoreTechnologies/Maaza-MLM-135M-JSON-v1",
        "description": "Micro Language Model (135M) for edge JSON extraction - 24.7% JSONExact"
    },
    {
        "name": "Maaza-SLM-360M-JSON-v1",
        "path": "/home/rain/SLMBench/models/slm_360m_json/final_model",
        "repo_id": "CycleCoreTechnologies/Maaza-SLM-360M-JSON-v1",
        "description": "Small Language Model (360M) for edge JSON extraction - 55.1% JSONExact"
    }
]

def upload_model(model_info):
    """Upload a single model to HuggingFace Hub"""
    print(f"\n{'='*60}")
    print(f"Uploading {model_info['name']}...")
    print(f"{'='*60}")
    
    api = HfApi()
    repo_id = model_info['repo_id']
    model_path = Path(model_info['path'])
    
    # Check if model files exist
    if not model_path.exists():
        print(f"❌ Error: Model path not found: {model_path}")
        return False
    
    print(f"📁 Model path: {model_path}")
    print(f"🎯 Repository: {repo_id}")
    
    try:
        # Create repository (will skip if exists)
        print(f"\n1️⃣  Creating repository...")
        create_repo(
            repo_id=repo_id,
            repo_type="model",
            exist_ok=True,
            private=False
        )
        print(f"✅ Repository ready: https://huggingface.co/{repo_id}")
        
        # Upload all files from the model directory
        print(f"\n2️⃣  Uploading model files...")
        api.upload_folder(
            folder_path=str(model_path),
            repo_id=repo_id,
            repo_type="model",
            commit_message=f"Upload {model_info['name']} - v1.0.0 production release"
        )
        
        print(f"✅ Upload complete!")
        print(f"🔗 View at: https://huggingface.co/{repo_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading {model_info['name']}: {e}")
        return False

def main():
    print("🚀 CycleCore Maaza Models - HuggingFace Upload")
    print("="*60)
    
    # Check authentication
    try:
        api = HfApi()
        user_info = api.whoami()
        print(f"✅ Authenticated as: {user_info['name']}")
    except Exception as e:
        print(f"❌ Not authenticated. Please run: hf auth login --token YOUR_TOKEN")
        print(f"   Get your token from: https://huggingface.co/settings/tokens")
        return
    
    # Upload each model
    results = []
    for model in MODELS:
        success = upload_model(model)
        results.append((model['name'], success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 UPLOAD SUMMARY")
    print(f"{'='*60}")
    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {name}")
    
    all_success = all(success for _, success in results)
    if all_success:
        print(f"\n🎉 All models uploaded successfully!")
        print(f"\n📋 Next steps:")
        print(f"   1. Upload logo to CycleCore org: /home/rain/SLMBench/assets/logos/cyclecore-logo-400x400.png")
        print(f"   2. Verify model cards look correct")
        print(f"   3. Update main README.md with HuggingFace links")
    else:
        print(f"\n⚠️  Some uploads failed. Check errors above.")

if __name__ == "__main__":
    main()

