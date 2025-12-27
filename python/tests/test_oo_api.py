"""Tests for object-oriented API."""

import tempfile
from pathlib import Path
import pytest

from toon_parser import (
    ToonParser,
    ToonSerializer,
    ToonDocument,
    ToonConverter,
    ToonConfig,
    Schema,
    Field,
    FieldType,
    ValidationError,
)


class TestToonParser:
    """Test OO parser."""

    def test_basic_parse(self):
        """Test basic parsing with OO API."""
        parser = ToonParser()

        toon = """users[2]{id,name}:
  1,Alice
  2,Bob"""

        data = parser.parse(toon)
        assert data == {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

    def test_advanced_parse(self):
        """Test advanced parsing."""
        parser = ToonParser(advanced=True)

        toon = """users[1]{id,address.city}:
  1,NYC"""

        data = parser.parse(toon)
        assert data == {"users": [{"id": 1, "address": {"city": "NYC"}}]}

    def test_parse_with_schema(self):
        """Test parsing with validation."""
        schema = Schema("users", [Field("id", FieldType.INTEGER), Field("name", FieldType.STRING)])

        parser = ToonParser(schema=schema)

        toon = """users[1]{id,name}:
  1,Alice"""

        data = parser.parse(toon)  # Should pass

        # Invalid data
        bad_toon = """users[1]{id,name}:
  invalid,Alice"""

        with pytest.raises(ValidationError):
            parser.parse(bad_toon)

    def test_parse_file(self, tmp_path):
        """Test parsing from file."""
        parser = ToonParser()

        toon_file = tmp_path / "test.toon"
        toon_file.write_text("users[1]{id}:\n  1")

        data = parser.parse_file(toon_file)
        assert data == {"users": [{"id": 1}]}

    def test_stream(self):
        """Test streaming parse."""
        parser = ToonParser(advanced=True)

        toon = """users[2]{id}:
  1
  2
products[1]{sku}:
  A001"""

        arrays = list(parser.stream(toon))
        assert len(arrays) == 2
        assert arrays[0][0] == "users"
        assert arrays[1][0] == "products"


class TestToonSerializer:
    """Test OO serializer."""

    def test_basic_stringify(self):
        """Test basic serialization."""
        serializer = ToonSerializer()

        data = {"users": [{"id": 1, "name": "Alice"}]}
        toon = serializer.stringify(data)

        assert "users[1]{id,name}:" in toon
        assert "1,Alice" in toon

    def test_advanced_stringify(self):
        """Test advanced serialization."""
        serializer = ToonSerializer(advanced=True)

        data = {"users": [{"id": 1, "address": {"city": "NYC"}}]}
        toon = serializer.stringify(data)

        assert "address.city" in toon

    def test_stringify_with_schema(self):
        """Test serialization with validation."""
        schema = Schema("users", [Field("id", FieldType.INTEGER)])
        serializer = ToonSerializer(schema=schema)

        # Valid data
        valid = {"users": [{"id": 1}]}
        toon = serializer.stringify(valid)  # Should pass

        # Invalid data
        invalid = {"users": [{"id": "not_int"}]}
        with pytest.raises(ValidationError):
            serializer.stringify(invalid)

    def test_stringify_to_file(self, tmp_path):
        """Test serializing to file."""
        serializer = ToonSerializer()

        data = {"users": [{"id": 1}]}
        output_file = tmp_path / "output.toon"

        serializer.stringify_to_file(data, output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert "users[1]{id}:" in content


class TestToonDocument:
    """Test OO document wrapper."""

    def test_from_string(self):
        """Test creating document from string."""
        toon = """users[1]{id,name}:
  1,Alice"""

        doc = ToonDocument.from_string(toon)
        assert doc.has_array("users")
        assert len(doc.get_array("users")) == 1

    def test_from_file(self, tmp_path):
        """Test creating document from file."""
        toon_file = tmp_path / "test.toon"
        toon_file.write_text("users[1]{id}:\n  1")

        doc = ToonDocument.from_file(toon_file)
        assert doc.count("users") == 1

    def test_get_array(self):
        """Test getting array data."""
        doc = ToonDocument({"users": [{"id": 1}]})

        users = doc.get_array("users")
        assert len(users) == 1

        with pytest.raises(KeyError):
            doc.get_array("nonexistent")

    def test_array_operations(self):
        """Test array manipulation."""
        doc = ToonDocument({})

        # Add array
        doc.add_array("users", [{"id": 1}])
        assert doc.has_array("users")

        # Add item
        doc.add_item("users", {"id": 2})
        assert doc.count("users") == 2

        # Get array names
        assert "users" in doc.get_array_names()

    def test_query(self):
        """Test querying data."""
        doc = ToonDocument(
            {"users": [{"id": 1, "active": True}, {"id": 2, "active": False}, {"id": 3, "active": True}]}
        )

        active_users = doc.query("users", lambda u: u["active"])
        assert len(active_users) == 2

    def test_total_items(self):
        """Test counting total items."""
        doc = ToonDocument({"users": [{"id": 1}, {"id": 2}], "products": [{"sku": "A001"}]})

        assert doc.total_items() == 3

    def test_schema_validation(self):
        """Test schema validation on document."""
        doc = ToonDocument({"users": [{"id": 1, "name": "Alice"}]})

        schema = Schema("users", [Field("id", FieldType.INTEGER), Field("name", FieldType.STRING)])

        doc.set_schema("users", schema)
        doc.validate()  # Should pass

    def test_to_string(self):
        """Test serializing document."""
        doc = ToonDocument({"users": [{"id": 1}]})

        toon = doc.to_string()
        assert "users[1]{id}:" in toon

    def test_save(self, tmp_path):
        """Test saving document to file."""
        doc = ToonDocument({"users": [{"id": 1}]})

        output_file = tmp_path / "output.toon"
        doc.save(output_file)

        assert output_file.exists()

    def test_repr(self):
        """Test string representation."""
        doc = ToonDocument({"users": [{"id": 1}, {"id": 2}]})

        repr_str = repr(doc)
        assert "ToonDocument" in repr_str
        assert "users(2)" in repr_str


class TestToonConverter:
    """Test OO converter."""

    def test_json_to_toon(self, tmp_path):
        """Test JSON to TOON conversion."""
        converter = ToonConverter()

        json_file = tmp_path / "input.json"
        toon_file = tmp_path / "output.toon"

        import json
        json_file.write_text(json.dumps({"users": [{"id": 1}]}))

        converter.json_to_toon(json_file, toon_file)
        assert toon_file.exists()

    def test_toon_to_json(self, tmp_path):
        """Test TOON to JSON conversion."""
        converter = ToonConverter()

        toon_file = tmp_path / "input.toon"
        json_file = tmp_path / "output.json"

        toon_file.write_text("users[1]{id}:\n  1")

        converter.toon_to_json(toon_file, json_file)
        assert json_file.exists()

    def test_get_savings(self, tmp_path):
        """Test calculating savings."""
        converter = ToonConverter()

        json_file = tmp_path / "input.json"
        toon_file = tmp_path / "output.toon"

        import json
        data = {"users": [{"id": i, "name": f"User{i}"} for i in range(100)]}
        json_file.write_text(json.dumps(data))

        converter.json_to_toon(json_file, toon_file)

        stats = converter.get_savings(json_file, toon_file)

        assert "json_size_bytes" in stats
        assert "toon_size_bytes" in stats
        assert "savings_percent" in stats
        assert stats["savings_percent"] > 0


class TestOOvsFunc:
    """Test that OO and functional APIs produce same results."""

    def test_parse_equivalence(self):
        """Test that OO parser matches functional parser."""
        from toon_parser import parse

        toon = """users[1]{id,name}:
  1,Alice"""

        parser = ToonParser()
        oo_result = parser.parse(toon)
        func_result = parse(toon)

        assert oo_result == func_result

    def test_stringify_equivalence(self):
        """Test that OO serializer matches functional serializer."""
        from toon_parser import stringify

        data = {"users": [{"id": 1, "name": "Alice"}]}

        serializer = ToonSerializer()
        oo_result = serializer.stringify(data)
        func_result = stringify(data)

        assert oo_result == func_result
