#!/usr/bin/env python3
"""
Manual Testing Script for CycleCore-Maaza-SLM-135M-JSON

Tests the trained LoRA model on sample prompts to verify:
1. Model and adapter load correctly
2. JSON output is valid and parseable
3. Basic extraction functionality works

Usage:
    python scripts/test_mlm_135m_json.py [--device cpu/cuda]
"""

import json
import sys
import argparse
import time
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


# Test cases covering different complexity levels
TEST_CASES = [
    {
        "name": "Simple Contact Info",
        "complexity": "simple",
        "prompt": "Extract contact information: John Doe, john@example.com, 555-1234",
        "expected_fields": ["name", "email", "phone"]
    },
    {
        "name": "Order Information",
        "complexity": "medium",
        "prompt": "Order ORD-12345 for Jane Smith (jane@example.com). Items: 2x Product A ($50 each). Total: $100.00. Ship to: 123 Main St, Seattle, WA 98101.",
        "expected_fields": ["order_id", "customer_name", "customer_email", "items", "total_amount", "shipping_address"]
    },
    {
        "name": "Event Details",
        "complexity": "medium",
        "prompt": "Annual Tech Conference on January 15, 2025 at 9:00 AM. Location: Convention Center, Room 301, San Francisco. Attendees: 250 people. Speaker: Dr. Sarah Johnson.",
        "expected_fields": ["event_name", "date", "time", "location", "attendees", "speaker"]
    },
    {
        "name": "Product Listing",
        "complexity": "simple",
        "prompt": "Laptop Model XPS-15. Price: $1,299.99. RAM: 16GB. Storage: 512GB SSD. In stock: Yes.",
        "expected_fields": ["name", "price", "ram", "storage", "in_stock"]
    }
]


def load_model(base_model_path: str, adapter_path: str, device: str = "cuda"):
    """Load base model and LoRA adapter."""
    print("=" * 80)
    print("Loading Model and Adapter")
    print("=" * 80)
    print(f"Base model: {base_model_path}")
    print(f"LoRA adapter: {adapter_path}")
    print(f"Device: {device}")
    print()

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load base model
    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None
    )

    if device == "cpu":
        base_model = base_model.to("cpu")

    # Load LoRA adapter
    print("Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model.eval()

    print("✓ Model loaded successfully")
    print()

    return model, tokenizer


def extract_json_from_output(text: str) -> dict:
    """Extract JSON from model output text."""
    # Try to find JSON in the output
    # Model outputs format: "Output: {json}"

    # First try: split on "Output:" and take everything after
    if "Output:" in text:
        json_text = text.split("Output:")[-1].strip()
    else:
        json_text = text.strip()

    # Find first { and try to parse progressively
    start = json_text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in output")

    # Try to find valid JSON by progressively including more text
    # This handles cases where model generates text after JSON
    for end_pos in range(len(json_text), start, -1):
        try:
            candidate = json_text[start:end_pos]
            # Try to parse
            parsed = json.loads(candidate)
            return parsed
        except json.JSONDecodeError:
            # Try next position
            continue

    # If that didn't work, try to find just up to the last }
    end = json_text.rfind("}") + 1
    if end > start:
        try:
            return json.loads(json_text[start:end])
        except json.JSONDecodeError:
            pass

    raise ValueError("Could not parse valid JSON from output")


def test_extraction(model, tokenizer, test_case: dict, device: str = "cuda"):
    """Test model on a single case."""
    print("-" * 80)
    print(f"Test: {test_case['name']} ({test_case['complexity']})")
    print("-" * 80)
    print(f"Input: {test_case['prompt']}")
    print()

    # Format prompt
    full_prompt = f"Extract the structured JSON data from the following text.\n\nInput: {test_case['prompt']}\n\nOutput:"

    # Tokenize
    inputs = tokenizer(full_prompt, return_tensors="pt")
    if device == "cuda":
        inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate with stop strings
    start_time = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            # Stop at double newline or when repeating the prompt structure
            stop_strings=["\\n\\nInput:", "\\n\\nExtract", "Please extract"],
            tokenizer=tokenizer
        )
    generation_time = time.time() - start_time

    # Decode
    result_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Raw Output:\n{result_text}")
    print()

    # Try to parse JSON
    try:
        json_output = extract_json_from_output(result_text)
        print("✓ Valid JSON extracted:")
        print(json.dumps(json_output, indent=2))
        print()

        # Check for expected fields
        expected = set(test_case["expected_fields"])
        actual = set(json_output.keys())

        missing = expected - actual
        extra = actual - expected

        if not missing and not extra:
            print("✓ All expected fields present")
            field_status = "PASS"
        else:
            field_status = "PARTIAL"
            if missing:
                print(f"⚠ Missing fields: {missing}")
            if extra:
                print(f"⚠ Extra fields: {extra}")

        parse_status = "PASS"

    except Exception as e:
        print(f"✗ Failed to parse JSON: {e}")
        parse_status = "FAIL"
        field_status = "N/A"
        json_output = None

    print(f"Generation time: {generation_time:.3f}s")
    print()

    return {
        "name": test_case["name"],
        "complexity": test_case["complexity"],
        "parse_status": parse_status,
        "field_status": field_status,
        "generation_time": generation_time,
        "output": json_output
    }


