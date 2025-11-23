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
Training Script for CycleCore Maaza SLM-135M-JSON
LoRA Fine-tuning of SmolLM2-135M on EdgeJSON Benchmark

Phase 4: Model Training & Evaluation
"""

import os
import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
import numpy as np

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))
from data_loader import create_data_loaders, get_dataset_stats


def load_config(config_path: Path) -> Dict:
    """Load training configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def setup_model_and_tokenizer(config: Dict, use_lora: bool = True):
    """
    Setup model and tokenizer with optional LoRA.

    Args:
        config: Training configuration dictionary
        use_lora: Whether to apply LoRA (default: True)

    Returns:
        (model, tokenizer)
    """
    model_path = config['model']['base_model_path']

    print(f"Loading tokenizer from {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Ensure pad token is set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Loading base model from {model_path}")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16 if config['training']['bf16'] else torch.float16,
        device_map="auto",
        trust_remote_code=True
    )

    # Apply LoRA if enabled
    if use_lora and config['lora']['enabled']:
        print("Applying LoRA configuration...")
        lora_config = LoraConfig(
            r=config['lora']['r'],
            lora_alpha=config['lora']['lora_alpha'],
            lora_dropout=config['lora']['lora_dropout'],
            target_modules=config['lora']['target_modules'],
            bias=config['lora']['bias'],
            task_type=TaskType.CAUSAL_LM
        )

        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

    return model, tokenizer


def compute_metrics(eval_pred):
    """Compute evaluation metrics."""
    predictions, labels = eval_pred

    # For language modeling, we just track perplexity
    # (actual JSON extraction metrics run separately with eval.py)

    return {}


