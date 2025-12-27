/**
 * TOON Serializer - Convert JSON to TOON format
 * Ported from Python implementation
 */

export class ToonSerializeError extends Error {
	constructor(message: string) {
		super(message);
		this.name = 'ToonSerializeError';
	}
}

/**
 * Serialize JavaScript object (JSON-compatible) to TOON format string.
 */
export function stringify(obj: any, indent: number = 0): string {
	if (obj === null || obj === undefined) {
		return 'null';
	}

	if (typeof obj === 'boolean') {
		return obj ? 'true' : 'false';
	}

	if (typeof obj === 'number') {
		return String(obj);
	}

	if (typeof obj === 'string') {
		return quoteIfNeeded(obj);
	}

	if (Array.isArray(obj)) {
		return stringifyList(obj, indent);
	}

	if (typeof obj === 'object') {
		return stringifyDict(obj, indent);
	}

	throw new ToonSerializeError(`Cannot serialize type ${typeof obj} to TOON`);
}

/**
 * Serialize an object to TOON format.
 * For objects containing uniform arrays, use tabular format.
 */
function stringifyDict(obj: Record<string, any>, indent: number): string {
	const lines: string[] = [];
	const indentStr = '  '.repeat(indent);

	for (const [key, value] of Object.entries(obj)) {
		if (Array.isArray(value) && value.length > 0 && isUniformArray(value)) {
			// Use tabular format for uniform arrays
			const fields = extractFields(value);
			const count = value.length;

			// Header line: arrayName[N]{field1,field2}:
			const header = `${indentStr}${key}[${count}]{${fields.join(',')}}:`;
			lines.push(header);

			// Data rows
			for (const item of value) {
				const rowValues = fields.map((field) => formatValue(item[field]));
				const row = `${indentStr}  ${rowValues.join(',')}`;
				lines.push(row);
			}
		} else if (Array.isArray(value)) {
			// Non-uniform list
			throw new ToonSerializeError(
				`Non-uniform arrays are not yet supported in TOON format (key: '${key}')`,
			);
		} else if (typeof value === 'object' && value !== null) {
			// Nested object
			const nested = stringifyDict(value, indent + 1);
			lines.push(`${indentStr}${key}:`);
			lines.push(nested);
		} else {
			// Simple key-value pair
			const formattedValue = formatValue(value);
			lines.push(`${indentStr}${key}: ${formattedValue}`);
		}
	}

	return lines.join('\n');
}

/**
 * Serialize a list to TOON format.
 * Note: Top-level lists are not well-defined in TOON spec.
 */
function stringifyList(obj: any[], indent: number): string {
	if (isUniformArray(obj)) {
		throw new ToonSerializeError(
			'Top-level uniform arrays should be wrapped in an object with a key',
		);
	}

	// Handle as a simple list (non-standard TOON)
	const indentStr = '  '.repeat(indent);
	const lines: string[] = [];

	for (const item of obj) {
		if (typeof item === 'object' && item !== null) {
			const serialized = stringify(item, indent + 1);
			lines.push(`${indentStr}- ${serialized}`);
		} else {
			lines.push(`${indentStr}- ${formatValue(item)}`);
		}
	}

	return lines.join('\n');
}

/**
 * Check if an array is uniform (all items are objects with same keys).
 */
function isUniformArray(arr: any[]): boolean {
	if (!arr || arr.length === 0) {
		return false;
	}

	if (!arr.every((item) => typeof item === 'object' && item !== null && !Array.isArray(item))) {
		return false;
	}

	// Check if all objects have the same keys
	const firstKeys = new Set(Object.keys(arr[0]));
	return arr.every((item) => {
		const itemKeys = new Set(Object.keys(item));
		if (itemKeys.size !== firstKeys.size) {
			return false;
		}
		for (const key of firstKeys) {
			if (!itemKeys.has(key)) {
				return false;
			}
		}
		return true;
	});
}

/**
 * Extract field names from a uniform array (order preserved from first item).
 */
function extractFields(arr: Array<Record<string, any>>): string[] {
	if (!arr || arr.length === 0) {
		return [];
	}

	// Use the first item to determine field order
	return Object.keys(arr[0]);
}

/**
 * Format a single value for TOON output.
 * Quotes strings if they contain special characters.
 */
function formatValue(value: any): string {
	if (value === null || value === undefined) {
		return 'null';
	}

	if (typeof value === 'boolean') {
		return value ? 'true' : 'false';
	}

	if (typeof value === 'number') {
		return String(value);
	}

	if (typeof value === 'string') {
		return quoteIfNeeded(value);
	}

	throw new ToonSerializeError(`Cannot format value of type ${typeof value}`);
}

/**
 * Quote a string if it contains special characters.
 * Strings with commas, quotes, colons, or leading/trailing whitespace must be quoted.
 */
function quoteIfNeeded(s: string): string {
	if (!s) {
		return '""';
	}

	// Check if quoting is needed
	const needsQuotes =
		s.includes(',') ||
		s.includes('"') ||
		s.includes(':') ||
		s.includes(' ') ||
		s !== s.trim() ||
		['true', 'false', 'null'].includes(s.toLowerCase()) ||
		isNumeric(s);

	if (needsQuotes) {
		// Escape internal quotes and backslashes
		const escaped = s.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
		return `"${escaped}"`;
	}

	return s;
}

/**
 * Check if string looks like a number.
 */
function isNumeric(s: string): boolean {
	const num = parseFloat(s);
	return !isNaN(num) && isFinite(num) && num.toString() === s;
}
