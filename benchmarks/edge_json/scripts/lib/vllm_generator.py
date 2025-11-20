"""
vLLM Generator - Wrapper for batched LLM inference using vLLM.

Loads one model at a time and performs batched generation for efficiency.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class ModelConfig:
    """Configuration for a teacher model."""
    name: str              # Short name: "qwen", "mistral", "phi4"
    model_path: str        # Path to model directory or HF repo
    max_tokens: int = 512
    temperature: float = 0.4
    top_p: float = 0.95


# Prompt template for JSON extraction
JSON_EXTRACTION_TEMPLATE = """You are a careful data extraction system.
You will be given a piece of unstructured or semi-structured text and a JSON schema.
Your job is to extract the relevant information and return a JSON object that strictly follows the schema.

RULES:
- Do not include any extra keys not in the schema.
- Use null for fields that cannot be determined.
- Use realistic values consistent with the input text.
- Output ONLY the JSON object, no extra text, no markdown code blocks.

JSON SCHEMA:
{schema_json}

INPUT TEXT:
{text}

JSON OUTPUT:"""


class VLLMGenerator:
    """
    Wrapper for vLLM-based generation.

    Loads one model at a time to conserve VRAM, performs batched generation.
    """

    def __init__(self, configs: Dict[str, ModelConfig], gpu_memory_utilization: float = 0.9):
        """
        Initialize vLLM generator.

        Args:
            configs: Dictionary mapping model names to ModelConfig objects
            gpu_memory_utilization: Fraction of GPU memory to use (0.0-1.0)
        """
        self.configs = configs
        self.gpu_memory_utilization = gpu_memory_utilization
        self.llm = None
        self.current_model_name: Optional[str] = None

    def _ensure_model_loaded(self, model_key: str):
        """Load the requested model if not already loaded."""
        if self.current_model_name == model_key and self.llm is not None:
            print(f"  Model {model_key} already loaded, reusing...")
            return

        # Unload previous model
        if self.llm is not None:
            print(f"  Unloading previous model: {self.current_model_name}")
            del self.llm
            self.llm = None

        # Load new model
        cfg = self.configs[model_key]
        print(f"  Loading {cfg.name}: {cfg.model_path}")

        try:
            from vllm import LLM
            self.llm = LLM(
                model=cfg.model_path,
                dtype="auto",
                gpu_memory_utilization=self.gpu_memory_utilization,
                tensor_parallel_size=1,
                max_model_len=2048,
                max_num_seqs=16,     # Conservative batch size
                enforce_eager=True,  # Disable CUDA graphs for memory efficiency
            )
            self.current_model_name = model_key
            print(f"  ✓ {cfg.name} loaded successfully")
        except Exception as e:
            print(f"  ✗ Failed to load {cfg.name}: {e}")
            raise

    def generate(self, model_key: str, prompts: List[str], batch_size: int = 8) -> List[str]:
        """
        Generate completions for a batch of prompts.

        Args:
            model_key: Name of the model to use (must be in configs)
            prompts: List of prompt strings
            batch_size: Number of prompts to process in parallel

        Returns:
            List of generated text completions
        """
        self._ensure_model_loaded(model_key)
        cfg = self.configs[model_key]

        try:
            from vllm import SamplingParams

            sampling_params = SamplingParams(
                temperature=cfg.temperature,
                top_p=cfg.top_p,
                max_tokens=cfg.max_tokens,
                stop=["\n\n\n", "```"]  # Stop on triple newlines or markdown code blocks
            )

            # Process all prompts (vLLM handles batching internally)
            print(f"  Generating {len(prompts)} completions with {cfg.name}...")
            outputs = self.llm.generate(prompts, sampling_params)

            # Extract text from outputs
            completions = []
            for out in outputs:
                text = out.outputs[0].text.strip()
                completions.append(text)

            print(f"  ✓ Generated {len(completions)} completions")
            return completions

        except Exception as e:
            print(f"  ✗ Generation failed: {e}")
            raise

    def generate_json_extractions(
        self,
        model_key: str,
        texts: List[str],
        schema: Dict[str, Any],
        batch_size: int = 8
    ) -> List[str]:
        """
        Generate JSON extractions for a list of input texts.

        Args:
            model_key: Name of the model to use
            texts: List of input texts to extract from
            schema: JSON schema that outputs should conform to
            batch_size: Batch size for generation

        Returns:
            List of generated JSON strings (not yet parsed)
        """
        # Build prompts for all texts
        schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
        prompts = []

        for text in texts:
            prompt = JSON_EXTRACTION_TEMPLATE.format(
                schema_json=schema_json,
                text=text
            )
            prompts.append(prompt)

        # Generate completions
        return self.generate(model_key, prompts, batch_size)

    def cleanup(self):
        """Unload current model and free GPU memory."""
        if self.llm is not None:
            print(f"  Cleaning up {self.current_model_name}...")
            del self.llm
            self.llm = None
            self.current_model_name = None


# Default model configurations
# NOTE: Using only Qwen2.5-14B-AWQ for all schemas due to VRAM constraints
# Mistral Small 3.1-24B (42GB) and Phi-4 14B (28GB) are unquantized and too large for 16GB GPU
DEFAULT_CONFIGS = {
    "qwen": ModelConfig(
        name="qwen",
        model_path="/home/rain/SLMBench/models/qwen2.5-14b-awq",
        max_tokens=512,
        temperature=0.4,
        top_p=0.95
    ),
    # Disabled due to VRAM constraints (unquantized models):
    # "mistral": ModelConfig(name="mistral", model_path="/home/rain/SLMBench/models/mistral-small-24b", ...),
    # "phi4": ModelConfig(name="phi4", model_path="/home/rain/SLMBench/models/phi-4", ...),
}


if __name__ == "__main__":
    # Test the generator (requires models to be downloaded)
    import sys

    print("VLLMGenerator Test")
    print("=" * 70)
    print("\nThis test requires models to be downloaded.")
    print("Model paths:")
    for name, cfg in DEFAULT_CONFIGS.items():
        path = Path(cfg.model_path)
        exists = "✓" if path.exists() else "✗"
        print(f"  {exists} {name}: {cfg.model_path}")

    print("\nTo run a live test, ensure models are downloaded.")
    print("Skipping live generation test for now.")

    # Test prompt formatting
    print("\n" + "=" * 70)
    print("Testing prompt template formatting:\n")

    test_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "email"]
    }

    test_text = "Contact: John Doe (john@example.com)"

    schema_json = json.dumps(test_schema, indent=2)
    prompt = JSON_EXTRACTION_TEMPLATE.format(
        schema_json=schema_json,
        text=test_text
    )

    print(prompt)
    print("\n" + "=" * 70)
    print("Prompt template test complete.")
