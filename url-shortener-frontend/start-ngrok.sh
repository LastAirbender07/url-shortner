#!/bin/sh

echo "🔄 Starting frontend ngrok tunnel setup..."

# Step 1: Configure ngrok auth token
echo "🔐 Adding ngrok auth token..."
ngrok config add-authtoken "$NGROK_AUTHTOKEN"

# Step 2: Start ngrok tunnel on port 3000
echo "🚀 Starting ngrok tunnel on port 3000..."
ngrok http 3000 > /dev/null &

# Step 3: Wait for ngrok to initialize
echo "⏳ Waiting for ngrok to initialize..."
sleep 5

# Step 4: Fetch public URL from ngrok API
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Step 5: Error handling if URL couldn't be fetched
if [ -z "$NGROK_URL" ]; then
    echo "❌ ERROR: Could not retrieve ngrok URL!"
    exit 1
fi

# Step 6: Write to .env.local file
echo "💾 Writing ngrok URL to .env.local as NEXT_PUBLIC_FRONTEND_URL"
echo "NEXT_PUBLIC_FRONTEND_URL=${NGROK_URL}" > /app/.env.local

# Step 7: Print confirmation
echo "✅ Frontend exposed via ngrok at: ${NGROK_URL}"
echo "📄 Current contents of /app/.env.local:"
cat /app/.env.local

# Step 8: Start React frontend
echo "🚀 Starting React frontend (yarn start)..."
yarn start
