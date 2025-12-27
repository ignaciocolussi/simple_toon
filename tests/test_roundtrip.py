"""Round-trip tests for TOON parser and serializer."""

import json
from pathlib import Path

from toon_parser import parse, stringify

# Load shared test cases
test_cases_path = Path(__file__).parent.parent.parent / "shared" / "test_cases.json"
with open(test_cases_path) as f:
    TEST_CASES = json.load(f)


class TestRoundTrip:
    """Test that JSON → TOON → JSON produces identical results."""

    def test_simple_array_roundtrip(self):
        """Test round-trip conversion for simple array."""
        original = TEST_CASES["simple_array"]["json"]
        toon = stringify(original)
        result = parse(toon)
        assert result == original

    def test_with_strings_roundtrip(self):
        """Test round-trip conversion with strings."""
        original = TEST_CASES["with_strings"]["json"]
        toon = stringify(original)
        result = parse(toon)
        assert result == original

    def test_with_nulls_roundtrip(self):
        """Test round-trip conversion with nulls."""
        original = TEST_CASES["with_nulls"]["json"]
        toon = stringify(original)
        result = parse(toon)
        assert result == original

    def test_mixed_types_roundtrip(self):
        """Test round-trip conversion with mixed types."""
        original = TEST_CASES["mixed_types"]["json"]
        toon = stringify(original)
        result = parse(toon)
        assert result == original

    def test_special_chars_roundtrip(self):
        """Test round-trip conversion with special characters."""
        original = TEST_CASES["special_chars"]["json"]
        toon = stringify(original)
        result = parse(toon)
        assert result == original

    def test_toon_to_json_to_toon(self):
        """Test TOON → JSON → TOON produces equivalent results."""
        original_toon = TEST_CASES["simple_array"]["toon"]
        json_obj = parse(original_toon)
        result_toon = stringify(json_obj)
        # Parse both to compare structure (formatting might differ)
        assert parse(result_toon) == parse(original_toon)

    def test_large_dataset_roundtrip(self):
        """Test round-trip with larger dataset."""
        large_data = {
            "transactions": [
                {
                    "id": i,
                    "amount": round(100.50 + i * 0.33, 2),
                    "status": "completed" if i % 2 == 0 else "pending",
                    "verified": i % 3 == 0,
                }
                for i in range(100)
            ]
        }
        toon = stringify(large_data)
        result = parse(toon)
        assert result == large_data
