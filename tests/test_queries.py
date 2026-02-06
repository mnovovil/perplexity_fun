"""Tests for queries module"""
import pytest
from src.queries import (
    get_query,
    PREDEFINED_QUERIES,
    AVAILABLE_PRESETS,
)


class TestPredefinedQueries:
    """Tests for predefined queries"""

    def test_predefined_queries_dict_exists(self):
        """Test that PREDEFINED_QUERIES dictionary exists and is populated"""
        assert isinstance(PREDEFINED_QUERIES, dict)
        assert len(PREDEFINED_QUERIES) > 0

    def test_history_query_exists(self):
        """Test that History query is available"""
        assert "History" in PREDEFINED_QUERIES
        assert isinstance(PREDEFINED_QUERIES["History"], str)

    def test_get_query_returns_string(self):
        """Test that get_query returns a string"""
        result = get_query("History")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_query_valid_key(self):
        """Test get_query with valid key"""
        query = get_query("History")
        assert query == PREDEFINED_QUERIES["History"]

    def test_get_query_invalid_key_raises_error(self):
        """Test get_query with invalid key raises KeyError"""
        with pytest.raises(KeyError):
            get_query("NonExistentQuery")

    def test_all_predefined_queries_are_strings(self):
        """Test that all predefined queries are strings"""
        for key, query in PREDEFINED_QUERIES.items():
            assert isinstance(query, str)
            assert len(query) > 0


class TestPresets:
    """Tests for available presets"""

    def test_available_presets_exists(self):
        """Test that AVAILABLE_PRESETS list exists"""
        assert isinstance(AVAILABLE_PRESETS, list)
        assert len(AVAILABLE_PRESETS) > 0

    def test_available_presets_are_strings(self):
        """Test that all presets are strings"""
        for preset in AVAILABLE_PRESETS:
            assert isinstance(preset, str)
            assert len(preset) > 0

    def test_required_presets_exist(self):
        """Test that required presets are available"""
        required = ["pro-search", "pro", "fast"]
        for preset in required:
            assert preset in AVAILABLE_PRESETS

    def test_presets_not_empty(self):
        """Test that we have at least 3 presets"""
        assert len(AVAILABLE_PRESETS) >= 3
