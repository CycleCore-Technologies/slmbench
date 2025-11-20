#!/usr/bin/env python3
"""
Validate OSS tools installation and performance.

Tests:
1. Unsloth + TRL availability
2. PyTorch + CUDA availability
3. Transformers compatibility
4. LM Eval Harness functionality
5. Dataset loading
"""

import sys

def test_imports():
    """Test all critical imports."""
    print("=" * 60)
    print("Testing imports...")
    print("=" * 60)

    tests = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("datasets", "Datasets"),
        ("unsloth", "Unsloth"),
        ("trl", "TRL"),
        ("lm_eval", "LM Evaluation Harness"),
        ("sklearn", "scikit-learn"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
    ]

    for module, name in tests:
        try:
            mod = __import__(module)
            version = getattr(mod, "__version__", "unknown")
            print(f"✅ {name:30s} version {version}")
        except ImportError as e:
            print(f"❌ {name:30s} FAILED: {e}")
            return False

    return True

def test_cuda():
    """Test CUDA availability."""
    import torch
    print("\n" + "=" * 60)
    print("Testing CUDA...")
    print("=" * 60)

    cuda_available = torch.cuda.is_available()
    if cuda_available:
        print(f"✅ CUDA available: {torch.version.cuda}")
        print(f"✅ Device: {torch.cuda.get_device_name(0)}")
        print(f"✅ Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️  CUDA not available (CPU-only mode)")

    return cuda_available

def test_unsloth():
    """Test Unsloth functionality."""
    print("\n" + "=" * 60)
    print("Testing Unsloth...")
    print("=" * 60)

    try:
        from unsloth import FastLanguageModel
        print("✅ Unsloth FastLanguageModel imported successfully")
        print("✅ Ready for 2x faster training with 70% less VRAM")
        return True
    except Exception as e:
        print(f"❌ Unsloth test failed: {e}")
        return False

def test_dataset_loading():
    """Test BANKING77 dataset loading."""
    print("\n" + "=" * 60)
    print("Testing BANKING77 dataset...")
    print("=" * 60)

    try:
        import json
        from pathlib import Path

        test_path = Path("benchmarks/edge_intent/dataset/banking77_test.jsonl")

        if not test_path.exists():
            print(f"❌ Dataset not found at {test_path}")
            return False

        # Load first example
        with open(test_path) as f:
            example = json.loads(f.readline())

        print(f"✅ Dataset loaded from {test_path}")
        print(f"✅ Example text: {example.get('text', 'N/A')[:60]}...")
        print(f"✅ Example label: {example.get('label', 'N/A')}")
        print(f"✅ Ready for EdgeIntent benchmark!")
        return True
    except Exception as e:
        print(f"❌ Dataset test failed: {e}")
        return False

def test_lm_eval():
    """Test LM Eval Harness."""
    print("\n" + "=" * 60)
    print("Testing LM Evaluation Harness...")
    print("=" * 60)

    try:
        import lm_eval
        print(f"✅ LM Eval version: {lm_eval.__version__}")
        print("✅ Ready for benchmark evaluations")
        return True
    except Exception as e:
        print(f"❌ LM Eval test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("\n" + "=" * 60)
    print("OSS TOOLS VALIDATION")
    print("=" * 60)
    print()

    results = {
        "Imports": test_imports(),
        "CUDA": test_cuda(),
        "Unsloth": test_unsloth(),
        "BANKING77 Dataset": test_dataset_loading(),
        "LM Eval Harness": test_lm_eval(),
    }

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10s} {test_name}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Ready for Phase 2 work!")
    else:
        print("⚠️  SOME TESTS FAILED - Review errors above")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
