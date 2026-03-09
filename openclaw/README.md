# OpenClaw Slack Bot

A containerized Slack bot based on your manifest configuration.

## Setup

1. Copy `.env.example` to `.env` and add your tokens:
   ```bash
   cp .env.example .env
   ```

2. Get your tokens from Slack:
   - SLACK_BOT_TOKEN: OAuth & Permissions → Bot User OAuth Token
   - SLACK_APP_TOKEN: Basic Information → App-Level Tokens (create one with `connections:write` scope)

3. Build and run:
   ```bash
   docker-compose up --build
   ```

## Features

- Responds to @mentions
- Handles direct messages
- `/openclaw` slash command
- Socket mode enabled (no public URL needed)

## Stop the container

```bash
docker-compose down
```
