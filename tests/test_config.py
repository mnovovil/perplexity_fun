"""Tests for config module"""
import pytest
import os
from unittest.mock import patch
from src import config
from src.queries import AVAILABLE_PRESETS


class TestConfigValidation:
    """Tests for configuration validation"""

    def test_has_required_constants(self):
        """Test that required constants are defined"""
        assert hasattr(config, "DEFAULT_PRESET")
        assert hasattr(config, "DEFAULT_TIMEOUT")
        assert hasattr(config, "BASE_URL")
        assert hasattr(config, "LOG_LEVEL")

    def test_default_preset_value(self):
        """Test default preset is set correctly"""
        assert config.DEFAULT_PRESET in AVAILABLE_PRESETS

    def test_default_timeout_value(self):
        """Test default timeout is set correctly"""
        assert config.DEFAULT_TIMEOUT == 30

    def test_base_url_value(self):
        """Test base URL is set correctly"""
        assert config.BASE_URL == "https://api.perplexity.ai"

    def test_validate_config_function_exists(self):
        """Test that validate_config function exists"""
        assert callable(config.validate_config)

    @patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"})
    def test_log_level_from_env(self):
        """Test that LOG_LEVEL can be set from environment"""
        # Reload the module to pick up the new env var
        import importlib
        importlib.reload(config)
        assert config.LOG_LEVEL == "DEBUG"


class TestConfigAPIKey:
    """Tests for API key configuration"""

    def test_api_key_from_env(self):
        """Test that API key can be read from environment"""
        # This should handle cases where the key is not set
        assert isinstance(config.PERPLEXITY_API_KEY, str)


class TestPresets:
    """Tests for available presets"""

    def test_preset_in_available_presets(self):
        """Test that default preset is in available presets"""
        from src.queries import AVAILABLE_PRESETS
        assert config.DEFAULT_PRESET in AVAILABLE_PRESETS
