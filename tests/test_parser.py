"""Tests for TOON parser."""

import json
from pathlib import Path

import pytest

from toon_parser import parse
from toon_parser.parser import ToonParseError

# Load shared test cases
test_cases_path = Path(__file__).parent.parent.parent / "shared" / "test_cases.json"
with open(test_cases_path) as f:
    TEST_CASES = json.load(f)


class TestParser:
    """Test TOON to JSON parsing."""

    def test_simple_array(self):
        """Test parsing a simple uniform array."""
        toon = TEST_CASES["simple_array"]["toon"]
        expected = TEST_CASES["simple_array"]["json"]
        result = parse(toon)
        assert result == expected

    def test_with_strings(self):
        """Test parsing arrays with quoted strings."""
        toon = TEST_CASES["with_strings"]["toon"]
        expected = TEST_CASES["with_strings"]["json"]
        result = parse(toon)
        assert result == expected

    def test_with_nulls(self):
        """Test parsing arrays with null values."""
        toon = TEST_CASES["with_nulls"]["toon"]
        expected = TEST_CASES["with_nulls"]["json"]
        result = parse(toon)
        assert result == expected

    def test_mixed_types(self):
        """Test parsing arrays with mixed data types."""
        toon = TEST_CASES["mixed_types"]["toon"]
        expected = TEST_CASES["mixed_types"]["json"]
        result = parse(toon)
        assert result == expected

    def test_special_chars(self):
        """Test parsing strings with special characters."""
        toon = TEST_CASES["special_chars"]["toon"]
        expected = TEST_CASES["special_chars"]["json"]
        result = parse(toon)
        assert result == expected

    def test_empty_string(self):
        """Test parsing empty string."""
        result = parse("")
        assert result is None

    def test_whitespace_only(self):
        """Test parsing whitespace-only string."""
        result = parse("   \n\n  ")
        assert result is None

    def test_invalid_header_format(self):
        """Test that invalid header format raises error."""
        invalid_toon = "users{id,name}:\n  1,Alice"
        with pytest.raises(ToonParseError):
            parse(invalid_toon)

    def test_mismatched_field_count(self):
        """Test that mismatched field count raises error."""
        invalid_toon = "users[1]{id,name,active}:\n  1,Alice"
        with pytest.raises(ToonParseError):
            parse(invalid_toon)

    def test_mismatched_row_count(self):
        """Test that mismatched row count raises error."""
        invalid_toon = "users[2]{id,name}:\n  1,Alice"
        with pytest.raises(ToonParseError):
            parse(invalid_toon)

    def test_type_inference(self):
        """Test that types are correctly inferred."""
        toon = "data[1]{num,float,bool,null,str}:\n  42,3.14,true,null,hello"
        result = parse(toon)
        assert result == {
            "data": [{"num": 42, "float": 3.14, "bool": True, "null": None, "str": "hello"}]
        }

    def test_boolean_values(self):
        """Test parsing boolean values."""
        toon = "flags[3]{id,enabled}:\n  1,true\n  2,false\n  3,TRUE"
        result = parse(toon)
        assert result == {
            "flags": [
                {"id": 1, "enabled": True},
                {"id": 2, "enabled": False},
                {"id": 3, "enabled": True},
            ]
        }
