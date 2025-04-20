# Frontend Build Stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

# Final Frontend Container
FROM node:20-alpine
WORKDIR /app

# Install ngrok
RUN apk add --no-cache curl jq \
 && curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.tgz | tar -xz -C /usr/local/bin

# Copy app and start-ngrok.sh script
COPY --from=builder /app ./
COPY start-ngrok.sh /app/start-ngrok.sh
RUN chmod +x /app/start-ngrok.sh

EXPOSE 3000

CMD ["sh", "-c", "yarn build && yarn start"]

# Frontend entrypoint
#CMD ["sh", "-c", "chmod +x /app/start-ngrok.sh && /app/start-ngrok.sh"]