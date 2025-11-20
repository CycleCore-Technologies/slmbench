#!/usr/bin/env python3
"""
Quick test to verify Qwen2.5-14B-AWQ works with vLLM.
"""

import sys
from pathlib import Path

# Add benchmarks to path
sys.path.insert(0, str(Path(__file__).parent / "benchmarks/edge_json/scripts/lib"))

from vllm_generator import VLLMGenerator, ModelConfig


def main():
    # Test with just Qwen
    test_config = {
        "qwen": ModelConfig(
            name="qwen",
            model_path="/home/rain/SLMBench/models/qwen2.5-14b-awq",
            max_tokens=128,
            temperature=0.4,
            top_p=0.95
        )
    }

    print("=" * 70)
    print("Testing Qwen2.5-14B-AWQ with vLLM")
    print("=" * 70)
    print()

    try:
        # Initialize generator
        print("Initializing vLLM generator...")
        gen = VLLMGenerator(test_config, gpu_memory_utilization=0.85)

        # Test prompts
        test_prompts = [
            "Extract contact info: John Doe, email: john@example.com, phone: 555-1234",
            "Extract product: iPhone 15 Pro, price: $999, in stock: yes"
        ]

        print(f"Generating {len(test_prompts)} test completions...")
        print()

        # Generate
        completions = gen.generate("qwen", test_prompts, batch_size=2)

        # Show results
        print("=" * 70)
        print("Results:")
        print("=" * 70)
        for i, (prompt, completion) in enumerate(zip(test_prompts, completions)):
            print(f"\n[{i+1}] Prompt: {prompt[:60]}...")
            print(f"    Output: {completion[:100]}...")

        print("\n" + "=" * 70)
        print("✓ Test successful! Qwen2.5-14B-AWQ is working.")
        print("=" * 70)

        gen.cleanup()
        return 0

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
