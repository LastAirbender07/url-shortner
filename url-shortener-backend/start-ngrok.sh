#!/bin/sh
ngrok config add-authtoken "$NGROK_AUTHTOKEN"
ngrok http 8000 > /dev/null &

sleep 5

NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ]; then
    echo "❌ Ngrok URL not retrieved! Exiting."
    exit 1
fi

# Ensure the frontend folder exists
if [ ! -d "/app/url-shortener-frontend" ]; then
    echo "❌ Frontend directory does not exist! Skipping env update."
    exit 1
fi

echo "NEXT_PUBLIC_API_URL=${NGROK_URL}" > /app/url-shortener-frontend/.env.local
echo "✅ Wrote API URL to /app/url-shortener-frontend/.env.local"
cat /app/url-shortener-frontend/.env.local

echo "✅ Backend exposed at: ${NGROK_URL}"

# Start backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
