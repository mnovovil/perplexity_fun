"""
Configuration module for Perplexity API client
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Default settings
DEFAULT_PRESET = "pro-search"
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
