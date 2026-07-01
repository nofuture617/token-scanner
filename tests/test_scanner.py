"""Tests for scanner."""
import pytest
from datetime import datetime

from scanner import ScannerState, ScannerStateManager


def test_scanner_state_management():
    """Test scanner state management."""
    state_mgr = ScannerStateManager()
    
    assert state_mgr.get_state() == ScannerState.IDLE
    
    state_mgr.set_state(ScannerState.CONNECTING)
    assert state_mgr.get_state() == ScannerState.CONNECTING
    
    state_mgr.set_state(ScannerState.CONNECTED)
    assert state_mgr.get_state() == ScannerState.CONNECTED
    assert state_mgr.is_running() is True


def test_scanner_statistics():
    """Test scanner statistics."""
    state_mgr = ScannerStateManager()
    
    assert state_mgr.get_stats()["tokens_found"] == 0
    
    state_mgr.increment_stat("tokens_found", 5)
    assert state_mgr.get_stats()["tokens_found"] == 5
    
    state_mgr.increment_stat("tokens_matched", 2)
    assert state_mgr.get_stats()["tokens_matched"] == 2
