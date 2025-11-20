"""
Template Generator - Generate realistic synthetic data using Faker.

Uses generic field name matching to map schema fields to Faker functions.
No YAML config required - fully automatic.
"""

from typing import Dict, Any, Tuple, Optional
from faker import Faker
from datetime import datetime
import random
import re


class TemplateGenerator:
    """
    Generate (prompt, expected_output) pairs using Faker library.

    Maps schema field names to appropriate Faker functions automatically.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize template generator.

        Args:
            seed: Random seed for reproducibility (optional)
        """
        self.fake = Faker()
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

    def generate_for_schema(self, schema_id: str, schema: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a synthetic example for a given schema.

        Args:
            schema_id: Identifier for the schema
            schema: JSON schema definition

        Returns:
            Tuple of (prompt_text, expected_output_json)
        """
        # Generate the expected output first
        expected_output = self._generate_object(schema)

        # Generate a natural language prompt from the data
        prompt = self._generate_prompt(schema_id, expected_output, schema)

        return prompt, expected_output

    def _generate_object(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a JSON object matching the schema."""
        if schema.get("type") != "object":
            raise ValueError("Top-level schema must be type 'object'")

        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        additional_allowed = schema.get("additionalProperties", True)

        obj = {}

        for prop_name, prop_schema in properties.items():
            # Always generate required fields, randomly include others
            if prop_name in required or random.random() > 0.3:
                value = self._generate_value(prop_name, prop_schema)
                if value is not None:  # None means skip this field
                    obj[prop_name] = value

        return obj

    def _generate_value(self, field_name: str, schema: Dict[str, Any]) -> Any:
        """Generate a value for a specific field based on its schema."""
        field_type = schema.get("type")
        field_format = schema.get("format")
        field_enum = schema.get("enum")

        # Handle enum first (highest priority)
        if field_enum:
            return random.choice(field_enum)

        # Handle by type
        if field_type == "string":
            return self._generate_string(field_name, schema, field_format)
        elif field_type == "integer":
            return self._generate_integer(field_name, schema)
        elif field_type == "number":
            return self._generate_number(field_name, schema)
        elif field_type == "boolean":
            return random.choice([True, False])
        elif field_type == "array":
            return self._generate_array(field_name, schema)
        elif field_type == "object":
            return self._generate_nested_object(field_name, schema)
        elif field_type == "null":
            return None
        else:
            # No type specified or unknown type
            return self._generate_string(field_name, schema, field_format)

    def _generate_string(self, field_name: str, schema: Dict[str, Any], field_format: Optional[str]) -> str:
        """Generate a string value based on field name and format."""
        field_lower = field_name.lower()

        # Handle format hints first
        if field_format == "email":
            return self.fake.email()
        elif field_format == "uri" or field_format == "url":
            return self.fake.url()
        elif field_format == "date":
            return self.fake.date()
        elif field_format == "date-time":
            return self.fake.iso8601()
        elif field_format == "time":
            return self.fake.time()

        # Handle pattern if specified
        pattern = schema.get("pattern")
        if pattern and "phone" not in field_lower:  # Skip regex for phone (use Faker instead)
            # For simple patterns, try to generate matching values
            if pattern in ["^[+]?[0-9\\-\\s()]+$", "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"]:
                return self.fake.phone_number()

        # Field name-based heuristics
        if "email" in field_lower:
            return self.fake.email()
        elif "phone" in field_lower or "tel" in field_lower:
            return self.fake.phone_number()
        elif "url" in field_lower or "website" in field_lower or "link" in field_lower:
            return self.fake.url()
        elif "address" in field_lower:
            return self.fake.address()
        elif "street" in field_lower:
            return self.fake.street_address()
        elif "city" in field_lower:
            return self.fake.city()
        elif "state" in field_lower or "province" in field_lower:
            return self.fake.state()
        elif "country" in field_lower:
            return self.fake.country()
        elif "zip" in field_lower or "postal" in field_lower:
            return self.fake.zipcode()
        elif "name" in field_lower:
            if "first" in field_lower:
                return self.fake.first_name()
            elif "last" in field_lower:
                return self.fake.last_name()
            elif "company" in field_lower or "organization" in field_lower or "vendor" in field_lower:
                return self.fake.company()
            else:
                return self.fake.name()
        elif "company" in field_lower or "organization" in field_lower:
            return self.fake.company()
        elif "job" in field_lower or "title" in field_lower or "position" in field_lower:
            return self.fake.job()
        elif "date" in field_lower:
            return self.fake.date()
        elif "time" in field_lower:
            return self.fake.time()
        elif "description" in field_lower or "comment" in field_lower or "note" in field_lower:
            return self.fake.sentence(nb_words=random.randint(5, 15))
        elif "message" in field_lower or "text" in field_lower or "content" in field_lower:
            return self.fake.paragraph(nb_sentences=random.randint(2, 4))
        elif "id" in field_lower or "uuid" in field_lower:
            return self.fake.uuid4()
        elif "color" in field_lower:
            return self.fake.color_name()
        elif "username" in field_lower or "user" in field_lower:
            return self.fake.user_name()
        elif "password" in field_lower:
            return self.fake.password()
        elif "domain" in field_lower:
            return self.fake.domain_name()
        elif "ip" in field_lower:
            return self.fake.ipv4()
        elif "mac" in field_lower:
            return self.fake.mac_address()
        elif "currency" in field_lower:
            return random.choice(["USD", "EUR", "GBP", "JPY", "CAD", "AUD"])
        elif "status" in field_lower:
            return random.choice(["active", "inactive", "pending", "completed"])
        elif "type" in field_lower or "category" in field_lower:
            return random.choice(["standard", "premium", "basic", "advanced"])
        elif "version" in field_lower:
            return f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 20)}"
        else:
            # Generic fallback
            return self.fake.word().capitalize()

    def _generate_integer(self, field_name: str, schema: Dict[str, Any]) -> int:
        """Generate an integer value."""
        minimum = schema.get("minimum", 0)
        maximum = schema.get("maximum", 1000)

        field_lower = field_name.lower()

        # Context-specific ranges
        if "age" in field_lower:
            return random.randint(18, 90)
        elif "year" in field_lower:
            return random.randint(2020, 2025)
        elif "month" in field_lower:
            return random.randint(1, 12)
        elif "day" in field_lower:
            return random.randint(1, 28)
        elif "hour" in field_lower:
            return random.randint(0, 23)
        elif "minute" in field_lower or "second" in field_lower:
            return random.randint(0, 59)
        elif "count" in field_lower or "total" in field_lower or "quantity" in field_lower:
            return random.randint(1, 100)
        elif "port" in field_lower:
            return random.randint(1024, 65535)
        elif "percentage" in field_lower or "percent" in field_lower:
            return random.randint(0, 100)
        else:
            return random.randint(minimum, min(maximum, 10000))

    def _generate_number(self, field_name: str, schema: Dict[str, Any]) -> float:
        """Generate a number (float) value."""
        minimum = schema.get("minimum", 0.0)
        maximum = schema.get("maximum", 1000.0)

        field_lower = field_name.lower()

        # Context-specific ranges
        if "price" in field_lower or "amount" in field_lower or "cost" in field_lower:
            return round(random.uniform(10.0, 5000.0), 2)
        elif "rate" in field_lower or "percentage" in field_lower:
            return round(random.uniform(0.0, 100.0), 2)
        elif "temperature" in field_lower:
            return round(random.uniform(-20.0, 40.0), 1)
        elif "latitude" in field_lower:
            return round(random.uniform(-90.0, 90.0), 6)
        elif "longitude" in field_lower:
            return round(random.uniform(-180.0, 180.0), 6)
        else:
            return round(random.uniform(minimum, min(maximum, 10000.0)), 2)

    def _generate_array(self, field_name: str, schema: Dict[str, Any]) -> list:
        """Generate an array value."""
        items_schema = schema.get("items", {})
        min_items = schema.get("minItems", 1)
        max_items = schema.get("maxItems", 5)

        # Generate random number of items
        count = random.randint(min_items, min(max_items, 5))

        array = []
        for i in range(count):
            value = self._generate_value(f"{field_name}_item", items_schema)
            if value is not None:
                array.append(value)

        return array

    def _generate_nested_object(self, field_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a nested object."""
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))

        obj = {}
        for prop_name, prop_schema in properties.items():
            if prop_name in required or random.random() > 0.4:
                value = self._generate_value(prop_name, prop_schema)
                if value is not None:
                    obj[prop_name] = value

        return obj

    def _generate_prompt(self, schema_id: str, data: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """
        Generate a natural language prompt from the generated data.

        This creates a realistic text that a user might provide when asking
        for JSON extraction.
        """
        title = schema.get("title", schema_id.replace("_", " ").title())
        description = schema.get("description", "")

        # Build a natural language representation of the data
        lines = []

        # Add a context-appropriate header
        if "invoice" in schema_id or "order" in schema_id:
            lines.append(f"=== {title} ===")
        elif "report" in schema_id or "analytics" in schema_id:
            lines.append(f"{title} Report")
        elif "record" in schema_id or "entry" in schema_id:
            lines.append(f"New {title}")
        else:
            lines.append(title)

        lines.append("")

        # Convert data to natural text
        self._data_to_text(data, lines, indent=0)

        # Add extraction instruction
        lines.append("")
        lines.append(f"Please extract the {title.lower()} information as JSON.")

        return "\n".join(lines)

    def _data_to_text(self, data: Any, lines: list, indent: int = 0):
        """Convert structured data to natural text format."""
        prefix = "  " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                label = key.replace("_", " ").title()
                if isinstance(value, dict):
                    lines.append(f"{prefix}{label}:")
                    self._data_to_text(value, lines, indent + 1)
                elif isinstance(value, list):
                    lines.append(f"{prefix}{label}:")
                    for item in value:
                        self._data_to_text(item, lines, indent + 1)
                else:
                    lines.append(f"{prefix}{label}: {value}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    lines.append(f"{prefix}- ")
                    self._data_to_text(item, lines, indent + 1)
                else:
                    lines.append(f"{prefix}- {item}")
        else:
            lines.append(f"{prefix}{data}")


if __name__ == "__main__":
    # Test the generator
    from pathlib import Path
    import json
    from schema_loader import SchemaLoader

    schemas_root = Path(__file__).parent.parent.parent / "schemas"
    loader = SchemaLoader(schemas_root)
    generator = TemplateGenerator(seed=42)

    print("Testing TemplateGenerator with sample schemas:\n")

    # Test with a few schemas
    test_schemas = ["contact_info", "product_info", "order_details"]

    for schema_id in test_schemas:
        try:
            schema_info = loader.get(schema_id)
            prompt, expected = generator.generate_for_schema(schema_info.schema_id, schema_info.schema)

            print(f"{'='*60}")
            print(f"Schema: {schema_id} ({schema_info.complexity})")
            print(f"{'='*60}")
            print("\nPROMPT:")
            print(prompt)
            print("\nEXPECTED OUTPUT:")
            print(json.dumps(expected, indent=2, ensure_ascii=False))
            print("\n")
        except Exception as e:
            print(f"Error testing {schema_id}: {e}")
