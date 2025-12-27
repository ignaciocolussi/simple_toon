"""Tests for TOON serializer."""

import json
from pathlib import Path

import pytest

from toon_parser import stringify
from toon_parser.serializer import ToonSerializeError

# Load shared test cases
test_cases_path = Path(__file__).parent.parent / "shared" / "test_cases.json"
with open(test_cases_path) as f:
    TEST_CASES = json.load(f)


class TestSerializer:
    """Test JSON to TOON serialization."""

    def test_simple_array(self):
        """Test serializing a simple uniform array."""
        json_obj = TEST_CASES["simple_array"]["json"]
        expected = TEST_CASES["simple_array"]["toon"]
        result = stringify(json_obj)
        assert result == expected

    def test_with_strings(self):
        """Test serializing arrays with quoted strings."""
        json_obj = TEST_CASES["with_strings"]["json"]
        expected = TEST_CASES["with_strings"]["toon"]
        result = stringify(json_obj)
        assert result == expected

    def test_with_nulls(self):
        """Test serializing arrays with null values."""
        json_obj = TEST_CASES["with_nulls"]["json"]
        expected = TEST_CASES["with_nulls"]["toon"]
        result = stringify(json_obj)
        assert result == expected

    def test_mixed_types(self):
        """Test serializing arrays with mixed data types."""
        json_obj = TEST_CASES["mixed_types"]["json"]
        expected = TEST_CASES["mixed_types"]["toon"]
        result = stringify(json_obj)
        assert result == expected

    def test_special_chars(self):
        """Test serializing strings with special characters."""
        json_obj = TEST_CASES["special_chars"]["json"]
        expected = TEST_CASES["special_chars"]["toon"]
        result = stringify(json_obj)
        assert result == expected

    def test_primitive_values(self):
        """Test serializing primitive values."""
        assert stringify(42) == "42"
        assert stringify(3.14) == "3.14"
        assert stringify(True) == "true"
        assert stringify(False) == "false"
        assert stringify(None) == "null"
        assert stringify("hello") == "hello"

    def test_string_quoting(self):
        """Test that strings with special chars are quoted."""
        assert stringify("hello, world") == '"hello, world"'
        assert stringify("key: value") == '"key: value"'
        assert stringify("true") == '"true"'
        assert stringify("false") == '"false"'
        assert stringify("null") == '"null"'
        assert stringify("123") == '"123"'

    def test_uniform_array_detection(self):
        """Test that uniform arrays are detected correctly."""
        uniform = {"items": [{"a": 1, "b": 2}, {"a": 3, "b": 4}]}
        result = stringify(uniform)
        assert "items[2]{a,b}:" in result

    def test_non_uniform_array_error(self):
        """Test that non-uniform arrays raise error."""
        non_uniform = {"items": [{"a": 1}, {"b": 2}]}
        with pytest.raises(ToonSerializeError):
            stringify(non_uniform)

    def test_nested_objects_error(self):
        """Test that nested objects in arrays raise error for now."""
        _nested = {"items": [{"id": 1, "data": {"nested": "value"}}]}
        # This should work if we support nested structures
        # For now, it might fail depending on implementation
        # TODO: Implement actual test when nested object support is added

    def test_field_order_preservation(self):
        """Test that field order is preserved from first item."""
        obj = {"items": [{"z": 1, "a": 2, "m": 3}, {"z": 4, "a": 5, "m": 6}]}
        result = stringify(obj)
        # Should preserve order z,a,m from first item
        assert "items[2]{z,a,m}:" in result
