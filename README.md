# Slack MCP Server

A Python server that implements the Message Control Protocol (MCP) for integrating Slack with Minecraft servers.

## Overview

This server acts as a bridge between Slack and Minecraft, allowing:

- Sending messages from Slack to Minecraft
- Receiving messages from Minecraft and forwarding them to Slack
- Executing Minecraft commands from Slack

## Requirements

- Python 3.12+
- Poetry (for dependency management)
- Slack Bot Token
- Minecraft server with MCP protocol support

## Installation

1. Clone the repository
2. Install dependencies:

```bash
cd slack-mcp
poetry install
```

3. Configure environment variables:

Create a `.env` file in the project root with the following variables:

```
# Slack API credentials
SLACK_BOT_TOKEN=your_slack_bot_token_here
SLACK_SIGNING_SECRET=your_slack_signing_secret_here
SLACK_CHANNEL=your_slack_channel_id_here

# Minecraft server configuration
MINECRAFT_SERVER_HOST=your_minecraft_server_host
MINECRAFT_SERVER_PORT=your_minecraft_server_port
```

## Usage

### Starting the server

```bash
poetry run fastapi dev app/main.py
```

The server will start on http://localhost:8000

### API Endpoints

- `GET /healthz` - Health check endpoint
- `GET /status` - Get connection status for Slack and Minecraft
- `POST /slack/events` - Webhook for Slack events
- `POST /minecraft/command` - Send a command to the Minecraft server
- `POST /minecraft/chat` - Send a chat message to the Minecraft server

### Slack Integration

1. Create a Slack app at https://api.slack.com/apps
2. Enable the Events API and subscribe to the `message.channels` event
3. Set the Request URL to your server's `/slack/events` endpoint
4. Install the app to your workspace and get the Bot Token
5. Update your `.env` file with the Bot Token and Signing Secret

### Minecraft Integration

This server expects a Minecraft server that supports the MCP protocol. The protocol uses a simple JSON-based format for communication.

## License

MIT
