"""Scanner state management."""
from typing import Dict, List, Any
from datetime import datetime
from enum import Enum
from loguru import logger


class ScannerState(str, Enum):
    """Scanner operational states."""

    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    SCANNING = "scanning"
    ERROR = "error"
    STOPPED = "stopped"


class ScannerStateManager:
    """Manages scanner state."""

    def __init__(self):
        """Initialize state manager."""
        self.state = ScannerState.IDLE
        self.error_message = None
        self.last_state_change = datetime.utcnow()
        self.stats = {
            "tokens_found": 0,
            "tokens_matched": 0,
            "tokens_notified": 0,
            "reconnect_count": 0,
            "start_time": None,
            "filters_applied": 0,
        }

    def set_state(self, new_state: ScannerState, error_message: str = None) -> None:
        """Change scanner state.

        Args:
            new_state: New state
            error_message: Error message if state is ERROR
        """
        if self.state != new_state:
            logger.info(f"Scanner state: {self.state.value} -> {new_state.value}")
            self.state = new_state
            self.last_state_change = datetime.utcnow()

            if new_state == ScannerState.ERROR:
                self.error_message = error_message
                logger.error(f"Scanner error: {error_message}")
            else:
                self.error_message = None

    def get_state(self) -> ScannerState:
        """Get current state.

        Returns:
            Current scanner state
        """
        return self.state

    def is_running(self) -> bool:
        """Check if scanner is running.

        Returns:
            True if running (connected or scanning)
        """
        return self.state in [ScannerState.CONNECTED, ScannerState.SCANNING]

    def increment_stat(self, stat_name: str, amount: int = 1) -> None:
        """Increment a statistic.

        Args:
            stat_name: Name of statistic
            amount: Amount to increment
        """
        if stat_name in self.stats:
            self.stats[stat_name] += amount

    def set_stat(self, stat_name: str, value: Any) -> None:
        """Set a statistic value.

        Args:
            stat_name: Name of statistic
            value: Value to set
        """
        self.stats[stat_name] = value

    def get_stats(self) -> Dict[str, Any]:
        """Get all statistics.

        Returns:
            Statistics dictionary
        """
        return self.stats.copy()

    def get_status(self) -> Dict[str, Any]:
        """Get complete status.

        Returns:
            Status dictionary
        """
        return {
            "state": self.state.value,
            "error": self.error_message,
            "last_change": self.last_state_change.isoformat(),
            "stats": self.get_stats(),
        }
