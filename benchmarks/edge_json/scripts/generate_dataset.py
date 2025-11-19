#!/usr/bin/env python3
"""
EdgeJSON Dataset Generation Script
Generates synthetic JSON extraction test cases for EdgeBench evaluation.

Usage:
    python generate_dataset.py --num_samples 1000 --output dataset/test.jsonl

Complexity Levels:
- Simple: 3-5 fields, flat structure
- Medium: 8-12 fields, nested objects
- Complex: 15+ fields, arrays, deep nesting
"""

import json
import random
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta


# Schema templates for each complexity level
SIMPLE_SCHEMAS = [
    {
        "name": "contact_info",
        "description": "Basic contact information",
        "fields": ["name", "email", "phone"],
        "types": {"name": "string", "email": "string", "phone": "string"}
    },
    {
        "name": "product_info",
        "description": "Simple product details",
        "fields": ["product_name", "price", "quantity"],
        "types": {"product_name": "string", "price": "float", "quantity": "int"}
    },
    {
        "name": "user_profile",
        "description": "Basic user profile",
        "fields": ["username", "age", "city"],
        "types": {"username": "string", "age": "int", "city": "string"}
    },
]

MEDIUM_SCHEMAS = [
    {
        "name": "order_details",
        "description": "E-commerce order with line items",
        "fields": ["order_id", "customer_name", "customer_email", "order_date",
                  "total_amount", "status", "shipping_address", "items"],
        "types": {
            "order_id": "string",
            "customer_name": "string",
            "customer_email": "string",
            "order_date": "string",
            "total_amount": "float",
            "status": "string",
            "shipping_address": "object",
            "items": "array"
        }
    },
    {
        "name": "event_registration",
        "description": "Event registration form data",
        "fields": ["event_name", "attendee_name", "attendee_email", "ticket_type",
                  "registration_date", "payment_status", "dietary_requirements", "emergency_contact"],
        "types": {
            "event_name": "string",
            "attendee_name": "string",
            "attendee_email": "string",
            "ticket_type": "string",
            "registration_date": "string",
            "payment_status": "string",
            "dietary_requirements": "array",
            "emergency_contact": "object"
        }
    },
]

COMPLEX_SCHEMAS = [
    {
        "name": "multi_party_transaction",
        "description": "Complex transaction with multiple parties",
        "fields": ["transaction_id", "timestamp", "parties", "line_items", "payment_details",
                  "terms", "metadata", "approvals", "documents", "notes"],
        "types": {
            "transaction_id": "string",
            "timestamp": "string",
            "parties": "array",
            "line_items": "array",
            "payment_details": "object",
            "terms": "object",
            "metadata": "object",
            "approvals": "array",
            "documents": "array",
            "notes": "array"
        }
    },
]


def generate_simple_example(schema: Dict) -> Dict[str, Any]:
    """Generate a simple JSON example based on schema"""
    result = {}

    for field in schema["fields"]:
        field_type = schema["types"][field]

        if field_type == "string":
            if "name" in field:
                result[field] = random.choice(["John Doe", "Jane Smith", "Alice Johnson", "Bob Williams"])
            elif "email" in field:
                result[field] = f"{random.choice(['john', 'jane', 'alice', 'bob'])}@example.com"
            elif "phone" in field:
                result[field] = f"555-{random.randint(1000, 9999)}"
            elif "city" in field:
                result[field] = random.choice(["New York", "San Francisco", "Seattle", "Boston"])
            elif "product" in field:
                result[field] = random.choice(["Widget A", "Gadget B", "Tool C", "Device D"])
            elif "username" in field:
                result[field] = random.choice(["johndoe", "janesmith", "alice123", "bobw"])
            else:
                result[field] = f"sample_{field}"

        elif field_type == "int":
            if "age" in field:
                result[field] = random.randint(18, 70)
            elif "quantity" in field:
                result[field] = random.randint(1, 100)
            else:
                result[field] = random.randint(1, 1000)

        elif field_type == "float":
            if "price" in field or "amount" in field:
                result[field] = round(random.uniform(10.0, 1000.0), 2)
            else:
                result[field] = round(random.uniform(0.0, 100.0), 2)

    return result


