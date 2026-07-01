"""Settings storage and management."""
from pathlib import Path
import json
from loguru import logger
from typing import Dict, Any, Optional

from models import FilterConfigModel


class SettingsStorage:
    """Persistent settings storage."""

    def __init__(self, storage_path: str = "settings/config.json"):
        """Initialize settings storage.

        Args:
            storage_path: Path to settings file
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        """Load settings from file.

        Returns:
            Settings dictionary
        """
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")
        return {}

    def _save(self) -> None:
        """Save settings to file."""
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value.

        Args:
            key: Setting key
            default: Default value

        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        self._save()

    def get_all(self) -> Dict[str, Any]:
        """Get all settings.

        Returns:
            All settings
        """
        return self.settings.copy()
