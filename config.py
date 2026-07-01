"""Configuration management for Token Scanner application."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    app_name: str = "Token Scanner"
    app_version: str = "1.0.0"
    app_debug: bool = False
    app_log_level: str = "INFO"

    # Axiom Trade API
    axiom_access_token: str
    axiom_refresh_token: str
    api_timeout: int = 30
    api_max_retries: int = 3

    # WebSocket
    ws_reconnect_delay: int = 5
    ws_max_reconnects: int = 10

    # Database
    database_path: str = "data/scanner.db"
    database_backup_path: str = "data/backups"

    # Browser
    browser_auto_open: bool = True
    browser_new_tab: bool = True
    browser_headless: bool = True

    # Notifications
    notify_desktop: bool = True
    notify_sound: bool = True
    notify_sound_path: str = "assets/notification.wav"
    notify_popup: bool = True

    # Filters
    filter_min_successful_migrations: int = 1
    filter_max_created_tokens: int = 100
    filter_min_success_rate: float = 0.0
    filter_min_liquidity_sol: float = 2.0
    filter_min_market_cap_usd: float = 0
    filter_max_market_cap_usd: float = 10000000
    filter_min_holders: int = 10
    filter_max_dev_ownership: float = 50.0
    filter_migration_only: bool = False
    filter_no_mint_authority: bool = False
    filter_no_freeze_authority: bool = False

    # Whitelist/Blacklist
    whitelist_addresses: str = ""
    blacklist_addresses: str = ""

    # Logging
    log_retention_days: int = 30
    log_max_size_mb: int = 10
    log_backup_count: int = 5

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False

    @property
    def whitelist_set(self) -> set[str]:
        """Get whitelist as set of addresses."""
        return {addr.strip() for addr in self.whitelist_addresses.split(",") if addr.strip()}

    @property
    def blacklist_set(self) -> set[str]:
        """Get blacklist as set of addresses."""
        return {addr.strip() for addr in self.blacklist_addresses.split(",") if addr.strip()}

    def ensure_directories(self) -> None:
        """Create required directories."""
        db_dir = Path(self.database_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

        backup_dir = Path(self.database_backup_path)
        backup_dir.mkdir(parents=True, exist_ok=True)

        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        assets_dir = Path("assets")
        assets_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Load and return settings."""
    return Settings()