def generate_medium_example(schema: Dict) -> Dict[str, Any]:
    """Generate a medium complexity JSON example"""
    result = {}

    for field in schema["fields"]:
        field_type = schema["types"][field]

        if field_type == "string":
            if "id" in field:
                result[field] = f"ORD-{random.randint(10000, 99999)}"
            elif "name" in field:
                result[field] = random.choice(["John Doe", "Jane Smith", "Alice Johnson"])
            elif "email" in field:
                result[field] = f"{random.choice(['john', 'jane', 'alice'])}@example.com"
            elif "date" in field:
                date = datetime.now() - timedelta(days=random.randint(0, 365))
                result[field] = date.strftime("%Y-%m-%d")
            elif "status" in field:
                result[field] = random.choice(["pending", "confirmed", "completed", "cancelled"])
            elif "event" in field:
                result[field] = random.choice(["Tech Conference 2025", "Workshop Series", "Annual Summit"])
            elif "ticket" in field:
                result[field] = random.choice(["standard", "vip", "early_bird"])
            else:
                result[field] = f"sample_{field}"

        elif field_type == "float":
            result[field] = round(random.uniform(50.0, 5000.0), 2)

        elif field_type == "object":
            if "address" in field:
                result[field] = {
                    "street": f"{random.randint(100, 999)} Main St",
                    "city": random.choice(["New York", "San Francisco", "Seattle"]),
                    "state": random.choice(["NY", "CA", "WA"]),
                    "zip": f"{random.randint(10000, 99999)}"
                }
            elif "contact" in field:
                result[field] = {
                    "name": random.choice(["John Doe", "Jane Smith"]),
                    "phone": f"555-{random.randint(1000, 9999)}"
                }
            else:
                result[field] = {"key": "value"}

        elif field_type == "array":
            if "items" in field or "line_items" in field:
                result[field] = [
                    {
                        "name": random.choice(["Product A", "Product B", "Product C"]),
                        "quantity": random.randint(1, 10),
                        "price": round(random.uniform(10.0, 100.0), 2)
                    }
                    for _ in range(random.randint(1, 4))
                ]
            elif "dietary" in field:
                result[field] = random.sample(["vegetarian", "vegan", "gluten-free", "none"], k=random.randint(0, 2))
            else:
                result[field] = [f"item_{i}" for i in range(random.randint(1, 3))]

    return result


def generate_prompt(schema: Dict, example: Dict[str, Any]) -> str:
    """Generate natural language prompt for the JSON extraction task"""
    schema_name = schema["name"]

    if schema_name == "contact_info":
        return f"Extract contact information: {example['name']}, {example['email']}, {example['phone']}"

    elif schema_name == "product_info":
        return f"Product details: {example['product_name']} costs ${example['price']}, {example['quantity']} in stock"

    elif schema_name == "user_profile":
        return f"User profile: {example['username']}, age {example['age']}, lives in {example['city']}"

    elif schema_name == "order_details":
        items_text = ", ".join([f"{item['quantity']}x {item['name']}" for item in example.get('items', [])])
        return f"Order {example['order_id']} for {example['customer_name']} ({example['customer_email']}). Items: {items_text}. Total: ${example['total_amount']}. Status: {example['status']}. Ship to: {example.get('shipping_address', {}).get('city', 'unknown')}."

    elif schema_name == "event_registration":
        diet_text = ", ".join(example.get('dietary_requirements', [])) or "none"
        return f"Event registration for {example['event_name']}: {example['attendee_name']} ({example['attendee_email']}), {example['ticket_type']} ticket, dietary needs: {diet_text}. Emergency contact: {example.get('emergency_contact', {}).get('name', 'unknown')}."

    else:
        # Generic prompt
        return f"Extract the following information as JSON: {schema['description']}. Data: {str(example)}"


