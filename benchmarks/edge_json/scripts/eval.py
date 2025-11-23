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
EdgeJSON Evaluation Harness
Evaluate SLMs on JSON extraction tasks from EdgeBench.

Usage:
    python eval.py --model HuggingFaceTB/SmolLM2-135M --dataset dataset/test.jsonl
    python eval.py --model Qwen/Qwen2.5-0.5B --dataset dataset/test.jsonl --output results/qwen_results.json

Metrics:
- JSONExact: Exact match (binary, 1/0)
- FieldF1: Per-field precision/recall/F1
- SchemaCompliance: Valid JSON structure
- Latency: Time to generate output (tokens/sec)
"""

import json
import argparse
import time
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
import re


# Import transformers (will be installed via requirements.txt)
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    from peft import PeftModel
except ImportError as e:
    print(f"Error: Required library not installed: {e}")
    print("Run: pip install transformers torch peft")
    exit(1)


@dataclass
class EvaluationResult:
    """Results for a single example"""
    prompt: str
    expected_output: Dict
    model_output: str
    model_output_parsed: Dict | None
    json_exact: bool
    field_f1: float
    schema_compliance: bool
    latency_ms: float
    complexity: str
    schema_name: str
    error: str | None = None


@dataclass
class AggregateResults:
    """Aggregate results across all examples"""
    model_name: str
    total_examples: int
    json_exact_score: float
    avg_field_f1: float
    schema_compliance_rate: float
    avg_latency_ms: float
    tokens_per_sec: float
    by_complexity: Dict[str, Dict]
    by_schema: Dict[str, Dict]


def extract_json_from_text(text: str) -> Dict | None:
    """
    Extract JSON from model output text.
    Handles cases where model includes extra text before/after JSON.
    """
    # Try to parse entire text first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Look for JSON-like content between braces
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    return None


def calculate_field_f1(expected: Dict, predicted: Dict) -> Tuple[float, float, float]:
    """
    Calculate precision, recall, F1 for field-level matching.

    Compares fields (keys) and values between expected and predicted dicts.
    """
    if not expected and not predicted:
        return 1.0, 1.0, 1.0

    if not expected or not predicted:
        return 0.0, 0.0, 0.0

    # Handle case where predicted is not a dict (e.g., list or other type)
    if not isinstance(predicted, dict):
        return 0.0, 0.0, 0.0

    expected_fields = set(expected.keys())
    predicted_fields = set(predicted.keys())

    # Count correct fields (key + value match)
    correct = 0
    for key in expected_fields & predicted_fields:
        if expected[key] == predicted[key]:
            correct += 1

    precision = correct / len(predicted_fields) if predicted_fields else 0.0
    recall = correct / len(expected_fields) if expected_fields else 0.0

    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    return precision, recall, f1


def check_schema_compliance(expected: Dict, predicted: Dict) -> bool:
    """
    Check if predicted JSON has the same structure as expected.
    (All expected keys present, types match)
    """
    if not predicted:
        return False

    # Handle case where predicted is not a dict
    if not isinstance(predicted, dict):
        return False

    expected_keys = set(expected.keys())
    predicted_keys = set(predicted.keys())

    # All expected keys must be present
    if not expected_keys.issubset(predicted_keys):
        return False

    # Types should match (basic check)
    for key in expected_keys:
        expected_type = type(expected[key])
        predicted_type = type(predicted[key])

        # Allow some flexibility (int/float interchangeable)
        if expected_type in [int, float] and predicted_type in [int, float]:
            continue

        if expected_type != predicted_type:
            return False

    return True


def evaluate_example(
    model,
    tokenizer,
    example: Dict,
    device: str = "cpu",
    max_new_tokens: int = 512
) -> EvaluationResult:
    """Evaluate model on a single EdgeJSON example"""

    prompt = example["prompt"]
    expected_output = example["expected_output"]
    complexity = example.get("complexity", "unknown")
    schema_name = example.get("schema_name", example.get("schema_id", "unknown"))

    # Format prompt for model (matching training format)
    formatted_prompt = f"Extract the structured JSON data from the following text.\n\nInput: {prompt}\n\nOutput:"

    # Tokenize
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    # Generate
    start_time = time.time()
    try:
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.0,  # Deterministic
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )

        # Decode
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the generated part (after the prompt)
        model_output = generated_text[len(formatted_prompt):].strip()

        latency_ms = (time.time() - start_time) * 1000

    except Exception as e:
        return EvaluationResult(
            prompt=prompt,
            expected_output=expected_output,
            model_output="",
            model_output_parsed=None,
            json_exact=False,
            field_f1=0.0,
            schema_compliance=False,
            latency_ms=0.0,
            complexity=complexity,
            schema_name=schema_name,
            error=str(e)
        )

    # Parse JSON from model output
    model_output_parsed = extract_json_from_text(model_output)

    # Calculate metrics
    if model_output_parsed is None:
        # Failed to parse JSON
        json_exact = False
        field_f1 = 0.0
        schema_compliance = False
    else:
        # JSON parsed successfully
        json_exact = (model_output_parsed == expected_output)
        _, _, field_f1 = calculate_field_f1(expected_output, model_output_parsed)
        schema_compliance = check_schema_compliance(expected_output, model_output_parsed)

    return EvaluationResult(
        prompt=prompt,
        expected_output=expected_output,
        model_output=model_output,
        model_output_parsed=model_output_parsed,
        json_exact=json_exact,
        field_f1=field_f1,
        schema_compliance=schema_compliance,
        latency_ms=latency_ms,
        complexity=complexity,
        schema_name=schema_name,
        error=None
    )


def aggregate_results(results: List[EvaluationResult], model_name: str) -> AggregateResults:
    """Aggregate evaluation results"""

    total = len(results)
    json_exact_count = sum(1 for r in results if r.json_exact)
    avg_field_f1 = sum(r.field_f1 for r in results) / total
    schema_compliance_count = sum(1 for r in results if r.schema_compliance)
    avg_latency_ms = sum(r.latency_ms for r in results) / total

    # Estimate tokens/sec (rough estimate: assume ~50 tokens per output)
    avg_tokens = 50
    tokens_per_sec = (avg_tokens / avg_latency_ms) * 1000 if avg_latency_ms > 0 else 0.0

    # By complexity
    by_complexity = {}
    for complexity in ["simple", "medium", "complex"]:
        complexity_results = [r for r in results if r.complexity == complexity]
        if complexity_results:
            by_complexity[complexity] = {
                "count": len(complexity_results),
                "json_exact": sum(1 for r in complexity_results if r.json_exact) / len(complexity_results),
                "avg_field_f1": sum(r.field_f1 for r in complexity_results) / len(complexity_results),
                "schema_compliance": sum(1 for r in complexity_results if r.schema_compliance) / len(complexity_results)
            }

    # By schema
    by_schema = {}
    schema_names = set(r.schema_name for r in results)
    for schema_name in schema_names:
        schema_results = [r for r in results if r.schema_name == schema_name]
        by_schema[schema_name] = {
            "count": len(schema_results),
            "json_exact": sum(1 for r in schema_results if r.json_exact) / len(schema_results),
            "avg_field_f1": sum(r.field_f1 for r in schema_results) / len(schema_results),
            "schema_compliance": sum(1 for r in schema_results if r.schema_compliance) / len(schema_results)
        }

    return AggregateResults(
        model_name=model_name,
        total_examples=total,
        json_exact_score=json_exact_count / total,
        avg_field_f1=avg_field_f1,
        schema_compliance_rate=schema_compliance_count / total,
        avg_latency_ms=avg_latency_ms,
        tokens_per_sec=tokens_per_sec,
        by_complexity=by_complexity,
        by_schema=by_schema
    )


def print_results(aggregate: AggregateResults):
    """Print aggregate results to console"""
    print("\n" + "="*60)
    print(f"EdgeJSON Evaluation Results: {aggregate.model_name}")
    print("="*60)

    print(f"\nOverall Metrics:")
    print(f"  Total Examples: {aggregate.total_examples}")
    print(f"  JSONExact Score: {aggregate.json_exact_score:.1%}")
    print(f"  Average Field F1: {aggregate.avg_field_f1:.3f}")
    print(f"  Schema Compliance: {aggregate.schema_compliance_rate:.1%}")
    print(f"  Avg Latency: {aggregate.avg_latency_ms:.1f}ms")
    print(f"  Throughput: {aggregate.tokens_per_sec:.1f} tokens/sec (estimated)")

    print(f"\nBy Complexity:")
    for complexity in ["simple", "medium", "complex"]:
        if complexity in aggregate.by_complexity:
            stats = aggregate.by_complexity[complexity]
            print(f"  {complexity.capitalize()}:")
            print(f"    JSONExact: {stats['json_exact']:.1%}")
            print(f"    Field F1: {stats['avg_field_f1']:.3f}")
            print(f"    Compliance: {stats['schema_compliance']:.1%}")

    print(f"\nBy Schema:")
    for schema_name, stats in sorted(aggregate.by_schema.items()):
        print(f"  {schema_name}:")
        print(f"    JSONExact: {stats['json_exact']:.1%}")
        print(f"    Field F1: {stats['avg_field_f1']:.3f}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate SLM on EdgeJSON benchmark")
    parser.add_argument("--model", type=str, required=True, help="Hugging Face model name or path")
    parser.add_argument("--adapter", type=str, help="Path to LoRA adapter (optional, for fine-tuned models)")
    parser.add_argument("--dataset", type=str, required=True, help="Path to dataset JSONL file")
    parser.add_argument("--output", type=str, help="Path to save results JSON")
    parser.add_argument("--limit", type=int, help="Limit number of examples (for testing)")
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "cuda"], help="Device to use")
    parser.add_argument("--max_new_tokens", type=int, default=512, help="Max tokens to generate")

    args = parser.parse_args()

    print(f"Loading model: {args.model}")
    if args.adapter:
        print(f"Loading LoRA adapter: {args.adapter}")
    print(f"Device: {args.device}")

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model)

    # Load LoRA adapter if specified
    if args.adapter:
        print("Applying LoRA adapter...")
        model = PeftModel.from_pretrained(model, args.adapter)
        print("✓ LoRA adapter loaded successfully")

    if args.device == "cuda" and torch.cuda.is_available():
        model = model.to("cuda")
    else:
        model = model.to("cpu")

    model.eval()

    # Load dataset
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"Error: Dataset file not found: {dataset_path}")
        return

    dataset = []
    with open(dataset_path, 'r') as f:
        for line in f:
            dataset.append(json.loads(line))

    if args.limit:
        dataset = dataset[:args.limit]

    print(f"Loaded {len(dataset)} examples from {dataset_path}")

    # Evaluate
    print("\nEvaluating...")
    results = []
    for i, example in enumerate(dataset):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{len(dataset)}")

        result = evaluate_example(model, tokenizer, example, device=args.device, max_new_tokens=args.max_new_tokens)
        results.append(result)

    # Aggregate results
    aggregate = aggregate_results(results, args.model)

    # Print results
    print_results(aggregate)

    # Save results if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_data = {
            "aggregate": asdict(aggregate),
            "individual_results": [asdict(r) for r in results]
        }

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
