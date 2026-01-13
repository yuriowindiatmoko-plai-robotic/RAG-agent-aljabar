#!/bin/bash
# Quick test script for Food Analyst Agent

echo "=== Creating Food Analyst Session ==="
SESSION_RESPONSE=$(curl -s -X POST http://localhost:8000/apps/food_analyst_agent_adk/users/demo_user/sessions \
  -H "Content-Type: application/json" \
  -d '{"systemInstruction": {"parts": [{"text": "You are a helpful food analyst."}]}}')

SESSION_ID=$(echo $SESSION_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Session created: $SESSION_ID"
echo ""

echo "=== Asking: Rekomendasi menu tinggi protein untuk muscle building ==="
echo ""

curl -s -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d "{
    \"appName\": \"food_analyst_agent_adk\",
    \"userId\": \"demo_user\",
    \"sessionId\": \"$SESSION_ID\",
    \"newMessage\": {
      \"role\": \"user\",
      \"parts\": [{\"text\": \"Rekomendasi menu tinggi protein untuk muscle building\"}]
    }
  }" > /tmp/agent_response.json

echo "⏳ Waiting for agent response..."
sleep 3

echo ""
echo "=== Agent's Response ==="
echo ""

curl -s -X GET "http://localhost:8000/apps/food_analyst_agent_adk/users/demo_user/sessions/$SESSION_ID" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for event in data['events']:
    if 'content' in event and 'parts' in event['content']:
        for part in event['content']['parts']:
            if 'text' in part and event['content'].get('role') == 'model':
                print(part['text'])
                print()
"

echo ""
echo "=== Session Details ==="
echo "Session ID: $SESSION_ID"
echo "View at: http://localhost:8000/docs"
