"""
Module containing predefined queries for Perplexity API
"""
from typing import List, Dict

# Dictionary of predefined queries
PREDEFINED_QUERIES = {
    "History": "Who created the broom and what is its historical significance?",
}

# Available presets
AVAILABLE_PRESETS = [
    "pro-search",
    "pro",
    "stable-diffusion",
    "fast",
]

def get_query(query_key: str) -> str:
    """
    Retrieve a predefined query by key.
    
    Args:
        query_key (str): The key of the predefined query
    
    Returns:
        str: The query text
        
    Raises:
        KeyError: If query_key is not found
    """
    if query_key not in PREDEFINED_QUERIES:
        raise KeyError(f"Query '{query_key}' not found. Available queries: {list(PREDEFINED_QUERIES.keys())}")
    
    return PREDEFINED_QUERIES[query_key]

def list_queries() -> List[str]:
    """List all available predefined queries."""
    return list(PREDEFINED_QUERIES.keys())

def list_presets() -> List[str]:
    """List all available presets."""
    return AVAILABLE_PRESETS
