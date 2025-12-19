import asyncio
import os
import sys
from pathlib import Path
from typing import Union, List, Dict, Any

# Mocking parts of server.py to test the logic
def _read_file_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# Define roots as they are in the project
base_path = Path("/Users/dujiepeng/AI/mcp-server/easemob-doc-mcp")
DOC_ROOT = base_path / "document"
UIKIT_ROOT = base_path / "uikit"
CALLKIT_ROOT = base_path / "callkit"

async def test_get_document_content(
    doc_paths: Union[str, List[str]] = None,
    keyword: str = ""
) -> Dict[str, Any]:
    try:
        if doc_paths is None:
            doc_paths = []
        elif isinstance(doc_paths, str):
            doc_paths = [doc_paths]
        
        results = []
        total_matches = 0
        
        for doc_path in doc_paths:
            try:
                if doc_path.startswith("uikit/"):
                    full_path = UIKIT_ROOT / doc_path[6:]
                elif doc_path.startswith("callkit/"):
                    full_path = CALLKIT_ROOT / doc_path[8:]
                elif doc_path.startswith("sdk/"):
                    full_path = DOC_ROOT / doc_path[4:]
                else:
                    full_path = DOC_ROOT / doc_path
                
                print(f"DEBUG: Processing {doc_path} -> {full_path}")
                if not full_path.exists():
                    results.append({"error": "文档不存在", "docPath": doc_path})
                    continue
                
                content = await asyncio.to_thread(_read_file_content, str(full_path))
                content = content.replace('\t', '')
                matches = []
                
                if keyword and keyword.strip() != "":
                    lines = content.split('\n')
                    keyword_lower = keyword.lower()
                    for i, line in enumerate(lines):
                        line_no_tabs = line.replace('\t', '')
                        if keyword_lower in line_no_tabs.lower():
                            start = max(0, i - 2)
                            end = min(len(lines) - 1, i + 2)
                            context = '\n'.join([lines[j].replace('\t', '') for j in range(start, end + 1)])
                            matches.append({
                                "lineNumber": i + 1,
                                "context": context,
                                "line": line_no_tabs
                            })
                
                results.append({
                    "content": "CONTENT_TRUNCATED",
                    "docPath": doc_path,
                    "matches": matches
                })
                total_matches += len(matches)
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                results.append({"error": str(e), "docPath": doc_path})
        
        return {"documents": results, "totalMatches": total_matches}
    except Exception as e:
        return {"error": str(e)}

async def main():
    print("--- Test 1: sdk prefix ---")
    res1 = await test_get_document_content(doc_paths=["sdk/flutter/initialization.md"])
    print(f"Result 1: {res1}\n")

    print("--- Test 2: no prefix ---")
    res2 = await test_get_document_content(doc_paths=["flutter/initialization.md"])
    print(f"Result 2: {res2}\n")

if __name__ == "__main__":
    asyncio.run(main())
