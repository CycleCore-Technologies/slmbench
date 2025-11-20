#!/usr/bin/env python3
"""
EdgeJSON Dataset Generator v2.0

Generates high-quality JSON extraction training data using:
- Template-based generation (Faker)
- Teacher committee (Qwen, Mistral, Phi-4)
- Multi-level quality validation
- Stratified sampling and balancing

Target: 1,500 examples → filter to best 1,000 → split 800/200 train/test
"""

import json
import random
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import sys

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from schema_loader import SchemaLoader, SchemaInfo
from template_generator import TemplateGenerator
from teacher_router import TeacherRouter
from vllm_generator import VLLMGenerator, DEFAULT_CONFIGS
from quality_validator import QualityValidator, ValidationStats


@dataclass
class Example:
    """A single training example."""
    id: str
    schema_id: str
    complexity: str
    teacher: str  # "template" or "qwen", "mistral", "phi4"
    source: str   # "template" or "llm"
    prompt: str
    expected_output: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


class DatasetGenerator:
    """Main orchestrator for dataset generation."""

    def __init__(
        self,
        schemas_root: Path,
        output_dir: Path,
        examples_per_schema: int = 60,
        template_ratio: float = 0.5,
        target_total: int = 1000,
        seed: int = 42
    ):
        """
        Initialize dataset generator.

        Args:
            schemas_root: Path to schemas directory
            output_dir: Output directory for generated datasets
            examples_per_schema: Number of examples to generate per schema
            template_ratio: Fraction of examples from templates (0.0-1.0)
            target_total: Target number of examples in final dataset
            seed: Random seed for reproducibility
        """
        self.schemas_root = schemas_root
        self.output_dir = Path(output_dir)
        self.examples_per_schema = examples_per_schema
        self.template_ratio = template_ratio
        self.target_total = target_total
        self.seed = seed

        # Set random seeds
        random.seed(seed)

        # Initialize components
        print("Initializing components...")
        self.schema_loader = SchemaLoader(schemas_root)
        self.template_gen = TemplateGenerator(seed=seed)
        self.teacher_router = TeacherRouter()
        self.vllm_gen = None  # Lazy initialization

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"✓ Loaded {len(self.schema_loader.all_schemas())} schemas")
        print(f"✓ Target: {self.examples_per_schema} examples/schema "
              f"({int(self.template_ratio*100)}% template, "
              f"{int((1-self.template_ratio)*100)}% LLM)")
        print(f"✓ Final dataset size: {self.target_total} examples\n")

    def generate_all(self):
        """Generate complete dataset with template + LLM examples."""
        print("=" * 70)
        print("Phase 1: Template-based Generation (Faker)")
        print("=" * 70)

        template_examples = self._generate_template_examples()
        print(f"\n✓ Generated {len(template_examples)} template examples")

        print("\n" + "=" * 70)
        print("Phase 2: LLM-based Generation (Teacher Committee)")
        print("=" * 70)

        llm_examples = self._generate_llm_examples()
        print(f"\n✓ Generated {len(llm_examples)} LLM examples")

        # Combine all examples
        all_examples = template_examples + llm_examples
        print(f"\n✓ Total raw examples: {len(all_examples)}")

        print("\n" + "=" * 70)
        print("Phase 3: Quality Validation & Filtering")
        print("=" * 70)

        valid_examples = self._validate_and_filter(all_examples)
        print(f"\n✓ Valid examples after filtering: {len(valid_examples)}")

        print("\n" + "=" * 70)
        print("Phase 4: Balancing & Final Selection")
        print("=" * 70)

        final_examples = self._balance_and_select(valid_examples, self.target_total)
        print(f"\n✓ Final dataset size: {len(final_examples)}")

        print("\n" + "=" * 70)
        print("Phase 5: Train/Test Split & Save")
        print("=" * 70)

        self._split_and_save(final_examples)

        print("\n" + "=" * 70)
        print("Dataset Generation Complete!")
        print("=" * 70)

    def _generate_template_examples(self) -> List[Example]:
        """Generate examples using template-based approach (Faker)."""
        examples = []
        schemas = self.schema_loader.all_schemas()

        num_template = int(self.examples_per_schema * self.template_ratio)

        for schema_info in schemas:
            print(f"\nGenerating {num_template} template examples for {schema_info.schema_id}...")

            for i in range(num_template):
                try:
                    prompt, expected = self.template_gen.generate_for_schema(
                        schema_info.schema_id,
                        schema_info.schema
                    )

                    example = Example(
                        id=f"edgejson_{schema_info.schema_id}_template_{i:03d}",
                        schema_id=schema_info.schema_id,
                        complexity=schema_info.complexity,
                        teacher="template",
                        source="template",
                        prompt=prompt,
                        expected_output=expected
                    )
                    examples.append(example)

                except Exception as e:
                    print(f"  Warning: Failed to generate template {i} for {schema_info.schema_id}: {e}")

            print(f"  ✓ Generated {num_template} examples")

        return examples

    def _generate_llm_examples(self) -> List[Example]:
        """Generate examples using LLM teacher committee."""
        examples = []
        schemas = self.schema_loader.all_schemas()

        num_llm = int(self.examples_per_schema * (1 - self.template_ratio))

        # Distribute schemas across teachers
        distribution = self.teacher_router.distribute_schemas(
            [s.schema_id for s in schemas]
        )

        print("\nTeacher Distribution:")
        for teacher_name, schema_ids in distribution.items():
            print(f"  {teacher_name}: {len(schema_ids)} schemas")

        # Initialize vLLM generator
        print("\nInitializing vLLM generator...")
        self.vllm_gen = VLLMGenerator(DEFAULT_CONFIGS, gpu_memory_utilization=0.85)

        # Generate examples per teacher
        for teacher_name, schema_ids in distribution.items():
            if not schema_ids:
                continue

            print(f"\n--- Generating with {teacher_name} ---")

            for schema_id in schema_ids:
                schema_info = self.schema_loader.get(schema_id)

                print(f"\n  Schema: {schema_id} ({schema_info.complexity})")
                print(f"  Generating {num_llm} LLM examples...")

                # Generate prompts using templates first
                prompts = []
                for i in range(num_llm):
                    try:
                        prompt, _ = self.template_gen.generate_for_schema(
                            schema_info.schema_id,
                            schema_info.schema
                        )
                        prompts.append(prompt)
                    except Exception as e:
                        print(f"    Warning: Failed to generate prompt {i}: {e}")

                if not prompts:
                    print(f"    ✗ No valid prompts generated, skipping")
                    continue

                # Generate completions with LLM
                try:
                    completions = self.vllm_gen.generate_json_extractions(
                        model_key=teacher_name,
                        texts=prompts,
                        schema=schema_info.schema,
                        batch_size=8
                    )

                    # Create examples
                    for i, (prompt, completion) in enumerate(zip(prompts, completions)):
                        # Try to parse JSON to get expected_output
                        try:
                            expected = json.loads(completion)
                        except:
                            # If JSON parsing fails, store as string for now
                            # (will be caught by validator)
                            expected = {"_raw": completion}

                        example = Example(
                            id=f"edgejson_{schema_info.schema_id}_{teacher_name}_{i:03d}",
                            schema_id=schema_info.schema_id,
                            complexity=schema_info.complexity,
                            teacher=teacher_name,
                            source="llm",
                            prompt=prompt,
                            expected_output=expected
                        )
                        examples.append(example)

                    print(f"    ✓ Generated {len(completions)} completions")

                except Exception as e:
                    print(f"    ✗ LLM generation failed: {e}")
                    continue

        # Cleanup
        if self.vllm_gen:
            self.vllm_gen.cleanup()

        return examples

    def _validate_and_filter(self, examples: List[Example]) -> List[Example]:
        """Validate all examples and filter out invalid ones."""
        valid_examples = []
        stats_by_schema = defaultdict(ValidationStats)

        print("\nValidating examples...")

        for example in examples:
            # Get schema
            schema_info = self.schema_loader.get(example.schema_id)

            # Create validator
            validator = QualityValidator(schema_info.schema, alignment_threshold=0.3)

            # Validate
            result = validator.validate_pair(
                example.prompt,
                json.dumps(example.expected_output)
            )

            # Track stats
            stats_by_schema[example.schema_id].add(result)

            # Keep if valid
            if result.valid:
                # Update with cleaned JSON
                example.expected_output = result.parsed_json
                valid_examples.append(example)

        # Print validation summary
        print("\nValidation Summary by Schema:")
        print("-" * 70)
        for schema_id, stats in stats_by_schema.items():
            summary = stats.summary()
            print(f"{schema_id:30s} {summary['valid']:3d}/{summary['total']:3d} "
                  f"({summary['pass_rate']:5.1f}%)")

        print("\nOverall Validation:")
        print("-" * 70)
        total_all = sum(s.total for s in stats_by_schema.values())
        valid_all = sum(s.valid for s in stats_by_schema.values())
        pass_rate = (valid_all / total_all * 100) if total_all > 0 else 0
        print(f"Total: {valid_all}/{total_all} ({pass_rate:.1f}% pass rate)")

        return valid_examples

    def _balance_and_select(self, examples: List[Example], target: int) -> List[Example]:
        """Balance examples across schemas and select best N."""
        # Group by schema
        by_schema = defaultdict(list)
        for ex in examples:
            by_schema[ex.schema_id].append(ex)

        # Calculate target per schema (roughly equal)
        num_schemas = len(by_schema)
        per_schema_target = max(1, target // num_schemas)

        print(f"\nTarget per schema: ~{per_schema_target} examples")
        print(f"Balancing across {num_schemas} schemas...")

        selected = []

        for schema_id, schema_examples in by_schema.items():
            # Shuffle and take up to target
            random.shuffle(schema_examples)
            selected.extend(schema_examples[:per_schema_target])

        # If we're under target, add more examples randomly
        if len(selected) < target:
            remaining = [ex for ex in examples if ex not in selected]
            random.shuffle(remaining)
            selected.extend(remaining[:target - len(selected)])

        # If over target, trim
        if len(selected) > target:
            random.shuffle(selected)
            selected = selected[:target]

        # Print distribution
        print("\nFinal Distribution:")
        final_by_schema = defaultdict(int)
        final_by_complexity = defaultdict(int)
        final_by_source = defaultdict(int)

        for ex in selected:
            final_by_schema[ex.schema_id] += 1
            final_by_complexity[ex.complexity] += 1
            final_by_source[ex.source] += 1

        print(f"\nBy Complexity:")
        for complexity in ["simple", "medium", "complex"]:
            count = final_by_complexity[complexity]
            pct = (count / len(selected) * 100) if selected else 0
            print(f"  {complexity:10s}: {count:4d} ({pct:5.1f}%)")

        print(f"\nBy Source:")
        for source in ["template", "llm"]:
            count = final_by_source[source]
            pct = (count / len(selected) * 100) if selected else 0
            print(f"  {source:10s}: {count:4d} ({pct:5.1f}%)")

        return selected

    def _split_and_save(self, examples: List[Example]):
        """Split into train/test and save as JSONL."""
        # Shuffle
        random.shuffle(examples)

        # Split 80/20
        split_idx = int(len(examples) * 0.8)
        train_examples = examples[:split_idx]
        test_examples = examples[split_idx:]

        print(f"\nTrain: {len(train_examples)} examples")
        print(f"Test:  {len(test_examples)} examples")

        # Save train
        train_path = self.output_dir / "edgejson_train_v2.jsonl"
        self._save_jsonl(train_examples, train_path)
        print(f"\n✓ Saved train: {train_path}")

        # Save test
        test_path = self.output_dir / "edgejson_test_v2.jsonl"
        self._save_jsonl(test_examples, test_path)
        print(f"✓ Saved test:  {test_path}")

        # Save metadata
        metadata = {
            "version": "2.0",
            "total_examples": len(examples),
            "train_examples": len(train_examples),
            "test_examples": len(test_examples),
            "num_schemas": len(set(ex.schema_id for ex in examples)),
            "examples_per_schema": self.examples_per_schema,
            "template_ratio": self.template_ratio,
            "seed": self.seed,
            "schemas": list(set(ex.schema_id for ex in examples))
        }

        metadata_path = self.output_dir / "dataset_metadata.json"
        with metadata_path.open("w") as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Saved metadata: {metadata_path}")

    def _save_jsonl(self, examples: List[Example], path: Path):
        """Save examples to JSONL file."""
        with path.open("w") as f:
            for example in examples:
                f.write(json.dumps(example.to_dict(), ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate EdgeJSON dataset v2")
    parser.add_argument(
        "--schemas-root",
        type=Path,
        default=Path(__file__).parent.parent / "schemas",
        help="Path to schemas directory"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent.parent / "data",
        help="Output directory for generated data"
    )
    parser.add_argument(
        "--examples-per-schema",
        type=int,
        default=60,
        help="Number of examples to generate per schema"
    )
    parser.add_argument(
        "--template-ratio",
        type=float,
        default=0.5,
        help="Fraction of examples from templates (0.0-1.0)"
    )
    parser.add_argument(
        "--target-total",
        type=int,
        default=1000,
        help="Target total examples in final dataset"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    # Create generator
    generator = DatasetGenerator(
        schemas_root=args.schemas_root,
        output_dir=args.output_dir,
        examples_per_schema=args.examples_per_schema,
        template_ratio=args.template_ratio,
        target_total=args.target_total,
        seed=args.seed
    )

    # Generate dataset
    generator.generate_all()


if __name__ == "__main__":
    main()
