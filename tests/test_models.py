"""Tests for data models."""
import pytest
from datetime import datetime

from models import TokenModel, DeveloperModel, FilterConfigModel, EventModel, EventType


def test_token_model_creation():
    """Test token model creation."""
    token = TokenModel(
        mint_address="EPjFWaLb3odccccccccccccccccccccccccccccccckq5CLdjT",
        name="Test Token",
        symbol="TEST",
        creator_address="EPjFWaLb3odccccccccccccccccccccccccccccccckq5CLdjT",
        created_at=datetime.utcnow(),
        discovered_at=datetime.utcnow(),
    )
    
    assert token.name == "Test Token"
    assert token.symbol == "TEST"
    assert token.mint_address == "EPjFWaLb3odccccccccccccccccccccccccccccccckq5CLdjT"


def test_developer_model_creation():
    """Test developer model creation."""
    dev = DeveloperModel(
        address="EPjFWaLb3odccccccccccccccccccccccccccccccckq5CLdjT",
        total_tokens_created=5,
        successful_launches=3,
        success_rate_percent=60.0,
    )
    
    assert dev.total_tokens_created == 5
    assert dev.success_rate_percent == 60.0


def test_filter_config_model():
    """Test filter configuration model."""
    filter_config = FilterConfigModel(
        name="Test Filter",
        min_liquidity_sol=5.0,
        max_dev_ownership_percent=25.0,
    )
    
    assert filter_config.name == "Test Filter"
    assert filter_config.min_liquidity_sol == 5.0
    assert filter_config.max_dev_ownership_percent == 25.0


def test_event_model_creation():
    """Test event model creation."""
    event = EventModel(
        type=EventType.TOKEN_FOUND,
        timestamp=datetime.utcnow(),
        token_mint="EPjFWaLb3odccccccccccccccccccccccccccccccckq5CLdjT",
        message="Test token found",
    )
    
    assert event.type == EventType.TOKEN_FOUND
    assert event.token_mint == "EPjFWaLb3odccccccccccccccccccccccccccccccckq5CLdjT"
