"""
Teacher Router - Route schemas to appropriate teacher models.

Uses keyword-based heuristics to select the best teacher model for each schema.
No configuration required - fully automatic.
"""

from typing import Literal
from dataclasses import dataclass


TeacherName = Literal["qwen", "mistral", "phi4"]


@dataclass
class TeacherInfo:
    """Information about a teacher model."""
    name: TeacherName
    display_name: str
    specialization: str


class TeacherRouter:
    """
    Route schemas to appropriate teacher models based on content and domain.

    Teacher Specializations:
    - Qwen2.5-14B: General-purpose, broad coverage, long-context
    - Mistral Small 3.1: API responses, function calling, integration schemas
    - Phi-4: Medical, STEM, scientific, reasoning-heavy schemas
    """

    TEACHERS = {
        "qwen": TeacherInfo(
            name="qwen",
            display_name="Qwen2.5-14B-Instruct",
            specialization="General-purpose JSON extraction"
        ),
        "mistral": TeacherInfo(
            name="mistral",
            display_name="Mistral Small 3.1-24B",
            specialization="API responses, function calling"
        ),
        "phi4": TeacherInfo(
            name="phi4",
            display_name="Phi-4 14B",
            specialization="Medical, STEM, reasoning"
        ),
    }

    # Keywords for routing
    MISTRAL_KEYWORDS = [
        "api", "response", "request", "endpoint", "webhook",
        "function", "call", "integration", "service", "rest",
        "graphql", "rpc", "notification", "event"
    ]

    PHI4_KEYWORDS = [
        "medical", "patient", "diagnosis", "clinical", "health",
        "lab", "result", "treatment", "prescription", "doctor",
        "scientific", "research", "experiment", "analytics",
        "iot", "device", "sensor", "telemetry", "network"
    ]

    def __init__(self, default_teacher: TeacherName = "qwen"):
        """
        Initialize teacher router.

        Args:
            default_teacher: Default teacher to use when no specific match found
        """
        self.default_teacher = default_teacher

    def pick_teacher(self, schema_id: str, complexity: str = "medium") -> TeacherName:
        """
        Pick the best teacher model for a given schema.

        NOTE: Currently using only Qwen due to VRAM constraints.
        Mistral Small 3.1 (42GB unquantized) and Phi-4 (28GB unquantized) are too large for 16GB GPU.
        Original routing logic preserved below for future use with quantized versions.

        Args:
            schema_id: Schema identifier (e.g., "api_response", "medical_record")
            complexity: Schema complexity level ("simple", "medium", "complex")

        Returns:
            Name of the selected teacher model
        """
        # Temporarily use only Qwen for all schemas
        # TODO: Re-enable when AWQ/GPTQ quantized versions of Mistral/Phi-4 are available
        return "qwen"

        # Original routing logic (disabled due to VRAM constraints):
        # schema_lower = schema_id.lower()
        # if any(keyword in schema_lower for keyword in self.MISTRAL_KEYWORDS):
        #     return "mistral"
        # if any(keyword in schema_lower for keyword in self.PHI4_KEYWORDS):
        #     return "phi4"
        # return self.default_teacher

    def get_teacher_info(self, teacher_name: TeacherName) -> TeacherInfo:
        """Get information about a teacher model."""
        return self.TEACHERS[teacher_name]

    def distribute_schemas(self, schema_ids: list[str]) -> dict[TeacherName, list[str]]:
        """
        Distribute schemas across teachers for balanced generation.

        Args:
            schema_ids: List of schema identifiers

        Returns:
            Dictionary mapping teacher names to lists of schema IDs
        """
        distribution = {
            "qwen": [],
            "mistral": [],
            "phi4": [],
        }

        for schema_id in schema_ids:
            teacher = self.pick_teacher(schema_id)
            distribution[teacher].append(schema_id)

        return distribution

    def summary(self, schema_ids: list[str]) -> dict:
        """
        Get a summary of how schemas would be distributed.

        Args:
            schema_ids: List of schema identifiers

        Returns:
            Summary dictionary with counts and lists per teacher
        """
        distribution = self.distribute_schemas(schema_ids)

        summary = {
            "total_schemas": len(schema_ids),
            "teachers": {}
        }

        for teacher_name, schemas in distribution.items():
            teacher_info = self.get_teacher_info(teacher_name)
            summary["teachers"][teacher_name] = {
                "display_name": teacher_info.display_name,
                "specialization": teacher_info.specialization,
                "schema_count": len(schemas),
                "schemas": schemas
            }

        return summary


if __name__ == "__main__":
    # Test the router
    from pathlib import Path
    import json
    from schema_loader import SchemaLoader

    schemas_root = Path(__file__).parent.parent.parent / "schemas"
    loader = SchemaLoader(schemas_root)
    router = TeacherRouter()

    print("Testing TeacherRouter with all schemas:\n")
    print("=" * 70)

    # Get all schema IDs
    schema_ids = [s.schema_id for s in loader.all_schemas()]

    # Get distribution summary
    summary = router.summary(schema_ids)

    print(f"Total Schemas: {summary['total_schemas']}\n")

    for teacher_name, info in summary["teachers"].items():
        print(f"{info['display_name']} ({teacher_name})")
        print(f"  Specialization: {info['specialization']}")
        print(f"  Schema Count: {info['schema_count']}")
        print(f"  Schemas:")
        for schema_id in info["schemas"]:
            print(f"    - {schema_id}")
        print()

    # Test individual routing
    print("=" * 70)
    print("\nIndividual Routing Tests:\n")

    test_cases = [
        "api_response",
        "medical_record",
        "contact_info",
        "iot_device_network",
        "notification",
        "patient_lab_result"
    ]

    for schema_id in test_cases:
        try:
            schema_info = loader.get(schema_id)
            teacher = router.pick_teacher(schema_info.schema_id, schema_info.complexity)
            teacher_info = router.get_teacher_info(teacher)
            print(f"{schema_id} ({schema_info.complexity})")
            print(f"  → {teacher_info.display_name} ({teacher})")
            print(f"  Reason: {teacher_info.specialization}")
            print()
        except KeyError:
            print(f"{schema_id} - Schema not found")
            print()
