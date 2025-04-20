"""
Minecraft client module for connecting to Minecraft servers using the MCP protocol.
"""
import socket
import json
import logging
from typing import Dict, Any, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MinecraftClient:
    """
    Client for connecting to Minecraft servers using the MCP protocol.
    """
    def __init__(self, host: str, port: int):
        """
        Initialize the Minecraft client.
        
        Args:
            host: Minecraft server hostname or IP
            port: Minecraft server port
        """
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Connect to the Minecraft server.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to Minecraft server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Minecraft server: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """
        Disconnect from the Minecraft server.
        """
        if self.socket:
            self.socket.close()
        self.connected = False
        logger.info("Disconnected from Minecraft server")
    
    def send_command(self, command: str) -> bool:
        """
        Send a command to the Minecraft server.
        
        Args:
            command: The command to send
            
        Returns:
            bool: True if command sent successfully, False otherwise
        """
        if not self.connected or self.socket is None:
            logger.error("Not connected to Minecraft server")
            return False
        
        try:
            packet = {
                "type": "command",
                "payload": command
            }
            self.socket.sendall(json.dumps(packet).encode('utf-8') + b'\n')
            logger.info(f"Sent command to Minecraft server: {command}")
            return True
        except Exception as e:
            logger.error(f"Failed to send command to Minecraft server: {e}")
            return False
    
    def send_chat_message(self, username: str, message: str) -> bool:
        """
        Send a chat message to the Minecraft server.
        
        Args:
            username: The username to display
            message: The message content
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.connected or self.socket is None:
            logger.error("Not connected to Minecraft server")
            return False
        
        try:
            packet = {
                "type": "chat",
                "payload": {
                    "username": username,
                    "message": message
                }
            }
            self.socket.sendall(json.dumps(packet).encode('utf-8') + b'\n')
            logger.info(f"Sent chat message to Minecraft server: {username}: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send chat message to Minecraft server: {e}")
            return False
    
    def receive_data(self) -> Optional[Dict[str, Any]]:
        """
        Receive data from the Minecraft server.
        
        Returns:
            Optional[Dict[str, Any]]: Received data as a dictionary, or None if error
        """
        if not self.connected or self.socket is None:
            logger.error("Not connected to Minecraft server")
            return None
        
        try:
            data = self.socket.recv(4096)
            if not data:
                logger.warning("No data received from Minecraft server")
                return None
            
            packet = json.loads(data.decode('utf-8'))
            logger.info(f"Received data from Minecraft server: {packet}")
            return packet
        except Exception as e:
            logger.error(f"Failed to receive data from Minecraft server: {e}")
            return None
