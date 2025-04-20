# Slack MCP Server

A Python server that implements the Message Control Protocol (MCP) for integrating Slack with Minecraft servers.

# Slack MCPサーバー

SlackとMinecraftサーバーを連携するためのメッセージコントロールプロトコル（MCP）を実装したPythonサーバーです。

## Overview | 概要

This server acts as a bridge between Slack and Minecraft, allowing:

このサーバーはSlackとMinecraftの間のブリッジとして機能し、以下のことが可能です：

- Sending messages from Slack to Minecraft | SlackからMinecraftへのメッセージ送信
- Receiving messages from Minecraft and forwarding them to Slack | MinecraftからSlackへのメッセージ転送
- Executing Minecraft commands from Slack | Slackからのコマンド実行

## Requirements | 必要条件

- Python 3.12+
- Poetry (for dependency management | 依存関係管理用)
- Slack Bot Token | Slack Botトークン
- Minecraft server with MCP protocol support | MCPプロトコルをサポートするMinecraftサーバー

## Installation | インストール方法

1. Clone the repository | リポジトリをクローン
2. Install dependencies | 依存関係をインストール:

```bash
cd slack-mcp
poetry install
```

3. Configure environment variables | 環境変数の設定:

Create a `.env` file in the project root with the following variables:

プロジェクトのルートディレクトリに以下の変数を含む`.env`ファイルを作成してください：

```
# Slack API credentials | Slack API認証情報
SLACK_BOT_TOKEN=your_slack_bot_token_here
SLACK_SIGNING_SECRET=your_slack_signing_secret_here
SLACK_CHANNEL=your_slack_channel_id_here

# Minecraft server configuration | Minecraftサーバー設定
MINECRAFT_SERVER_HOST=your_minecraft_server_host
MINECRAFT_SERVER_PORT=your_minecraft_server_port
```

## Usage | 使用方法

### Starting the server | サーバーの起動

```bash
poetry run fastapi dev app/main.py
```

The server will start on http://localhost:8000

サーバーは http://localhost:8000 で起動します

### API Endpoints | APIエンドポイント

- `GET /healthz` - Health check endpoint | ヘルスチェックエンドポイント
- `GET /status` - Get connection status for Slack and Minecraft | SlackとMinecraftの接続状態を取得
- `POST /slack/events` - Webhook for Slack events | Slackイベント用Webhook
- `POST /minecraft/command` - Send a command to the Minecraft server | Minecraftサーバーにコマンドを送信
- `POST /minecraft/chat` - Send a chat message to the Minecraft server | Minecraftサーバーにチャットメッセージを送信

### Slack Integration | Slack連携

1. Create a Slack app at https://api.slack.com/apps | https://api.slack.com/apps でSlackアプリを作成
2. Enable the Events API and subscribe to the `message.channels` event | Events APIを有効にし、`message.channels`イベントをサブスクライブ
3. Set the Request URL to your server's `/slack/events` endpoint | リクエストURLをサーバーの`/slack/events`エンドポイントに設定
4. Install the app to your workspace and get the Bot Token | アプリをワークスペースにインストールし、Botトークンを取得
5. Update your `.env` file with the Bot Token and Signing Secret | `.env`ファイルにBotトークンと署名シークレットを設定

### Minecraft Integration | Minecraft連携

This server expects a Minecraft server that supports the MCP protocol. The protocol uses a simple JSON-based format for communication.

このサーバーはMCPプロトコルをサポートするMinecraftサーバーを想定しています。プロトコルは通信にシンプルなJSON形式を使用します。

## License | ライセンス

MIT