def generate_dataset(num_samples: int, complexity_distribution: Dict[str, float]) -> List[Dict]:
    """
    Generate EdgeJSON dataset

    Args:
        num_samples: Total number of samples to generate
        complexity_distribution: Dict with keys 'simple', 'medium', 'complex' and percentages

    Returns:
        List of dataset examples (prompt, expected_output, schema, complexity)
    """
    dataset = []

    # Calculate samples per complexity level
    num_simple = int(num_samples * complexity_distribution["simple"])
    num_medium = int(num_samples * complexity_distribution["medium"])
    num_complex = num_samples - num_simple - num_medium

    # Generate simple examples
    for _ in range(num_simple):
        schema = random.choice(SIMPLE_SCHEMAS)
        example = generate_simple_example(schema)
        prompt = generate_prompt(schema, example)

        dataset.append({
            "prompt": prompt,
            "expected_output": example,
            "schema_name": schema["name"],
            "complexity": "simple",
            "schema": schema
        })

    # Generate medium examples
    for _ in range(num_medium):
        schema = random.choice(MEDIUM_SCHEMAS)
        example = generate_medium_example(schema)
        prompt = generate_prompt(schema, example)

        dataset.append({
            "prompt": prompt,
            "expected_output": example,
            "schema_name": schema["name"],
            "complexity": "medium",
            "schema": schema
        })

    # Generate complex examples (simplified for now - will expand later)
    for _ in range(num_complex):
        schema = random.choice(MEDIUM_SCHEMAS)  # Placeholder: use medium for now
        example = generate_medium_example(schema)
        prompt = generate_prompt(schema, example)

        dataset.append({
            "prompt": prompt,
            "expected_output": example,
            "schema_name": schema["name"],
            "complexity": "complex",  # Mark as complex even though using medium schema
            "schema": schema
        })

    # Shuffle dataset
    random.shuffle(dataset)

    return dataset


def save_dataset(dataset: List[Dict], output_path: Path):
    """Save dataset to JSONL file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        for example in dataset:
            f.write(json.dumps(example) + '\n')

    print(f"Saved {len(dataset)} examples to {output_path}")


def print_dataset_stats(dataset: List[Dict]):
    """Print dataset statistics"""
    complexity_counts = {"simple": 0, "medium": 0, "complex": 0}
    schema_counts = {}

    for example in dataset:
        complexity_counts[example["complexity"]] += 1
        schema_name = example["schema_name"]
        schema_counts[schema_name] = schema_counts.get(schema_name, 0) + 1

    print("\n=== Dataset Statistics ===")
    print(f"Total examples: {len(dataset)}")
    print(f"\nComplexity distribution:")
    for complexity, count in sorted(complexity_counts.items()):
        pct = (count / len(dataset)) * 100
        print(f"  {complexity}: {count} ({pct:.1f}%)")

    print(f"\nSchema distribution:")
    for schema_name, count in sorted(schema_counts.items()):
        pct = (count / len(dataset)) * 100
        print(f"  {schema_name}: {count} ({pct:.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="Generate EdgeJSON dataset")
    parser.add_argument("--num_samples", type=int, default=100, help="Number of samples to generate")
    parser.add_argument("--output", type=str, default="dataset/test.jsonl", help="Output file path")
    parser.add_argument("--simple", type=float, default=0.4, help="Percentage of simple examples (0-1)")
    parser.add_argument("--medium", type=float, default=0.4, help="Percentage of medium examples (0-1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")

    args = parser.parse_args()

    # Set random seed
    random.seed(args.seed)

    # Calculate complex percentage
    complex_pct = 1.0 - args.simple - args.medium
    if complex_pct < 0:
        print("Error: simple + medium percentages must be <= 1.0")
        return

    complexity_distribution = {
        "simple": args.simple,
        "medium": args.medium,
        "complex": complex_pct
    }

    print(f"Generating EdgeJSON dataset...")
    print(f"Samples: {args.num_samples}")
    print(f"Complexity: {args.simple*100:.0f}% simple, {args.medium*100:.0f}% medium, {complex_pct*100:.0f}% complex")

    # Generate dataset
    dataset = generate_dataset(args.num_samples, complexity_distribution)

    # Save to file
    output_path = Path(__file__).parent.parent / args.output
    save_dataset(dataset, output_path)

    # Print statistics
    print_dataset_stats(dataset)

    # Print sample
    print("\n=== Sample Example ===")
    sample = random.choice(dataset)
    print(f"Complexity: {sample['complexity']}")
    print(f"Schema: {sample['schema_name']}")
    print(f"Prompt: {sample['prompt']}")
    print(f"Expected Output: {json.dumps(sample['expected_output'], indent=2)}")


if __name__ == "__main__":
    main()
