"""
Configuration module for Perplexity API client
"""
import os
from dotenv import load_dotenv
import getpass

# Try to import keyring; optional dependency
try:
    import keyring
except Exception:
    keyring = None

# Load environment variables
load_dotenv()

# API Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Default settings
DEFAULT_PRESET = "sonar"
DEFAULT_TIMEOUT = 30

# API Endpoints
BASE_URL = "https://api.perplexity.ai"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def validate_config():
    """
    Validate that all required configuration is set.
    
    Raises:
        ValueError: If required configuration is missing
    """
    if not PERPLEXITY_API_KEY:
        raise ValueError("PERPLEXITY_API_KEY environment variable is not set. Please add it to .env file or set it as an environment variable.")


def get_api_key(service_name: str = "perplexity_api_key") -> str:
    """Retrieve API key from environment variable or system keyring.

    Priority: environment variable -> keyring -> empty string
    """
    env_key = os.getenv("PERPLEXITY_API_KEY")
    if env_key:
        return env_key

    if keyring is not None:
        try:
            # Use current user as username for storing key
            username = getpass.getuser()
            secret = keyring.get_password(service_name, username)
            if secret:
                return secret
        except Exception:
            pass

    return ""


def save_api_key_to_keyring(api_key: str, service_name: str = "perplexity_api_key") -> bool:
    """Save API key into the OS keyring. Returns True on success, False otherwise."""
    if keyring is None:
        return False
    try:
        username = getpass.getuser()
        keyring.set_password(service_name, username, api_key)
        return True
    except Exception:
        return False
