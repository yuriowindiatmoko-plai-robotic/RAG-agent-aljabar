# RAG Agent API Server

## Quick Start

```bash
# Start the server
# activate the venv
python custom_server.py
```

The server will start on `http://127.0.0.1:8000` with full Swagger UI documentation enabled.

## Accessing the Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **OpenAPI Spec**: http://127.0.0.1:8000/openapi.json

## Why the Custom Server?

The standard `adk api_server` command fails due to Pydantic schema generation errors with runtime-only types (`httpx.Client`, `ClientSession`, `PIL.Image`).

The `custom_server.py` patches Pydantic dynamically to handle these types, enabling full OpenAPI documentation support.

## What's Different?

- ✅ Same RAG agent functionality
- ✅ Full Swagger UI at `/docs`
- ✅ Complete API documentation
- ⚠️ Must use `custom_server.py` instead of `adk api_server`
