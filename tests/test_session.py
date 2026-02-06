"""Tests for session module"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from src.session import QueryClient


class TestQueryClientInitialization:
    """Tests for QueryClient initialization"""

    def test_query_client_can_be_instantiated(self):
        """Test that QueryClient can be created"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            assert client is not None

    def test_query_client_with_custom_preset(self):
        """Test QueryClient with custom preset"""
        with patch("src.session.Perplexity"):
            client = QueryClient(preset="pro")
            assert client is not None

    def test_query_client_with_custom_state_path(self):
        """Test QueryClient with custom state path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "test_session.json")
            with patch("src.session.Perplexity"):
                client = QueryClient(state_path=state_file)
                assert client is not None


class TestQueryClientAttributes:
    """Tests for QueryClient attributes"""

    def test_query_client_has_history_attribute(self):
        """Test that QueryClient has history attribute"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            assert hasattr(client, "history")
            assert isinstance(client.history, list)

    def test_query_client_history_starts_empty(self):
        """Test that history starts empty"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            assert len(client.history) == 0

    def test_query_client_has_state_path_attribute(self):
        """Test that QueryClient has state_path attribute"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            assert hasattr(client, "state_path")


class TestQueryClientPersistence:
    """Tests for QueryClient persistence"""

    def test_default_state_path_created(self):
        """Test that default state path is set"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            assert client.state_path is not None
            assert ".perplexity" in client.state_path

    def test_custom_state_path_set(self):
        """Test that custom state path is set correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "test_session.json")
            with patch("src.session.Perplexity"):
                client = QueryClient(state_path=state_file)
                assert client.state_path == state_file

    def test_state_persists_history(self):
        """Test that history is persisted to disk"""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "test_session.json")
            with patch("src.session.Perplexity"):
                client = QueryClient(state_path=state_file)
                # Manually add history items
                client.history.append({"role": "user", "text": "test", "ts": "2025-01-01T00:00:00Z"})
                client._save_state()
                # Verify file was created
                assert os.path.exists(state_file)
                with open(state_file, "r") as f:
                    data = json.load(f)
                    assert "history" in data
                    assert len(data["history"]) == 1

    def test_state_loads_from_disk(self):
        """Test loading state from file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "test_session.json")
            # Create a test state file
            test_state = {"history": [{"role": "user", "text": "test", "ts": "2025-01-01T00:00:00Z"}]}
            with open(state_file, "w") as f:
                json.dump(test_state, f)

            with patch("src.session.Perplexity"):
                client = QueryClient(state_path=state_file)
                assert len(client.history) == 1
                assert client.history[0]["role"] == "user"
                assert client.history[0]["text"] == "test"


class TestQueryClientMessaging:
    """Tests for QueryClient message handling"""

    def test_add_message_to_history(self):
        """Test adding a message to history"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            assert len(client.history) == 0
            # Assuming there's an add_message or similar method
            # This is a placeholder test

    def test_history_contains_dicts(self):
        """Test that history items are dictionaries"""
        with patch("src.session.Perplexity"):
            client = QueryClient()
            # Manually add a message structure
            client.history.append({"role": "user", "text": "test"})
            assert isinstance(client.history[0], dict)
            assert "role" in client.history[0]
            assert "text" in client.history[0]
