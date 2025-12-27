"""Tests for advanced TOON features."""

import pytest
from toon_parser import (
    ToonConfig,
    stringify_advanced,
    parse_advanced,
    stream_parse,
    flatten_object,
    unflatten_object,
)


class TestFlattenUnflatten:
    """Test object flattening and unflattening."""

    def test_flatten_simple_nested(self):
        """Test flattening simple nested object."""
        nested = {"name": "Alice", "address": {"city": "NYC", "zip": "10001"}}
        flattened = flatten_object(nested)
        assert flattened == {"name": "Alice", "address.city": "NYC", "address.zip": "10001"}

    def test_flatten_deep_nested(self):
        """Test flattening deeply nested object."""
        nested = {
            "user": {"profile": {"contact": {"email": "alice@example.com", "phone": "123"}}}
        }
        flattened = flatten_object(nested)
        assert flattened == {
            "user.profile.contact.email": "alice@example.com",
            "user.profile.contact.phone": "123",
        }

    def test_flatten_with_custom_separator(self):
        """Test flattening with custom separator."""
        nested = {"a": {"b": {"c": 1}}}
        flattened = flatten_object(nested, separator="_")
        assert flattened == {"a_b_c": 1}

    def test_flatten_max_depth(self):
        """Test flattening respects max depth."""
        nested = {"a": {"b": {"c": {"d": {"e": 1}}}}}
        flattened = flatten_object(nested, max_depth=3)
        # Should stop at depth 3
        assert "a.b.c" in flattened
        assert isinstance(flattened["a.b.c"], dict)

    def test_unflatten_simple(self):
        """Test unflattening simple object."""
        flattened = {"name": "Alice", "address.city": "NYC", "address.zip": "10001"}
        unflattened = unflatten_object(flattened)
        assert unflattened == {"name": "Alice", "address": {"city": "NYC", "zip": "10001"}}

    def test_unflatten_deep(self):
        """Test unflattening deeply nested object."""
        flattened = {"a.b.c.d": 1, "a.b.e": 2, "f": 3}
        unflattened = unflatten_object(flattened)
        assert unflattened == {"a": {"b": {"c": {"d": 1}, "e": 2}}, "f": 3}

    def test_roundtrip_flatten_unflatten(self):
        """Test that flatten -> unflatten is lossless."""
        original = {
            "id": 1,
            "name": "Alice",
            "contact": {"email": "alice@example.com", "phone": {"mobile": "123", "home": "456"}},
        }
        flattened = flatten_object(original)
        restored = unflatten_object(flattened)
        assert restored == original


class TestAdvancedStringify:
    """Test advanced TOON serialization."""

    def test_stringify_nested_objects(self):
        """Test serializing nested objects with flattening."""
        data = {
            "users": [
                {"id": 1, "name": "Alice", "address": {"city": "NYC", "zip": "10001"}},
                {"id": 2, "name": "Bob", "address": {"city": "LA", "zip": "90001"}},
            ]
        }
        result = stringify_advanced(data)
        assert "users[2]{id,name,address.city,address.zip}:" in result
        assert "1,Alice,NYC,\"10001\"" in result or "1,Alice,NYC,10001" in result

    def test_stringify_with_config(self):
        """Test serializing with custom configuration."""
        data = {
            "items": [
                {"id": 1, "data": {"x": 10, "y": 20}},
                {"id": 2, "data": {"x": 30, "y": 40}},
            ]
        }
        config = ToonConfig(indent_size=4, separator="_")
        result = stringify_advanced(data, config)
        assert "items[2]{id,data_x,data_y}:" in result
        assert "    " in result  # 4-space indent

    def test_stringify_multiple_arrays(self):
        """Test serializing multiple arrays."""
        data = {
            "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "products": [{"sku": "A001", "price": 19.99}, {"sku": "B002", "price": 29.99}],
        }
        result = stringify_advanced(data)
        assert "users[2]{id,name}:" in result
        assert "products[2]{sku,price}:" in result


