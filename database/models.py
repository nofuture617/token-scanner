"""SQLAlchemy database models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TokenORM(Base):
    """Token database model."""

    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    mint_address = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    symbol = Column(String(50), index=True, nullable=False)
    creator_address = Column(String(255), index=True, nullable=False)
    
    price_usd = Column(Float, nullable=True)
    market_cap_usd = Column(Float, nullable=True)
    fdv_usd = Column(Float, nullable=True)
    volume_usd = Column(Float, nullable=True)
    liquidity_sol = Column(Float, nullable=True)
    
    holders_count = Column(Integer, nullable=True)
    top_holders_percent = Column(Float, nullable=True)
    dev_ownership_percent = Column(Float, nullable=True)
    bundle_percent = Column(Float, nullable=True)
    
    is_migrated = Column(Boolean, default=False, index=True)
    has_mint_authority = Column(Boolean, default=True)
    has_freeze_authority = Column(Boolean, default=True)
    liquidity_locked = Column(Boolean, default=False)
    
    protocol = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False)
    discovered_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    axiom_url = Column(String(500), nullable=True)
    twitter_url = Column(String(500), nullable=True)
    telegram_url = Column(String(500), nullable=True)
    website_url = Column(String(500), nullable=True)
    
    matched_filters = Column(Text, nullable=True)  # JSON string
    notified = Column(Boolean, default=False)
    browser_opened = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    __table_args__ = (
        Index("idx_creator_discovered", "creator_address", "discovered_at"),
        Index("idx_market_cap", "market_cap_usd"),
        Index("idx_liquidity", "liquidity_sol"),
    )


class DeveloperORM(Base):
    """Developer database model."""

    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), unique=True, index=True, nullable=False)
    total_tokens_created = Column(Integer, default=0)
    successful_launches = Column(Integer, default=0)
    success_rate_percent = Column(Float, default=0.0)
    migrated_tokens = Column(Integer, default=0)
    last_token_created = Column(String(255), nullable=True)
    is_blacklisted = Column(Boolean, default=False, index=True)
    is_whitelisted = Column(Boolean, default=False, index=True)
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FilterConfigORM(Base):
    """Filter configuration database model."""

    __tablename__ = "filter_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    enabled = Column(Boolean, default=True, index=True)
    
    min_successful_migrations = Column(Integer, default=1)
    max_created_tokens = Column(Integer, default=100)
    min_success_rate = Column(Float, default=0.0)
    
    min_liquidity_sol = Column(Float, default=2.0)
    min_market_cap_usd = Column(Float, default=0)
    max_market_cap_usd = Column(Float, default=10_000_000)
    
    min_holders = Column(Integer, default=10)
    max_dev_ownership_percent = Column(Float, default=50.0)
    max_top_holders_percent = Column(Float, default=100.0)
    
    migration_only = Column(Boolean, default=False)
    no_mint_authority = Column(Boolean, default=False)
    no_freeze_authority = Column(Boolean, default=False)
    locked_liquidity_only = Column(Boolean, default=False)
    
    whitelist_addresses = Column(Text, nullable=True)  # JSON array
    blacklist_addresses = Column(Text, nullable=True)  # JSON array
    
    send_notification = Column(Boolean, default=True)
    auto_open_browser = Column(Boolean, default=True)
    
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EventORM(Base):
    """Event log database model."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    token_mint = Column(String(255), index=True, nullable=True)
    token_name = Column(String(255), nullable=True)
    filter_name = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="info", index=True)
    data = Column(Text, nullable=True)  # JSON string

    __table_args__ = (
        Index("idx_timestamp_type", "timestamp", "type"),
    )
