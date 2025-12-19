import asyncio
import httpx
import json
import sys

async def test_mcp_sse():
    url = "http://localhost:9000/mcp/"
    print(f"Connecting to {url}...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Start SSE session
        async with client.stream("GET", url) as response:
            if response.status_code != 200:
                print(f"Failed to connect: {response.status_code}")
                return

            print("Connected to SSE. Waiting for endpoint event...")
            endpoint_url = None
            session_id = None
            
            async for line in response.aiter_lines():
                if line.startswith("event: endpoint"):
                    continue
                if line.startswith("data: "):
                    endpoint_path = line[6:].strip()
                    endpoint_url = f"http://localhost:9000{endpoint_path}"
                    session_id = endpoint_path.split("session_id=")[1]
                    print(f"Got endpoint: {endpoint_url}")
                    break
            
            if not endpoint_url:
                print("Did not receive endpoint.")
                return

            # 2. Call list_tools
            print("\nCalling list_tools...")
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            res = await client.post(endpoint_url, json=payload)
            print(f"Response ({res.status_code}):")
            print(json.dumps(res.json(), indent=2, ensure_ascii=False))

            # 3. Call search_knowledge_base
            print("\nCalling search_knowledge_base...")
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "search_knowledge_base",
                    "arguments": {
                        "query": "Flutter SDK 初始化"
                    }
                }
            }
            
            res = await client.post(endpoint_url, json=payload)
            print(f"Response ({res.status_code}):")
            result = res.json()
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print("Success! Result keys:", result.get("result", {}).keys())

if __name__ == "__main__":
    asyncio.run(test_mcp_sse())
