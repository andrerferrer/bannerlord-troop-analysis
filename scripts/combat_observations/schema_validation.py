from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping

from .domain import DomainError, read_jsonl


def _type_matches(value: object, expected: str) -> bool:
    return {
        "null": value is None,
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }.get(expected, True)


def validate_value(value: object, schema: Mapping[str, object], path: str = "$") -> list[str]:
    errors: list[str] = []
    schema_type = schema.get("type")
    if schema_type:
        accepted = [schema_type] if isinstance(schema_type, str) else list(schema_type)
        if not any(_type_matches(value, str(expected)) for expected in accepted):
            return [f"{path}: expected type {accepted}, got {type(value).__name__}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in enum")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and not re.search(str(schema["pattern"]), value):
            errors.append(f"{path}: string does not match pattern")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value is above maximum")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            errors.append(f"{path}: array has too few items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: array items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_value(item, item_schema, f"{path}[{index}]"))
    if isinstance(value, dict):
        required = schema.get("required", [])
        for field in required if isinstance(required, list) else []:
            if field not in value:
                errors.append(f"{path}.{field}: required property is missing")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for field, child_schema in properties.items():
                if field in value and isinstance(child_schema, dict):
                    errors.extend(validate_value(value[field], child_schema, f"{path}.{field}"))
            if schema.get("additionalProperties") is False:
                extra = sorted(set(value) - set(properties))
                for field in extra:
                    errors.append(f"{path}.{field}: additional property is not allowed")
    return errors


def load_schema(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DomainError(f"invalid JSON Schema {path}: {error}") from error
    if not isinstance(value, dict) or value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise DomainError(f"{path}: expected a draft 2020-12 JSON Schema")
    return value


def validate_jsonl_file(data_path: Path, schema_path: Path) -> list[dict[str, object]]:
    schema = load_schema(schema_path)
    errors = []
    for index, record in enumerate(read_jsonl(data_path), 1):
        for error in validate_value(record, schema):
            errors.append({"file": data_path.name, "line": index, "error": error})
    return errors
