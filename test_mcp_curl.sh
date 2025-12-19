#!/bin/bash
URL="http://localhost:9000/mcp/"
echo "Step 1: Get SSE endpoint"
RESP=$(curl -s $URL | grep "data: ")
ENDPOINT=$(echo $RESP | sed 's/data: //')
echo "Endpoint: $ENDPOINT"

if [ -z "$ENDPOINT" ]; then
  echo "Failed to get endpoint"
  exit 1
fi

FULL_URL="http://localhost:9000$ENDPOINT"
echo "Step 2: List tools via POST to $FULL_URL"
curl -s -X POST "$FULL_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | json_pp || curl -s -X POST "$FULL_URL" -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
