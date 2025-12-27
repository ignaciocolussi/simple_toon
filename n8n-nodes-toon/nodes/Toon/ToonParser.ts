/**
 * TOON Parser - Convert TOON format to JSON
 * Ported from Python implementation
 */

export class ToonParseError extends Error {
	constructor(message: string) {
		super(message);
		this.name = 'ToonParseError';
	}
}

type ParsedValue = string | number | boolean | null | object | any[];

interface ParseResult {
	value: any;
	nextIndex: number;
}

/**
 * Parse TOON format string to JavaScript object (JSON-compatible).
 */
export function parse(toon: string): any {
	if (!toon || !toon.trim()) {
		return null;
	}

	const lines = toon.trim().split('\n');

	// Parse multiple arrays at root level
	const result: Record<string, any> = {};
	let idx = 0;

	while (idx < lines.length) {
		// Skip empty lines
		if (!lines[idx].trim()) {
			idx += 1;
			continue;
		}

		const parsed = parseLines(lines, idx, 0);

		if (parsed.value === null) {
			idx += 1;
			continue;
		}

		if (typeof parsed.value === 'object' && !Array.isArray(parsed.value)) {
			Object.assign(result, parsed.value);
		} else {
			// Single value at root - return as-is
			return parsed.value;
		}

		idx = parsed.nextIndex;
	}

	return Object.keys(result).length > 0 ? result : null;
}

/**
 * Parse lines starting from startIdx with expected indentation.
 */
function parseLines(lines: string[], startIdx: number, currentIndent: number): ParseResult {
	if (startIdx >= lines.length) {
		return { value: null, nextIndex: startIdx };
	}

	const line = lines[startIdx];
	const stripped = line.trimStart();
	const indent = line.length - stripped.length;

	// Check if this is an array header: arrayName[N]{field1,field2}:
	const arrayMatch = stripped.match(/^(\w+)\[(\d+)\]\{([^}]+)\}:\s*$/);

	// Check for malformed array header (missing count or brackets)
	if (/^(\w+)(\{[^}]+\}:|\[\d+\])/.test(stripped) && !arrayMatch) {
		throw new ToonParseError(
			`Malformed array header: '${stripped}'. Expected format: arrayName[N]{field1,field2}:`,
		);
	}

	if (arrayMatch) {
		const arrayName = arrayMatch[1];
		const count = parseInt(arrayMatch[2], 10);
		const fields = arrayMatch[3].split(',').map((f) => f.trim());

		// Parse data rows
		const rows: Array<Record<string, any>> = [];
		let idx = startIdx + 1;
		const expectedIndent = indent + 2; // TOON uses 2-space indentation

		while (idx < lines.length && rows.length < count) {
			const dataLine = lines[idx];
			const dataStripped = dataLine.trimStart();
			const dataIndent = dataLine.length - dataStripped.length;

			if (dataIndent < expectedIndent || !dataStripped) {
				break;
			}

			if (dataIndent === expectedIndent) {
				const values = parseRow(dataStripped, fields.length);
				if (values.length !== fields.length) {
					throw new ToonParseError(
						`Row has ${values.length} values but header defines ${fields.length} fields`,
					);
				}
				const rowObj: Record<string, any> = {};
				fields.forEach((field, i) => {
					rowObj[field] = values[i];
				});
				rows.push(rowObj);
				idx += 1;
			} else {
				break;
			}
		}

		if (rows.length !== count) {
			throw new ToonParseError(
				`Array '${arrayName}' declares ${count} items but found ${rows.length}`,
			);
		}

		// If we're at the root level, return as an object with array name as key
		if (currentIndent === 0) {
			return { value: { [arrayName]: rows }, nextIndex: idx };
		}

		return { value: rows, nextIndex: idx };
	}

	// Simple value or object
	return { value: parseValue(stripped), nextIndex: startIdx + 1 };
}

/**
 * Parse a comma-separated row of values, handling quoted strings.
 */
function parseRow(row: string, expectedFields: number): ParsedValue[] {
	const values: ParsedValue[] = [];
	let current = '';
	let inQuotes = false;
	let wasQuoted = false;
	let escapeNext = false;

	for (const char of row) {
		if (escapeNext) {
			current += char;
			escapeNext = false;
			continue;
		}

		if (char === '\\' && inQuotes) {
			escapeNext = true;
			continue;
		}

		if (char === '"') {
			inQuotes = !inQuotes;
			wasQuoted = true;
			continue;
		}

		if (char === ',' && !inQuotes) {
			// If value was quoted, keep it as string
			if (wasQuoted) {
				values.push(current);
			} else {
				values.push(parseValue(current.trim()));
			}
			current = '';
			wasQuoted = false;
			continue;
		}

		current += char;
	}

	// Add the last value
	if (wasQuoted) {
		values.push(current);
	} else if (current || values.length < expectedFields) {
		values.push(parseValue(current.trim()));
	}

	return values;
}

/**
 * Parse a single value, inferring type from string representation.
 */
function parseValue(value: string): ParsedValue {
	if (!value) {
		return '';
	}

	// Check for null
	if (value.toLowerCase() === 'null') {
		return null;
	}

	// Check for boolean
	if (value.toLowerCase() === 'true') {
		return true;
	}
	if (value.toLowerCase() === 'false') {
		return false;
	}

	// Try to parse as number
	if (value.includes('.')) {
		const parsed = parseFloat(value);
		if (!isNaN(parsed)) {
			return parsed;
		}
	} else {
		const parsed = parseInt(value, 10);
		if (!isNaN(parsed) && parsed.toString() === value) {
			return parsed;
		}
	}

	// Return as string
	return value;
}
