/**
 * TOON Utilities - Validation and auto-detection
 */

import { parse, ToonParseError } from './ToonParser';
import { stringify, ToonSerializeError } from './ToonSerializer';

export interface ValidationResult {
	valid: boolean;
	error?: string;
	format?: 'toon' | 'json';
}

/**
 * Validate if a string is valid TOON format.
 */
export function validate(input: string): ValidationResult {
	if (!input || !input.trim()) {
		return {
			valid: false,
			error: 'Input is empty',
		};
	}

	try {
		parse(input);
		return {
			valid: true,
			format: 'toon',
		};
	} catch (error) {
		if (error instanceof ToonParseError) {
			return {
				valid: false,
				error: error.message,
			};
		}
		return {
			valid: false,
			error: 'Unknown validation error',
		};
	}
}

/**
 * Detect if input is TOON or JSON format.
 */
export function detectFormat(input: string): 'toon' | 'json' | 'unknown' {
	if (!input || !input.trim()) {
		return 'unknown';
	}

	const trimmed = input.trim();

	// Check for JSON format indicators
	if (
		(trimmed.startsWith('{') && trimmed.endsWith('}')) ||
		(trimmed.startsWith('[') && trimmed.endsWith(']'))
	) {
		try {
			JSON.parse(trimmed);
			return 'json';
		} catch {
			// Not valid JSON, might be TOON
		}
	}

	// Check for TOON format indicators
	// TOON typically has array headers like: arrayName[N]{field1,field2}:
	if (/\w+\[\d+\]\{[^}]+\}:/.test(trimmed)) {
		return 'toon';
	}

	// Try parsing as TOON
	try {
		parse(trimmed);
		return 'toon';
	} catch {
		// Not TOON
	}

	// Try parsing as JSON as last resort
	try {
		JSON.parse(trimmed);
		return 'json';
	} catch {
		// Neither format
	}

	return 'unknown';
}

/**
 * Auto-detect format and convert to the opposite format.
 */
export function autoConvert(input: string): { output: string; convertedFrom: string; convertedTo: string } {
	const format = detectFormat(input);

	if (format === 'toon') {
		// Convert TOON to JSON
		const parsed = parse(input);
		const output = JSON.stringify(parsed, null, 2);
		return {
			output,
			convertedFrom: 'toon',
			convertedTo: 'json',
		};
	} else if (format === 'json') {
		// Convert JSON to TOON
		const parsed = JSON.parse(input);
		const output = stringify(parsed);
		return {
			output,
			convertedFrom: 'json',
			convertedTo: 'toon',
		};
	} else {
		throw new Error('Unable to detect input format. Input must be valid TOON or JSON.');
	}
}

/**
 * Parse TOON and return as JSON object.
 */
export function parseToon(input: string): any {
	return parse(input);
}

/**
 * Stringify object to TOON format.
 */
export function stringifyToToon(obj: any): string {
	return stringify(obj);
}
