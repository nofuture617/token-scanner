"""Tests for filter engine."""
import pytest
from datetime import datetime

from models import TokenModel, FilterConfigModel
from filters import FilterEngine
from database import DatabaseConnection
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_filter_matching(temp_db: DatabaseConnection):
    """Test token filter matching."""
    session = temp_db.get_session()
    
    # Create filter engine
    engine = FilterEngine(session)
    
    # Create test token
    token = TokenModel(
        mint_address="11111111111111111111111111111111",
        name="Test Token",
        symbol="TEST",
        creator_address="22222222222222222222222222222222",
        market_cap_usd=100000,
        liquidity_sol=10.0,
        holders_count=100,
        created_at=datetime.utcnow(),
        discovered_at=datetime.utcnow(),
    )
    
    # Create filter
    filter_config = FilterConfigModel(
        name="Test Filter",
        min_liquidity_sol=5.0,
        min_market_cap_usd=50000,
        min_holders=50,
    )
    
    # Evaluate
    result = engine._check_token_criteria(token, filter_config)
    assert result is True


@pytest.mark.asyncio
async def test_filter_rejection(temp_db: DatabaseConnection):
    """Test filter rejection."""
    session = temp_db.get_session()
    engine = FilterEngine(session)
    
    # Create token with low liquidity
    token = TokenModel(
        mint_address="11111111111111111111111111111111",
        name="Test Token",
        symbol="TEST",
        creator_address="22222222222222222222222222222222",
        market_cap_usd=100000,
        liquidity_sol=1.0,  # Too low
        holders_count=100,
        created_at=datetime.utcnow(),
        discovered_at=datetime.utcnow(),
    )
    
    # Create strict filter
    filter_config = FilterConfigModel(
        name="Strict Filter",
        min_liquidity_sol=5.0,
    )
    
    result = engine._check_token_criteria(token, filter_config)
    assert result is False
