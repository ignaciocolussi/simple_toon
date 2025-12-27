"""Tests for streaming serializer."""

import pytest

from toon_parser import StreamingSerializer, stream_from_database, streaming_serializer


class TestStreamingSerializer:
    """Test streaming TOON serializer."""

    def test_basic_streaming(self, tmp_path):
        """Test basic streaming write."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            writer.begin_array("users", ["id", "name", "active"])
            writer.write_row([1, "Alice", True])
            writer.write_row([2, "Bob", False])
            writer.end_array()

        # Read and verify
        content = output_file.read_text()
        assert "users[?]{id,name,active}:" in content
        assert "1,Alice,true" in content
        assert "2,Bob,false" in content

    def test_write_item(self, tmp_path):
        """Test writing dictionary items."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            writer.begin_array("products", ["sku", "name", "price"])
            writer.write_item({"sku": "A001", "name": "Widget", "price": 19.99})
            writer.write_item({"sku": "B002", "name": "Gadget", "price": 29.99})
            row_count = writer.end_array()

        assert row_count == 2

    def test_write_items_iterator(self, tmp_path):
        """Test writing from iterator."""
        output_file = tmp_path / "output.toon"

        def item_generator():
            for i in range(100):
                yield {"id": i, "value": f"item_{i}"}

        with StreamingSerializer(output_file) as writer:
            writer.begin_array("items", ["id", "value"])
            count = writer.write_items(item_generator())
            writer.end_array()

        assert count == 100

    def test_write_array_convenience(self, tmp_path):
        """Test write_array convenience method."""
        output_file = tmp_path / "output.toon"

        items = [{"id": i, "name": f"User{i}"} for i in range(50)]

        with StreamingSerializer(output_file) as writer:
            count = writer.write_array("users", iter(items))

        assert count == 50

        # Verify content
        content = output_file.read_text()
        assert "users[50]{id,name}:" in content

    def test_auto_close_array(self, tmp_path):
        """Test that arrays are auto-closed on context exit."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            writer.begin_array("test", ["id"])
            writer.write_row([1])
            # Don't call end_array - should auto-close

        content = output_file.read_text()
        assert "test[?]{id}:" in content
        assert "1" in content

    def test_error_on_mismatched_values(self, tmp_path):
        """Test error when value count doesn't match fields."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            writer.begin_array("test", ["id", "name"])

            with pytest.raises(ValueError, match="Expected .* values"):
                writer.write_row([1])  # Missing name

    def test_error_on_no_array_open(self, tmp_path):
        """Test error when writing without opening array."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            with pytest.raises(RuntimeError):
                writer.write_row([1, "test"])

    def test_error_on_nested_array(self, tmp_path):
        """Test error when trying to open nested array."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            writer.begin_array("first", ["id"])

            with pytest.raises(RuntimeError):
                writer.begin_array("second", ["id"])

    def test_streaming_context_manager(self, tmp_path):
        """Test streaming_serializer context manager."""
        output_file = tmp_path / "output.toon"

        with streaming_serializer(output_file) as writer:
            writer.begin_array("test", ["value"])
            for i in range(10):
                writer.write_row([i])
            writer.end_array()

        content = output_file.read_text()
        assert "test[?]{value}:" in content

    def test_stream_from_database(self, tmp_path):
        """Test streaming from database-like source."""
        output_file = tmp_path / "output.toon"

        def mock_query():
            """Simulate database query."""
            for i in range(100):
                yield {"user_id": i, "email": f"user{i}@example.com", "active": i % 2 == 0}

        count = stream_from_database(
            mock_query,
            "users",
            ["user_id", "email", "active"],
            output_file,
            batch_size=20,
        )

        assert count == 100

        content = output_file.read_text()
        assert "users[?]{user_id,email,active}:" in content

    def test_empty_array(self, tmp_path):
        """Test writing empty array."""
        output_file = tmp_path / "output.toon"

        with StreamingSerializer(output_file) as writer:
            count = writer.write_array("empty", iter([]))

        assert count == 0

        content = output_file.read_text()
        assert "empty[0]{}:" in content
