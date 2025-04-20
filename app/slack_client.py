"""
Slack client module for interacting with Slack API.
"""
import os
import logging
from typing import Dict, Any, List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackClient:
    """
    Client for interacting with Slack API.
    """
    def __init__(self, token: str):
        """
        Initialize the Slack client.
        
        Args:
            token: Slack API token
        """
        self.client = WebClient(token=token)
        self.connected = False
        self._test_connection()
    
    def _test_connection(self) -> None:
        """
        Test the connection to Slack API.
        """
        try:
            response = self.client.auth_test()
            self.bot_id = response["user_id"]
            self.team_id = response["team_id"]
            self.connected = True
            logger.info(f"Connected to Slack as {response['user']} in team {response['team']}")
        except SlackApiError as e:
            logger.error(f"Failed to connect to Slack: {e}")
            self.connected = False
    
    def send_message(self, channel: str, text: str, blocks: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Send a message to a Slack channel.
        
        Args:
            channel: Channel ID or name
            text: Message text
            blocks: Optional message blocks for rich formatting
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.connected:
            logger.error("Not connected to Slack")
            return False
        
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                blocks=blocks
            )
            logger.info(f"Sent message to Slack channel {channel}")
            return True
        except SlackApiError as e:
            logger.error(f"Failed to send message to Slack: {e}")
            return False
    
    def get_channels(self) -> List[Dict[str, Any]]:
        """
        Get list of channels in the workspace.
        
        Returns:
            List[Dict[str, Any]]: List of channel information
        """
        if not self.connected:
            logger.error("Not connected to Slack")
            return []
        
        try:
            response = self.client.conversations_list()
            channels = response["channels"]
            logger.info(f"Retrieved {len(channels)} channels from Slack")
            return channels
        except SlackApiError as e:
            logger.error(f"Failed to get channels from Slack: {e}")
            return []
    
    def get_channel_history(self, channel: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get message history from a channel.
        
        Args:
            channel: Channel ID
            limit: Maximum number of messages to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of messages
        """
        if not self.connected:
            logger.error("Not connected to Slack")
            return []
        
        try:
            response = self.client.conversations_history(channel=channel, limit=limit)
            messages = response["messages"]
            logger.info(f"Retrieved {len(messages)} messages from channel {channel}")
            return messages
        except SlackApiError as e:
            logger.error(f"Failed to get channel history from Slack: {e}")
            return []