def main():
    parser = argparse.ArgumentParser(description="Train MLM-135M-JSON model")
    parser.add_argument(
        "--config",
        type=str,
        default="/home/rain/SLMBench/models/mlm_135m_json/config.yaml",
        help="Path to configuration YAML file"
    )
    parser.add_argument(
        "--validation-run",
        action="store_true",
        help="Run quick validation (100 examples, 1 epoch)"
    )
    parser.add_argument(
        "--resume-from-checkpoint",
        type=str,
        default=None,
        help="Path to checkpoint to resume from"
    )

    args = parser.parse_args()

    # Load configuration
    print("=" * 80)
    print("CycleCore Maaza SLM-135M-JSON Training")
    print("=" * 80)
    print(f"\nLoading configuration from {args.config}")
    config = load_config(Path(args.config))

    # Adjust for validation run
    if args.validation_run:
        print("\n⚠️  VALIDATION RUN MODE")
        print("  - Limited to 100 examples")
        print("  - 1 epoch only")
        print("  - Faster evaluation intervals\n")
        config['training']['num_epochs'] = 1
        config['training']['save_steps'] = 50
        config['training']['eval_steps'] = 50
        config['training']['logging_steps'] = 10
        limit_examples = 100
    else:
        limit_examples = None

    # Print key configuration
    print("\nKey Configuration:")
    print(f"  Model: {config['model']['name']}")
    print(f"  Base: {config['model']['base_model']}")
    print(f"  Task: {config['model']['task']}")
    print(f"  LoRA: {'Enabled' if config['lora']['enabled'] else 'Disabled'}")
    if config['lora']['enabled']:
        print(f"  LoRA rank: {config['lora']['r']}")
        print(f"  LoRA alpha: {config['lora']['lora_alpha']}")
    print(f"  Learning rate: {config['training']['learning_rate']}")
    print(f"  Epochs: {config['training']['num_epochs']}")
    print(f"  Batch size: {config['training']['per_device_train_batch_size']}")
    print(f"  Gradient accumulation: {config['training']['gradient_accumulation_steps']}")
    print(f"  Effective batch size: {config['training']['per_device_train_batch_size'] * config['training']['gradient_accumulation_steps']}")

    # Setup model and tokenizer
    print("\n" + "=" * 80)
    print("Model Setup")
    print("=" * 80)
    model, tokenizer = setup_model_and_tokenizer(config)

    # Load data
    print("\n" + "=" * 80)
    print("Data Loading")
    print("=" * 80)

    train_file = Path(config['data']['train_file'])
    test_file = Path(config['data']['test_file'])

    print(f"\nDataset statistics:")
    print(f"Train: {get_dataset_stats(train_file)['total']} examples")
    print(f"Test: {get_dataset_stats(test_file)['total']} examples")

    # Create datasets using custom data loader (which handles tokenization)
    # Note: We'll use a simpler approach with Hugging Face datasets
    import json
    from datasets import Dataset

    def load_jsonl_as_hf_dataset(file_path, limit=None):
        """Load JSONL file as Hugging Face Dataset."""
        data = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                item = json.loads(line)
                # Convert expected_output dict to JSON string for PyArrow compatibility
                item['expected_output'] = json.dumps(item['expected_output'], ensure_ascii=False)
                data.append(item)
        return Dataset.from_list(data)

    train_dataset = load_jsonl_as_hf_dataset(train_file, limit=limit_examples)
    test_dataset = load_jsonl_as_hf_dataset(test_file)

    # Split train into train + validation
    if config['data']['validation_split'] > 0:
        split = train_dataset.train_test_split(
            test_size=config['data']['validation_split'],
            seed=config['training']['seed']
        )
        train_dataset = split['train']
        val_dataset = split['test']
        print(f"\nSplit: {len(train_dataset)} train, {len(val_dataset)} validation")
    else:
        val_dataset = None
        print(f"\nUsing all {len(train_dataset)} for training")

    # Format datasets for causal LM
    prompt_template = config['data']['prompt_template']

    def format_example(example):
        """Format example for causal language modeling."""
        prompt = prompt_template.format(prompt=example['prompt'])
        # expected_output is already a JSON string from load_jsonl_as_hf_dataset
        output = example['expected_output']
        full_text = prompt + output

        return {"text": full_text}

    train_dataset = train_dataset.map(format_example, remove_columns=train_dataset.column_names)
    if val_dataset:
        val_dataset = val_dataset.map(format_example, remove_columns=val_dataset.column_names)
    test_dataset = test_dataset.map(format_example, remove_columns=test_dataset.column_names)

    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=config['data']['max_length'],
            padding="max_length"
        )

    print("\nTokenizing datasets...")
    train_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    if val_dataset:
        val_dataset = val_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    test_dataset = test_dataset.map(tokenize_function, batched=True, remove_columns=["text"])

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal LM, not masked LM
    )

    # Training arguments
    print("\n" + "=" * 80)
    print("Training Setup")
    print("=" * 80)

    output_dir = Path(config['output']['output_dir'])
    logging_dir = Path(config['output']['logging_dir'])

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        overwrite_output_dir=config['output']['overwrite_output_dir'],

        # Training hyperparameters
        num_train_epochs=config['training']['num_epochs'],
        per_device_train_batch_size=config['training']['per_device_train_batch_size'],
        per_device_eval_batch_size=config['training']['per_device_eval_batch_size'],
        gradient_accumulation_steps=config['training']['gradient_accumulation_steps'],
        learning_rate=config['training']['learning_rate'],
        weight_decay=config['training']['weight_decay'],
        adam_beta1=config['training']['adam_beta1'],
        adam_beta2=config['training']['adam_beta2'],
        adam_epsilon=config['training']['adam_epsilon'],
        max_grad_norm=config['training']['max_grad_norm'],

        # Learning rate scheduler
        lr_scheduler_type=config['training']['lr_scheduler_type'],
        warmup_ratio=config['training']['warmup_ratio'],

        # Mixed precision
        fp16=config['training']['fp16'],
        bf16=config['training']['bf16'],

        # Checkpointing
        save_strategy=config['training']['save_strategy'],
        save_steps=config['training']['save_steps'],
        save_total_limit=config['training']['save_total_limit'],
        load_best_model_at_end=config['training']['load_best_model_at_end'],
        metric_for_best_model=config['training']['metric_for_best_model'],
        greater_is_better=config['training']['greater_is_better'],

        # Evaluation
        eval_strategy=config['training']['evaluation_strategy'],
        eval_steps=config['training']['eval_steps'],

        # Logging
        logging_dir=str(logging_dir),
        logging_strategy=config['training']['logging_strategy'],
        logging_steps=config['training']['logging_steps'],
        logging_first_step=config['training']['logging_first_step'],
        report_to=config['training']['report_to'],

        # Performance
        dataloader_num_workers=config['training']['dataloader_num_workers'],
        dataloader_pin_memory=config['training']['dataloader_pin_memory'],
        gradient_checkpointing=config['training']['gradient_checkpointing'],

        # Reproducibility
        seed=config['training']['seed'],
        data_seed=config['training']['data_seed'],

        # Disable tqdm for cleaner logs
        disable_tqdm=False,

        # Remove unused columns
        remove_unused_columns=True,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    # Print training info
    print(f"\nOutput directory: {output_dir}")
    print(f"Logging directory: {logging_dir}")
    print(f"Total training steps: {len(train_dataset) // (training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps) * training_args.num_train_epochs}")
    print(f"Checkpoints saved every {config['training']['save_steps']} steps")
    print(f"Evaluation every {config['training']['eval_steps']} steps")

    # Training
    print("\n" + "=" * 80)
    print("Starting Training")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if args.resume_from_checkpoint:
        print(f"Resuming from checkpoint: {args.resume_from_checkpoint}")
        trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
    else:
        trainer.train()

    # Save final model
    print("\n" + "=" * 80)
    print("Saving Final Model")
    print("=" * 80)

    final_output_dir = output_dir / "final_model"
    trainer.save_model(str(final_output_dir))
    tokenizer.save_pretrained(str(final_output_dir))

    print(f"Model saved to {final_output_dir}")

    # Save training metadata
    metadata = {
        "model_name": config['model']['name'],
        "base_model": config['model']['base_model'],
        "training_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "num_epochs": config['training']['num_epochs'],
        "learning_rate": config['training']['learning_rate'],
        "batch_size": config['training']['per_device_train_batch_size'] * config['training']['gradient_accumulation_steps'],
        "train_examples": len(train_dataset),
        "validation_examples": len(val_dataset) if val_dataset else 0,
        "test_examples": len(test_dataset),
        "lora_config": config['lora'] if config['lora']['enabled'] else None,
        "validation_run": args.validation_run
    }

    metadata_path = final_output_dir / "training_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to {metadata_path}")

    # Final evaluation (optional)
    if config['evaluation']['run_full_eval'] and not args.validation_run:
        print("\n" + "=" * 80)
        print("Running Full Evaluation")
        print("=" * 80)
        print("Note: Run eval.py separately for detailed JSON extraction metrics")

        eval_results = trainer.evaluate(test_dataset)
        print(f"Test set evaluation: {eval_results}")

        eval_results_path = final_output_dir / "eval_results.json"
        with open(eval_results_path, 'w') as f:
            json.dump(eval_results, f, indent=2)
        print(f"Evaluation results saved to {eval_results_path}")

    print("\n" + "=" * 80)
    print("Training Complete!")
    print("=" * 80)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nFinal model: {final_output_dir}")
    print("\nNext steps:")
    print("  1. Review training logs in models/mlm_135m_json/logs/")
    print("  2. Run full evaluation: python benchmarks/edge_json/scripts/eval.py")
    print("  3. Check hardware monitor: cat models/mlm_135m_json/logs/hardware_monitor.log")

    return 0


if __name__ == "__main__":
    sys.exit(main())
