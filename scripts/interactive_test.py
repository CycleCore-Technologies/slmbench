#!/usr/bin/env python3
"""
Interactive test script for CycleCore Maaza models
Allows you to chat with MLM-135M or SLM-360M in the terminal
"""

import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def load_model(model_choice):
    """Load the selected model"""
    print(f"\n{'='*60}")
    print(f"Loading {model_choice}...")
    print(f"{'='*60}\n")

    if model_choice == "135M":
        base_path = "/home/rain/SLMBench/models/smollm2-135m"
        adapter_path = "/home/rain/SLMBench/models/mlm_135m_json/final_model"
        model_name = "CycleCore Maaza MLM-135M-JSON v1.0.0"
    else:  # 360M
        base_path = "/home/rain/SLMBench/models/smollm2-360m"
        adapter_path = "/home/rain/SLMBench/models/slm_360m_json/final_model"
        model_name = "CycleCore Maaza SLM-360M-JSON v1.0.0"

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(base_path)

    # Load base model
    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load LoRA adapter
    print("Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model.eval()

    print(f"\n✓ {model_name} loaded successfully!")
    print(f"Device: {next(model.parameters()).device}")
    print(f"{'='*60}\n")

    return model, tokenizer, model_name

def format_prompt(user_input):
    """Format user input as JSON extraction prompt"""
    return f"""Extract the structured JSON data from the following text.

Input: {user_input}

Output:"""

def generate_response(model, tokenizer, prompt, max_tokens=512):
    """Generate model response"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.0,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode and extract just the generated part
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove the prompt from the response
    if prompt in full_response:
        response = full_response[len(prompt):].strip()
    else:
        response = full_response.strip()

    return response

def print_examples():
    """Print example prompts"""
    print("\n📝 Example prompts to try:\n")
    print("1. Extract contact info:")
    print("   → John Doe, email: john@example.com, phone: 555-1234")
    print()
    print("2. Extract product info:")
    print("   → Laptop Model X, price $999, 16GB RAM, 512GB SSD")
    print()
    print("3. Extract order:")
    print("   → Order #12345, customer Jane Smith, 2x widgets at $19.99 each, total $39.98")
    print()
    print("4. Extract sensor data:")
    print("   → Temperature 72.5°F, humidity 45%, pressure 1013 hPa at 2025-11-20 14:30")
    print()

def main():
    print("\n" + "="*60)
    print("CycleCore Maaza Models - Interactive Test")
    print("="*60)

    # Model selection
    print("\nSelect model:")
    print("  1) MLM-135M (faster, simpler schemas)")
    print("  2) SLM-360M (better accuracy, medium schemas)")

    while True:
        choice = input("\nEnter 1 or 2: ").strip()
        if choice in ["1", "2"]:
            model_choice = "135M" if choice == "1" else "360M"
            break
        print("Invalid choice. Please enter 1 or 2.")

    # Load model
    model, tokenizer, model_name = load_model(model_choice)

    # Show examples
    print_examples()

    # Interactive loop
    print("\n" + "="*60)
    print("Ready! Type your text to extract JSON.")
    print("Commands: 'examples' = show examples, 'quit' = exit")
    print("="*60 + "\n")

    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()

            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break

            if user_input.lower() == 'examples':
                print_examples()
                continue

            if not user_input:
                continue

            # Format prompt
            prompt = format_prompt(user_input)

            # Generate response
            print(f"\n🤖 {model_name}:")
            print("-" * 60)

            response = generate_response(model, tokenizer, prompt)
            print(response)
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()
