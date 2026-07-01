"""Notification service for alerts."""
from typing import Optional, List
from loguru import logger
from plyer import notification
import asyncio
import sys


class NotificationService:
    """Service for sending notifications."""

    def __init__(
        self,
        desktop_notifications: bool = True,
        sound_notifications: bool = True,
        sound_path: str = "assets/notification.wav",
    ):
        """Initialize notification service.

        Args:
            desktop_notifications: Enable desktop notifications
            sound_notifications: Enable sound notifications
            sound_path: Path to sound file
        """
        self.desktop_notifications = desktop_notifications
        self.sound_notifications = sound_notifications
        self.sound_path = sound_path

    async def notify_token_match(self, token_name: str, token_symbol: str, filters: List[str]) -> None:
        """Send token match notification.

        Args:
            token_name: Token name
            token_symbol: Token symbol
            filters: List of matched filter names
        """
        try:
            title = f"🎉 Token Match: {token_symbol}"
            message = f"{token_name}\nMatched: {', '.join(filters)}"

            # Desktop notification
            if self.desktop_notifications:
                self._send_desktop_notification(title, message)

            # Sound notification
            if self.sound_notifications:
                await self._play_sound()

            logger.info(f"Sent notification for {token_symbol}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    def _send_desktop_notification(self, title: str, message: str) -> None:
        """Send desktop notification.

        Args:
            title: Notification title
            message: Notification message
        """
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Token Scanner",
                timeout=10,
            )
            logger.debug(f"Desktop notification sent: {title}")
        except Exception as e:
            logger.warning(f"Failed to send desktop notification: {e}")

    async def _play_sound(self) -> None:
        """Play notification sound."""
        try:
            if sys.platform == "win32":
                import winsound
                winsound.Beep(1000, 500)
            elif sys.platform == "darwin":
                import os
                os.system(f"afplay {self.sound_path} &")
            else:
                import os
                os.system(f"play {self.sound_path} &")
            logger.debug("Sound notification played")
        except Exception as e:
            logger.warning(f"Failed to play sound: {e}")

    async def notify_scanner_status(self, status: str, message: str) -> None:
        """Send scanner status notification.

        Args:
            status: Status type (connected, disconnected, error)
            message: Status message
        """
        try:
            title = f"Scanner {status.upper()}"
            if self.desktop_notifications:
                self._send_desktop_notification(title, message)
            logger.info(f"Status notification: {status} - {message}")
        except Exception as e:
            logger.error(f"Failed to send status notification: {e}")
