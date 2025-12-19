import asyncio
import os
import sys
from pathlib import Path

# Mock the environment
os.environ["MCP_DEBUG"] = "1"

# Import the actual function
sys.path.append(os.getcwd())
from src.server import get_document_content

async def test():
    print("Testing with flutter/initialization.md (expecting content or error)")
    try:
        # Simulate tool call without keyword
        res = await get_document_content(doc_paths=["flutter/initialization.md"])
        print(f"Result: {res}")
    except Exception as e:
        print(f"Caught Exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test())
