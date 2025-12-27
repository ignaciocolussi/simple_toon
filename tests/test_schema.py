"""Tests for schema validation."""

import pytest

from toon_parser import (
    Field,
    FieldType,
    MultiSchema,
    Schema,
    ValidationError,
    infer_schema,
)


class TestField:
    """Test field validation."""

    def test_string_field(self):
        """Test string field validation."""
        field = Field("name", FieldType.STRING)
        field.validate("Alice")  # Should pass

        with pytest.raises(ValidationError):
            field.validate(123)

    def test_integer_field(self):
        """Test integer field validation."""
        field = Field("id", FieldType.INTEGER)
        field.validate(42)  # Should pass

        with pytest.raises(ValidationError):
            field.validate(3.14)

        with pytest.raises(ValidationError):
            field.validate("42")

    def test_float_field(self):
        """Test float field validation."""
        field = Field("price", FieldType.FLOAT)
        field.validate(19.99)  # Should pass

        with pytest.raises(ValidationError):
            field.validate(19)

    def test_boolean_field(self):
        """Test boolean field validation."""
        field = Field("active", FieldType.BOOLEAN)
        field.validate(True)  # Should pass
        field.validate(False)  # Should pass

        with pytest.raises(ValidationError):
            field.validate(1)

    def test_number_field(self):
        """Test number field (int or float)."""
        field = Field("value", FieldType.NUMBER)
        field.validate(42)  # Should pass
        field.validate(3.14)  # Should pass

        with pytest.raises(ValidationError):
            field.validate("42")

    def test_nullable_field(self):
        """Test nullable field."""
        field = Field("optional", FieldType.STRING, nullable=True)
        field.validate(None)  # Should pass
        field.validate("value")  # Should pass

        field_required = Field("required", FieldType.STRING, nullable=False)
        with pytest.raises(ValidationError):
            field_required.validate(None)

    def test_min_max_value(self):
        """Test min/max value validation."""
        field = Field("score", FieldType.INTEGER, min_value=0, max_value=100)
        field.validate(50)  # Should pass
        field.validate(0)  # Should pass
        field.validate(100)  # Should pass

        with pytest.raises(ValidationError):
            field.validate(-1)

        with pytest.raises(ValidationError):
            field.validate(101)

    def test_pattern_validation(self):
        """Test regex pattern validation."""
        field = Field("email", FieldType.STRING, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
        field.validate("alice@example.com")  # Should pass

        with pytest.raises(ValidationError):
            field.validate("invalid-email")

    def test_enum_validation(self):
        """Test enum validation."""
        field = Field("status", FieldType.STRING, enum=["pending", "completed", "failed"])
        field.validate("pending")  # Should pass
        field.validate("completed")  # Should pass

        with pytest.raises(ValidationError):
            field.validate("unknown")

    def test_custom_validator(self):
        """Test custom validator function."""
        field = Field("username", FieldType.STRING, validator=lambda x: len(x) >= 3)
        field.validate("alice")  # Should pass

        with pytest.raises(ValidationError):
            field.validate("ab")


class TestSchema:
    """Test schema validation."""

    def test_validate_item(self):
        """Test validating single item."""
        schema = Schema(
            "users",
            [
                Field("id", FieldType.INTEGER),
                Field("name", FieldType.STRING),
                Field("active", FieldType.BOOLEAN),
            ],
        )

        # Valid item
        schema.validate_item({"id": 1, "name": "Alice", "active": True})

        # Missing required field
        with pytest.raises(ValidationError):
            schema.validate_item({"id": 1, "name": "Alice"})

        # Wrong type
        with pytest.raises(ValidationError):
            schema.validate_item({"id": "1", "name": "Alice", "active": True})

    def test_validate_array(self):
        """Test validating entire array."""
        schema = Schema(
            "users",
            [Field("id", FieldType.INTEGER), Field("name", FieldType.STRING)],
        )

        # Valid array
        data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        schema.validate_array(data)

        # Invalid item in array
        with pytest.raises(ValidationError):
            schema.validate_array([{"id": 1, "name": "Alice"}, {"id": "2", "name": "Bob"}])

    def test_strict_mode(self):
        """Test strict mode (reject extra fields)."""
        schema = Schema("users", [Field("id", FieldType.INTEGER)], strict=True)

        # Extra field in strict mode
        with pytest.raises(ValidationError):
            schema.validate_item({"id": 1, "extra": "field"})

        # Non-strict allows extra fields
        schema_lenient = Schema("users", [Field("id", FieldType.INTEGER)], strict=False)
        schema_lenient.validate_item({"id": 1, "extra": "field"})  # Should pass

    def test_optional_fields(self):
        """Test optional (non-required) fields."""
        schema = Schema(
            "users",
            [Field("id", FieldType.INTEGER), Field("nickname", FieldType.STRING, required=False)],
        )

        # Without optional field
        schema.validate_item({"id": 1})

        # With optional field
        schema.validate_item({"id": 1, "nickname": "Al"})

    def test_validate_full_data(self):
        """Test validating data with array."""
        schema = Schema("users", [Field("id", FieldType.INTEGER)])

        data = {"users": [{"id": 1}, {"id": 2}]}
        schema.validate(data)  # Should pass

        # Missing array
        with pytest.raises(ValidationError):
            schema.validate({"products": []})


class TestMultiSchema:
    """Test multi-array schema validation."""

    def test_validate_multiple_arrays(self):
        """Test validating multiple arrays."""
        schemas = MultiSchema(
            [
                Schema("users", [Field("id", FieldType.INTEGER)]),
                Schema("products", [Field("sku", FieldType.STRING)]),
            ]
        )

        data = {"users": [{"id": 1}], "products": [{"sku": "A001"}]}
        schemas.validate(data)  # Should pass

    def test_reject_extra_arrays(self):
        """Test rejecting extra arrays."""
        schemas = MultiSchema(
            [Schema("users", [Field("id", FieldType.INTEGER)])], allow_extra_arrays=False
        )

        with pytest.raises(ValidationError):
            schemas.validate({"users": [{"id": 1}], "extra": [{"data": "value"}]})

    def test_allow_extra_arrays(self):
        """Test allowing extra arrays."""
        schemas = MultiSchema(
            [Schema("users", [Field("id", FieldType.INTEGER)])], allow_extra_arrays=True
        )

        # Should pass with extra array
        schemas.validate({"users": [{"id": 1}], "extra": [{"data": "value"}]})


class TestInferSchema:
    """Test schema inference."""

    def test_infer_simple_schema(self):
        """Test inferring schema from simple data."""
        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

        schema = infer_schema(data, "users")

        assert len(schema.fields) == 2
        assert "id" in schema.fields
        assert "name" in schema.fields
        assert schema.fields["id"].field_type == FieldType.INTEGER
        assert schema.fields["name"].field_type == FieldType.STRING

    def test_infer_with_nullable(self):
        """Test inferring schema with nullable fields."""
        data = {"items": [{"id": 1, "value": None}, {"id": 2, "value": "test"}]}

        schema = infer_schema(data, "items")

        assert schema.fields["value"].nullable is True

    def test_infer_with_optional(self):
        """Test inferring schema with optional fields."""
        data = {"items": [{"id": 1}, {"id": 2, "extra": "field"}]}

        schema = infer_schema(data, "items")

        assert schema.fields["id"].required is True
        assert schema.fields["extra"].required is False

    def test_infer_number_type(self):
        """Test inferring NUMBER type for mixed int/float."""
        data = {"values": [{"val": 1}, {"val": 2.5}]}

        schema = infer_schema(data, "values")

        assert schema.fields["val"].field_type == FieldType.NUMBER

    def test_validate_with_inferred_schema(self):
        """Test that inferred schema can validate data."""
        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

        schema = infer_schema(data, "users")

        # Should validate original data
        schema.validate(data)

        # Should reject invalid data
        with pytest.raises(ValidationError):
            schema.validate({"users": [{"id": "invalid", "name": "Charlie"}]})