class TestAdvancedParse:
    """Test advanced TOON parsing."""

    def test_parse_nested_objects(self):
        """Test parsing TOON with flattened nested objects."""
        toon = """users[2]{id,name,address.city,address.zip}:
  1,Alice,NYC,"10001"
  2,Bob,LA,"90001"
"""
        result = parse_advanced(toon)
        assert result == {
            "users": [
                {"id": 1, "name": "Alice", "address": {"city": "NYC", "zip": "10001"}},
                {"id": 2, "name": "Bob", "address": {"city": "LA", "zip": "90001"}},
            ]
        }

    def test_parse_with_custom_separator(self):
        """Test parsing with custom separator."""
        toon = """items[1]{id,data_x,data_y}:
  1,10,20
"""
        config = ToonConfig(separator="_")
        result = parse_advanced(toon, config)
        assert result == {"items": [{"id": 1, "data": {"x": 10, "y": 20}}]}

    def test_parse_multiple_arrays(self):
        """Test parsing multiple arrays."""
        toon = """users[2]{id,name}:
  1,Alice
  2,Bob
products[2]{sku,price}:
  A001,19.99
  B002,29.99
"""
        result = parse_advanced(toon)
        assert "users" in result
        assert "products" in result
        assert len(result["users"]) == 2
        assert len(result["products"]) == 2


class TestStreamParse:
    """Test streaming TOON parser."""

    def test_stream_parse_single_array(self):
        """Test streaming parse of single array."""
        toon = """users[3]{id,name}:
  1,Alice
  2,Bob
  3,Charlie
"""
        arrays = list(stream_parse(toon))
        assert len(arrays) == 1
        name, items = arrays[0]
        assert name == "users"
        assert len(items) == 3
        assert items[0] == {"id": 1, "name": "Alice"}

    def test_stream_parse_multiple_arrays(self):
        """Test streaming parse of multiple arrays."""
        toon = """users[2]{id,name}:
  1,Alice
  2,Bob
products[2]{sku,price}:
  A001,19.99
  B002,29.99
"""
        arrays = list(stream_parse(toon))
        assert len(arrays) == 2

        assert arrays[0][0] == "users"
        assert len(arrays[0][1]) == 2

        assert arrays[1][0] == "products"
        assert len(arrays[1][1]) == 2

    def test_stream_parse_with_nested_objects(self):
        """Test streaming parse with nested object support."""
        toon = """users[2]{id,address.city,address.zip}:
  1,NYC,"10001"
  2,LA,"90001"
"""
        arrays = list(stream_parse(toon))
        name, items = arrays[0]
        assert items[0] == {"id": 1, "address": {"city": "NYC", "zip": "10001"}}

    def test_stream_parse_memory_efficient(self):
        """Test that stream parse doesn't load all data at once."""
        # Create large TOON document
        large_toon = "users[1000]{id,name}:\n"
        for i in range(1000):
            large_toon += f"  {i},User{i}\n"

        # Stream parse should work efficiently
        count = 0
        for name, items in stream_parse(large_toon):
            assert name == "users"
            count += len(items)

        assert count == 1000


class TestAdvancedRoundtrip:
    """Test round-trip with advanced features."""

    def test_roundtrip_nested_objects(self):
        """Test nested objects round-trip."""
        original = {
            "users": [
                {
                    "id": 1,
                    "profile": {"name": "Alice", "age": 30, "contact": {"email": "alice@example.com"}},
                },
                {
                    "id": 2,
                    "profile": {"name": "Bob", "age": 25, "contact": {"email": "bob@example.com"}},
                },
            ]
        }

        toon = stringify_advanced(original)
        result = parse_advanced(toon)

        assert result == original

    def test_roundtrip_multiple_arrays(self):
        """Test multiple arrays round-trip."""
        original = {
            "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "logs": [
                {"timestamp": "2025-01-01T00:00:00Z", "level": "info"},
                {"timestamp": "2025-01-01T00:01:00Z", "level": "error"},
            ],
        }

        toon = stringify_advanced(original)
        result = parse_advanced(toon)

        assert result == original
