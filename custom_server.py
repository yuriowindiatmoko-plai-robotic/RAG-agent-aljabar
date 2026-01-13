"""Custom API server that comprehensively patches Pydantic for ADK compatibility"""
import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# ============================================================================
# COMPREHENSIVE PYDANTIC PATCHING
# ============================================================================

# Patch 1: Handle core schema generation for unknown types
from pydantic._internal._generate_schema import GenerateSchema
from pydantic_core import core_schema
from typing import Any

original_unknown_type_schema = GenerateSchema._unknown_type_schema

def patched_unknown_type_schema(self, obj: Any) -> core_schema.CoreSchema:
    """Patched version that returns a placeholder for ALL problematic types"""
    try:
        # Try original method first
        return original_unknown_type_schema(self, obj)
    except Exception as e:
        # For ANY type that can't be schema-generated, return a generic Any schema
        #  This allows problematic runtime types to pass through without breaking OpenAPI
        return core_schema.any_schema(
            metadata={'pydantic_js_annotation_functions': []},
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: None,
                return_schema=core_schema.none_schema()
            )
        )

GenerateSchema._unknown_type_schema = patched_unknown_type_schema

# Patch 2: Handle JSON schema generation for IsInstance schemas
from pydantic.json_schema import GenerateJsonSchema, JsonSchemaValue
import httpx

class PatchedGenerateJsonSchema(GenerateJsonSchema):
    """Custom schema generator for JSON schemas"""
    
    def handle_invalid_for_json_schema(self, schema: core_schema.CoreSchema, error_info: str) -> JsonSchemaValue:
        """Return placeholder for invalid types"""
        if 'httpx.Client' in error_info or 'ClientSession' in error_info:
            return {'type': 'object', 'additionalProperties': True, 'description': 'Runtime-only client object'}
        return super().handle_invalid_for_json_schema(schema, error_info)
    
    def is_instance_schema(self, schema: core_schema.IsInstanceSchema) -> JsonSchemaValue:
        """Handle IsInstance schemas"""
        cls = schema.get('cls')
        if cls is httpx.Client or (hasattr(cls, '__name__') and 'ClientSession' in cls.__name__):
            return {'type': 'object', 'additionalProperties': True, 'description': 'Runtime client'}
        try:
            return super().is_instance_schema(schema)
        except:
            return {'type': 'object', 'additionalProperties': True}

import pydantic.json_schema
pydantic.json_schema.GenerateJsonSchema = PatchedGenerateJsonSchema

# Patch 3: Monkey-patch mcp.client.session.ClientSession if it exists
try:
    from mcp.client.session import ClientSession
    from pydantic_core import core_schema as cs
    
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Make ClientSession compatible with Pydantic"""
        return cs.any_schema()
    
    ClientSession.__get_pydantic_core_schema__ = classmethod(__get_pydantic_core_schema__)
except ImportError:
    pass  # MCP not installed or not needed

print("=" * 70)
print("🚀 Starting ADK API Server with Comprehensive Pydantic Patches")
print("✅ OpenAPI documentation ENABLED at /docs")
print("=" * 70)

# Now safely import ADK
from google.adk.cli.fast_api import get_fast_api_app
import uvicorn

# Get the FastAPI app from ADK
app = get_fast_api_app(agents_dir=str(project_root), web=False)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

