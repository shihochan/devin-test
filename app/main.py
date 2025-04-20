import os
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.minecraft_client import MinecraftClient
from app.slack_client import SlackClient

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Slack MCP Server", description="A server that implements MCP protocol for Slack integration with Minecraft")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

slack_client = SlackClient(token=os.getenv("SLACK_BOT_TOKEN", ""))
minecraft_client = MinecraftClient(
    host=os.getenv("MINECRAFT_SERVER_HOST", "localhost"),
    port=int(os.getenv("MINECRAFT_SERVER_PORT", "25565"))
)

async def relay_messages():
    """
    Background task to relay messages between Slack and Minecraft.
    """
    while True:
        try:
            if minecraft_client.connected:
                data = minecraft_client.receive_data()
                if data and data.get("type") == "chat":
                    username = data.get("payload", {}).get("username", "Unknown")
                    message = data.get("payload", {}).get("message", "")
                    if username and message:
                        slack_client.send_message(
                            channel=os.getenv("SLACK_CHANNEL", "general"),
                            text=f"[Minecraft] {username}: {message}"
                        )
            
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in message relay: {e}")
            await asyncio.sleep(5)  # Wait longer on error

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    """
    minecraft_client.connect()
    
    asyncio.create_task(relay_messages())

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    """
    minecraft_client.disconnect()

@app.get("/healthz")
async def healthz():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@app.get("/status")
async def status():
    """
    Get status of connections.
    """
    return {
        "slack_connected": slack_client.connected,
        "minecraft_connected": minecraft_client.connected
    }

@app.post("/slack/events")
async def slack_events(request: Request):
    """
    Handle Slack events.
    """
    data = await request.json()
    
    
    if data.get("type") == "url_verification":
        return {"challenge": data.get("challenge")}
    
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        
        if event.get("type") == "message" and not event.get("bot_id"):
            channel = event.get("channel")
            user = event.get("user")
            text = event.get("text", "")
            
            try:
                user_info = slack_client.client.users_info(user=user)
                username = user_info["user"]["name"]
            except Exception:
                username = "Unknown"
            
            if minecraft_client.connected:
                minecraft_client.send_chat_message(username=username, message=text)
    
    return {"status": "ok"}

@app.post("/minecraft/command")
async def minecraft_command(command: Dict[str, Any]):
    """
    Send a command to the Minecraft server.
    """
    if not minecraft_client.connected:
        raise HTTPException(status_code=503, detail="Not connected to Minecraft server")
    
    cmd = command.get("command")
    if not cmd:
        raise HTTPException(status_code=400, detail="Command is required")
    
    success = minecraft_client.send_command(cmd)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send command")
    
    return {"status": "ok", "message": f"Command sent: {cmd}"}

@app.post("/minecraft/chat")
async def minecraft_chat(message: Dict[str, Any]):
    """
    Send a chat message to the Minecraft server.
    """
    if not minecraft_client.connected:
        raise HTTPException(status_code=503, detail="Not connected to Minecraft server")
    
    username = message.get("username", "Slack")
    text = message.get("message")
    if not text:
        raise HTTPException(status_code=400, detail="Message is required")
    
    success = minecraft_client.send_chat_message(username=username, message=text)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send message")
    
    return {"status": "ok", "message": f"Message sent: {username}: {text}"}
