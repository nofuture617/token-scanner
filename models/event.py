"""Pydantic models for Event logging."""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Event types."""

    TOKEN_FOUND = "token_found"
    TOKEN_MATCHED = "token_matched"
    TOKEN_NOTIFIED = "token_notified"
    BROWSER_OPENED = "browser_opened"
    FILTER_APPLIED = "filter_applied"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    CONNECTION_ESTABLISHED = "connection_established"
    CONNECTION_LOST = "connection_lost"
    RECONNECTING = "reconnecting"


class EventModel(BaseModel):
    """Event log entry model."""

    type: EventType = Field(..., description="Event type")
    timestamp: datetime = Field(..., description="Event timestamp")
    token_mint: Optional[str] = Field(None, description="Token mint address")
    token_name: Optional[str] = Field(None, description="Token name")
    filter_name: Optional[str] = Field(None, description="Filter name if applicable")
    message: str = Field(..., description="Event message")
    severity: str = Field("info", description="Severity level (info, warning, error)")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data")

    class Config:
        arbitrary_types_allowed = True
