"""Tests for services."""
import pytest

from services import NotificationService


@pytest.mark.asyncio
async def test_notification_service_initialization():
    """Test notification service initialization."""
    service = NotificationService(
        desktop_notifications=True,
        sound_notifications=False,
    )
    
    assert service.desktop_notifications is True
    assert service.sound_notifications is False


@pytest.mark.asyncio
async def test_notification_without_sound():
    """Test notification without sound."""
    service = NotificationService(
        desktop_notifications=False,
        sound_notifications=False,
    )
    
    # Should not raise exception
    await service.notify_token_match(
        token_name="Test Token",
        token_symbol="TEST",
        filters=["Filter1", "Filter2"],
    )
