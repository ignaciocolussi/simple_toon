"""Tests for file I/O utilities."""

import pytest

from toon_parser import (
    Field,
    FieldType,
    Schema,
    ToonFileError,
    ValidationError,
    batch_convert,
    convert_json_to_toon,
    convert_toon_to_json,
    get_file_stats,
    read_json,
    read_toon,
    write_json,
    write_toon,
)


class TestBasicIO:
    """Test basic file I/O operations."""

    def test_write_and_read_toon(self, tmp_path):
        """Test writing and reading TOON files."""
        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

        toon_file = tmp_path / "users.toon"

        # Write
        write_toon(data, toon_file)
        assert toon_file.exists()

        # Read
        result = read_toon(toon_file)
        assert result == data

    def test_write_and_read_json(self, tmp_path):
        """Test writing and reading JSON files."""
        data = {"users": [{"id": 1, "name": "Alice"}]}

        json_file = tmp_path / "users.json"

        # Write
        write_json(data, json_file)
        assert json_file.exists()

        # Read
        result = read_json(json_file)
        assert result == data

    def test_overwrite_protection(self, tmp_path):
        """Test file overwrite protection."""
        data = {"test": [{"id": 1}]}
        file_path = tmp_path / "test.toon"

        # First write
        write_toon(data, file_path)

        # Second write without overwrite
        with pytest.raises(ToonFileError):
            write_toon(data, file_path, overwrite=False)

        # Second write with overwrite
        write_toon(data, file_path, overwrite=True)  # Should pass

    def test_create_parent_directories(self, tmp_path):
        """Test automatic parent directory creation."""
        data = {"test": [{"id": 1}]}
        file_path = tmp_path / "subdir" / "nested" / "test.toon"

        write_toon(data, file_path)
        assert file_path.exists()

    def test_read_nonexistent_file(self, tmp_path):
        """Test reading non-existent file."""
        with pytest.raises(ToonFileError):
            read_toon(tmp_path / "nonexistent.toon")


class TestAdvancedIO:
    """Test advanced I/O with nested objects."""

    def test_write_read_nested_objects(self, tmp_path):
        """Test writing/reading files with nested objects."""
        data = {
            "users": [
                {"id": 1, "profile": {"name": "Alice", "age": 30}},
                {"id": 2, "profile": {"name": "Bob", "age": 25}},
            ]
        }

        toon_file = tmp_path / "users_nested.toon"

        # Write with advanced=True
        write_toon(data, toon_file, advanced=True)

        # Read with advanced=True
        result = read_toon(toon_file, advanced=True)
        assert result == data

    def test_write_read_multiple_arrays(self, tmp_path):
        """Test writing/reading files with multiple arrays."""
        data = {"users": [{"id": 1}], "products": [{"sku": "A001"}]}

        toon_file = tmp_path / "multi.toon"

        write_toon(data, toon_file, advanced=True)
        result = read_toon(toon_file, advanced=True)

        assert "users" in result
        assert "products" in result


class TestSchemaValidation:
    """Test schema validation with I/O."""

    def test_validate_on_read(self, tmp_path):
        """Test schema validation when reading."""
        data = {"users": [{"id": 1, "name": "Alice"}]}
        toon_file = tmp_path / "users.toon"

        write_toon(data, toon_file)

        # Valid schema
        schema = Schema("users", [Field("id", FieldType.INTEGER), Field("name", FieldType.STRING)])

        result = read_toon(toon_file, schema=schema)
        assert result == data

        # Invalid schema
        bad_schema = Schema("users", [Field("id", FieldType.STRING)])

        with pytest.raises(ValidationError):
            read_toon(toon_file, schema=bad_schema)

    def test_validate_on_write(self, tmp_path):
        """Test schema validation when writing."""
        data = {"users": [{"id": 1, "name": "Alice"}]}
        toon_file = tmp_path / "users.toon"

        schema = Schema("users", [Field("id", FieldType.INTEGER), Field("name", FieldType.STRING)])

        # Valid data
        write_toon(data, toon_file, schema=schema)

        # Invalid data
        bad_data = {"users": [{"id": "invalid", "name": "Alice"}]}
        with pytest.raises(ValidationError):
            write_toon(bad_data, toon_file, schema=schema)


