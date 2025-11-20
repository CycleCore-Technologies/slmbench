#!/usr/bin/env python3
"""
Download BANKING77 dataset for EdgeIntent benchmark.

Dataset: PolyAI/banking77
License: CC-BY-4.0 (attribution required)
Size: 13,083 examples (10,003 train / 3,080 test)
Classes: 77 banking intents
"""

from datasets import load_dataset
import json
from pathlib import Path

def download_banking77():
    """Download and save BANKING77 dataset."""
    print("Downloading BANKING77 dataset from Hugging Face...")

    # Load dataset (trust_remote_code required for this dataset)
    dataset = load_dataset("PolyAI/banking77", trust_remote_code=True)

    # Create output directory
    output_dir = Path("benchmarks/edge_intent/dataset")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save train set
    train_path = output_dir / "banking77_train.jsonl"
    with open(train_path, 'w') as f:
        for example in dataset['train']:
            json.dump(example, f)
            f.write('\n')
    print(f"✅ Train set saved: {train_path} ({len(dataset['train'])} examples)")

    # Save test set
    test_path = output_dir / "banking77_test.jsonl"
    with open(test_path, 'w') as f:
        for example in dataset['test']:
            json.dump(example, f)
            f.write('\n')
    print(f"✅ Test set saved: {test_path} ({len(dataset['test'])} examples)")

    # Print dataset info
    print("\n📊 Dataset Statistics:")
    print(f"  Train: {len(dataset['train'])} examples")
    print(f"  Test: {len(dataset['test'])} examples")
    print(f"  Total: {len(dataset['train']) + len(dataset['test'])} examples")
    print(f"  Classes: 77 banking intents")
    print(f"  License: CC-BY-4.0 (attribution required)")
    print(f"\n📄 Citation:")
    print("  Casanueva et al. (2020) - 'Efficient Intent Detection with Dual Sentence Encoders'")
    print(f"\n✅ BANKING77 dataset ready for EdgeIntent benchmark!")

if __name__ == "__main__":
    download_banking77()
