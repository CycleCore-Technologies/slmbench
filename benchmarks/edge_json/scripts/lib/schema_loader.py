"""
Schema Loader - Auto-discover and load JSON schemas from directory structure.

Automatically detects complexity level (simple/medium/complex) from directory.
No YAML config required.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class SchemaInfo:
    """Information about a JSON schema."""
    schema_id: str
    schema: Dict[str, Any]
    complexity: str  # "simple" | "medium" | "complex"
    path: Path

    def __repr__(self):
        return f"SchemaInfo({self.schema_id}, {self.complexity})"


class SchemaLoader:
    """
    Load JSON schemas from directory structure.

    Auto-detects complexity from directory name (simple/medium/complex).
    """

    def __init__(self, schemas_root: Path):
        """
        Initialize schema loader.

        Args:
            schemas_root: Path to schemas directory (contains simple/, medium/, complex/)
        """
        self.schemas_root = Path(schemas_root)
        self._schemas: List[SchemaInfo] = []
        self._load()

    def _load(self):
        """Load all schemas from directory structure."""
        complexities = ["simple", "medium", "complex"]

        for complexity in complexities:
            complexity_dir = self.schemas_root / complexity
            if not complexity_dir.exists():
                continue

            # Load all .json files in this complexity directory
            for schema_file in complexity_dir.glob("*.json"):
                schema_id = schema_file.stem  # filename without .json extension

                try:
                    with schema_file.open() as f:
                        schema = json.load(f)

                    self._schemas.append(SchemaInfo(
                        schema_id=schema_id,
                        schema=schema,
                        complexity=complexity,
                        path=schema_file
                    ))
                except Exception as e:
                    print(f"Warning: Failed to load {schema_file}: {e}")

    def all_schemas(self) -> List[SchemaInfo]:
        """Return all loaded schemas."""
        return self._schemas

    def get(self, schema_id: str) -> SchemaInfo:
        """Get schema by ID."""
        for schema in self._schemas:
            if schema.schema_id == schema_id:
                return schema
        raise KeyError(f"Schema not found: {schema_id}")

    def by_complexity(self, complexity: str) -> List[SchemaInfo]:
        """Get all schemas of a given complexity level."""
        return [s for s in self._schemas if s.complexity == complexity]

    def summary(self) -> Dict[str, int]:
        """Get summary of loaded schemas."""
        summary = {
            "total": len(self._schemas),
            "simple": len(self.by_complexity("simple")),
            "medium": len(self.by_complexity("medium")),
            "complex": len(self.by_complexity("complex")),
        }
        return summary


if __name__ == "__main__":
    # Test the loader
    schemas_root = Path(__file__).parent.parent.parent / "schemas"
    loader = SchemaLoader(schemas_root)

    print(f"Loaded {len(loader.all_schemas())} schemas:")
    print(f"Summary: {loader.summary()}")

    for schema_info in loader.all_schemas():
        print(f"  - {schema_info}")