class TestConversion:
    """Test format conversion utilities."""

    def test_json_to_toon_conversion(self, tmp_path):
        """Test converting JSON to TOON."""
        data = {"users": [{"id": 1, "name": "Alice"}]}

        json_file = tmp_path / "input.json"
        toon_file = tmp_path / "output.toon"

        # Create JSON file
        write_json(data, json_file)

        # Convert
        convert_json_to_toon(json_file, toon_file)

        assert toon_file.exists()

        # Verify content
        result = read_toon(toon_file)
        assert result == data

    def test_toon_to_json_conversion(self, tmp_path):
        """Test converting TOON to JSON."""
        data = {"users": [{"id": 1, "name": "Alice"}]}

        toon_file = tmp_path / "input.toon"
        json_file = tmp_path / "output.json"

        # Create TOON file
        write_toon(data, toon_file)

        # Convert
        convert_toon_to_json(toon_file, json_file)

        assert json_file.exists()

        # Verify content
        result = read_json(json_file)
        assert result == data


class TestBatchConversion:
    """Test batch file conversion."""

    def test_batch_json_to_toon(self, tmp_path):
        """Test batch converting JSON files to TOON."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        # Create multiple JSON files
        for i in range(3):
            data = {"items": [{"id": i, "value": f"item{i}"}]}
            write_json(data, input_dir / f"file{i}.json")

        # Batch convert
        results = batch_convert(
            input_dir, output_dir, from_format="json", to_format="toon", pattern="*.json"
        )

        assert len(results) == 3
        assert (output_dir / "file0.toon").exists()
        assert (output_dir / "file1.toon").exists()
        assert (output_dir / "file2.toon").exists()

    def test_batch_toon_to_json(self, tmp_path):
        """Test batch converting TOON files to JSON."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        # Create multiple TOON files
        for i in range(2):
            data = {"items": [{"id": i}]}
            write_toon(data, input_dir / f"file{i}.toon")

        # Batch convert
        results = batch_convert(
            input_dir, output_dir, from_format="toon", to_format="json", pattern="*.toon"
        )

        assert len(results) == 2
        assert (output_dir / "file0.json").exists()
        assert (output_dir / "file1.json").exists()

    def test_batch_no_files(self, tmp_path):
        """Test batch convert with no matching files."""
        input_dir = tmp_path / "input"
        output_dir = tmp_path / "output"
        input_dir.mkdir()

        with pytest.raises(ToonFileError):
            batch_convert(input_dir, output_dir, from_format="json", to_format="toon")


class TestFileStats:
    """Test file statistics utility."""

    def test_toon_file_stats(self, tmp_path):
        """Test getting statistics for TOON file."""
        data = {
            "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "products": [{"sku": "A001", "price": 19.99}],
        }

        toon_file = tmp_path / "data.toon"
        write_toon(data, toon_file, advanced=True)

        stats = get_file_stats(toon_file)

        assert stats["format"] == "toon"
        assert stats["total_arrays"] == 2
        assert stats["total_items"] == 3
        assert stats["arrays"]["users"]["count"] == 2
        assert stats["arrays"]["products"]["count"] == 1

    def test_json_file_stats(self, tmp_path):
        """Test getting statistics for JSON file."""
        data = {"users": [{"id": 1, "name": "Alice"}]}

        json_file = tmp_path / "data.json"
        write_json(data, json_file)

        stats = get_file_stats(json_file)

        assert stats["format"] == "json"
        assert stats["total_arrays"] == 1
        assert stats["total_items"] == 1