def main():
    parser = argparse.ArgumentParser(description="Test CycleCore-Maaza-SLM-135M-JSON model")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"],
                       help="Device to run on (default: cuda)")
    parser.add_argument("--base-model", type=str,
                       default="/home/rain/SLMBench/models/smollm2-135m",
                       help="Path to base model")
    parser.add_argument("--adapter", type=str,
                       default="/home/rain/SLMBench/models/mlm_135m_json/final_model",
                       help="Path to LoRA adapter")

    args = parser.parse_args()

    # Check if CUDA is available
    if args.device == "cuda" and not torch.cuda.is_available():
        print("Warning: CUDA not available, falling back to CPU")
        args.device = "cpu"

    print("=" * 80)
    print("CycleCore-Maaza-SLM-135M-JSON Manual Testing")
    print("=" * 80)
    print()

    # Check paths exist
    base_model_path = Path(args.base_model)
    adapter_path = Path(args.adapter)

    if not base_model_path.exists():
        print(f"Error: Base model not found at {base_model_path}")
        return 1

    if not adapter_path.exists():
        print(f"Error: Adapter not found at {adapter_path}")
        return 1

    # Load model
    try:
        model, tokenizer = load_model(str(base_model_path), str(adapter_path), args.device)
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Run tests
    print("=" * 80)
    print("Running Test Cases")
    print("=" * 80)
    print()

    results = []
    for test_case in TEST_CASES:
        try:
            result = test_extraction(model, tokenizer, test_case, args.device)
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "name": test_case["name"],
                "complexity": test_case["complexity"],
                "parse_status": "ERROR",
                "field_status": "N/A",
                "generation_time": 0,
                "output": None
            })
        print()

    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print()

    total = len(results)
    parse_pass = sum(1 for r in results if r["parse_status"] == "PASS")
    field_pass = sum(1 for r in results if r["field_status"] == "PASS")
    avg_time = sum(r["generation_time"] for r in results) / total if total > 0 else 0

    print(f"Total tests: {total}")
    print(f"Valid JSON: {parse_pass}/{total} ({parse_pass/total*100:.1f}%)")
    print(f"All fields correct: {field_pass}/{total} ({field_pass/total*100:.1f}%)")
    print(f"Average generation time: {avg_time:.3f}s")
    print()

    # Results table
    print("Results by test:")
    print()
    print(f"{'Test Name':<25} {'Complexity':<10} {'JSON':<6} {'Fields':<8} {'Time':<8}")
    print("-" * 80)
    for r in results:
        print(f"{r['name']:<25} {r['complexity']:<10} {r['parse_status']:<6} {r['field_status']:<8} {r['generation_time']:.3f}s")
    print()

    # Overall status
    if parse_pass == total:
        print("✓ ALL TESTS PASSED - Model is working correctly!")
        return 0
    elif parse_pass > 0:
        print("⚠ PARTIAL SUCCESS - Some tests passed, some failed")
        return 0
    else:
        print("✗ ALL TESTS FAILED - Model may not be working correctly")
        return 1


if __name__ == "__main__":
    sys.exit(main())
