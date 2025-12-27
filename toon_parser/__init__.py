"""TOON Parser - A Python parser and serializer for Token-Oriented Object Notation."""

from .advanced import (
    ToonConfig,
    flatten_object,
    parse_advanced,
    stream_parse,
    stringify_advanced,
    unflatten_object,
)
from .io import (
    ToonFileError,
    batch_convert,
    convert_json_to_toon,
    convert_toon_to_json,
    get_file_stats,
    read_json,
    read_toon,
    write_json,
    write_toon,
)
from .oo_api import (
    ToonConverter,
    ToonDocument,
    ToonParser,
    ToonSerializer,
)
from .parser import parse
from .schema import (
    Field,
    FieldType,
    MultiSchema,
    Schema,
    ValidationError,
    infer_schema,
)
from .serializer import stringify
from .streaming import (
    StreamingSerializer,
    stream_from_database,
    streaming_serializer,
)

__version__ = "0.2.1"  # Updated repository URLs
__all__ = [
    # Basic parsing/serializing (functional API)
    "parse",
    "stringify",
    # Advanced features (functional API)
    "ToonConfig",
    "stringify_advanced",
    "parse_advanced",
    "stream_parse",
    "flatten_object",
    "unflatten_object",
    # Schema validation
    "Field",
    "FieldType",
    "Schema",
    "MultiSchema",
    "ValidationError",
    "infer_schema",
    # File I/O
    "ToonFileError",
    "read_toon",
    "write_toon",
    "read_json",
    "write_json",
    "convert_json_to_toon",
    "convert_toon_to_json",
    "batch_convert",
    "get_file_stats",
    # Streaming serializer
    "StreamingSerializer",
    "streaming_serializer",
    "stream_from_database",
    # Object-oriented API
    "ToonParser",
    "ToonSerializer",
    "ToonDocument",
    "ToonConverter",
]
