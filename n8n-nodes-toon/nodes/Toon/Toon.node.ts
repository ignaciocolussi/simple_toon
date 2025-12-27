import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeOperationError,
} from 'n8n-workflow';

import { ToonParseError } from './ToonParser';
import { ToonSerializeError } from './ToonSerializer';
import {
	autoConvert,
	detectFormat,
	parseToon,
	stringifyToToon,
	validate,
} from './ToonUtils';

export class Toon implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Simple TOON',
		name: 'toon',
		icon: 'file:toon.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"]}}',
		description: 'Parse and serialize TOON (Token-Oriented Object Notation) format',
		defaults: {
			name: 'Simple TOON',
		},
		inputs: ['main'],
		outputs: ['main'],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Parse (TOON → JSON)',
						value: 'parse',
						description: 'Convert TOON format string to JSON object',
						action: 'Parse TOON to JSON',
					},
					{
						name: 'Stringify (JSON → TOON)',
						value: 'stringify',
						description: 'Convert JSON object to TOON format string',
						action: 'Stringify JSON to TOON',
					},
					{
						name: 'Validate',
						value: 'validate',
						description: 'Check if a string is valid TOON format',
						action: 'Validate TOON format',
					},
					{
						name: 'Auto-Detect and Convert',
						value: 'autoConvert',
						description: 'Automatically detect format and convert bidirectionally',
						action: 'Auto-detect and convert',
					},
				],
				default: 'parse',
			},
			// Parse operation fields
			{
				displayName: 'TOON Input',
				name: 'toonInput',
				type: 'string',
				typeOptions: {
					rows: 10,
				},
				displayOptions: {
					show: {
						operation: ['parse'],
					},
				},
				default: '',
				description: 'TOON format string to parse',
				placeholder: 'users[2]{id,name,active}:\n  1,Alice,true\n  2,Bob,false',
			},
			{
				displayName: 'Input Field',
				name: 'inputField',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['parse'],
					},
				},
				default: '',
				description: 'Field name containing TOON data (leave empty to use TOON Input)',
				placeholder: 'toonData',
			},
			// Stringify operation fields
			{
				displayName: 'JSON Input',
				name: 'jsonInput',
				type: 'json',
				displayOptions: {
					show: {
						operation: ['stringify'],
					},
				},
				default: '{\n  "users": [\n    {"id": 1, "name": "Alice", "active": true}\n  ]\n}',
				description: 'JSON object to convert to TOON format',
			},
			{
				displayName: 'Use Input Data',
				name: 'useInputData',
				type: 'boolean',
				displayOptions: {
					show: {
						operation: ['stringify'],
					},
				},
				default: false,
				description: 'Whether to use the input item data instead of JSON Input field',
			},
			// Validate operation fields
			{
				displayName: 'Input to Validate',
				name: 'validateInput',
				type: 'string',
				typeOptions: {
					rows: 10,
				},
				displayOptions: {
					show: {
						operation: ['validate'],
					},
				},
				default: '',
				description: 'String to validate as TOON format',
				placeholder: 'users[1]{id,name}:\n  1,Alice',
			},
			{
				displayName: 'Input Field',
				name: 'validateInputField',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['validate'],
					},
				},
				default: '',
				description: 'Field name containing data to validate (leave empty to use Input to Validate)',
				placeholder: 'dataToValidate',
			},
			// Auto-convert operation fields
			{
				displayName: 'Input Data',
				name: 'autoConvertInput',
				type: 'string',
				typeOptions: {
					rows: 10,
				},
				displayOptions: {
					show: {
						operation: ['autoConvert'],
					},
				},
				default: '',
				description: 'TOON or JSON string to auto-detect and convert',
				placeholder: 'Enter TOON or JSON data',
			},
			{
				displayName: 'Input Field',
				name: 'autoConvertInputField',
				type: 'string',
				displayOptions: {
					show: {
						operation: ['autoConvert'],
					},
				},
				default: '',
				description: 'Field name containing data to convert (leave empty to use Input Data)',
				placeholder: 'dataToConvert',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		const operation = this.getNodeParameter('operation', 0) as string;

		for (let i = 0; i < items.length; i++) {
			try {
				let outputJson: any = {};

				if (operation === 'parse') {
					// Parse TOON to JSON
					const inputField = this.getNodeParameter('inputField', i, '') as string;
					let toonInput: string;

					if (inputField) {
						// Get from input data field
						toonInput = items[i].json[inputField] as string;
						if (typeof toonInput !== 'string') {
							throw new NodeOperationError(
								this.getNode(),
								`Field '${inputField}' must contain a string`,
								{ itemIndex: i },
							);
						}
					} else {
						// Get from parameter
						toonInput = this.getNodeParameter('toonInput', i) as string;
					}

					const parsed = parseToon(toonInput);
					outputJson = { json: parsed, toon: toonInput };
				} else if (operation === 'stringify') {
					// Stringify JSON to TOON
					const useInputData = this.getNodeParameter('useInputData', i) as boolean;
					let jsonData: any;

					if (useInputData) {
						// Use the entire input item JSON
						jsonData = items[i].json;
					} else {
						// Use the jsonInput parameter
						const jsonInput = this.getNodeParameter('jsonInput', i) as string;
						jsonData = typeof jsonInput === 'string' ? JSON.parse(jsonInput) : jsonInput;
					}

					const toonOutput = stringifyToToon(jsonData);
					outputJson = { toon: toonOutput, json: jsonData };
				} else if (operation === 'validate') {
					// Validate TOON format
					const inputField = this.getNodeParameter('validateInputField', i, '') as string;
					let validateInput: string;

					if (inputField) {
						// Get from input data field
						validateInput = items[i].json[inputField] as string;
						if (typeof validateInput !== 'string') {
							throw new NodeOperationError(
								this.getNode(),
								`Field '${inputField}' must contain a string`,
								{ itemIndex: i },
							);
						}
					} else {
						// Get from parameter
						validateInput = this.getNodeParameter('validateInput', i) as string;
					}

					const validationResult = validate(validateInput);
					outputJson = {
						valid: validationResult.valid,
						format: validationResult.format || null,
						error: validationResult.error || null,
						input: validateInput,
					};
				} else if (operation === 'autoConvert') {
					// Auto-detect and convert
					const inputField = this.getNodeParameter('autoConvertInputField', i, '') as string;
					let autoConvertInput: string;

					if (inputField) {
						// Get from input data field
						autoConvertInput = items[i].json[inputField] as string;
						if (typeof autoConvertInput !== 'string') {
							throw new NodeOperationError(
								this.getNode(),
								`Field '${inputField}' must contain a string`,
								{ itemIndex: i },
							);
						}
					} else {
						// Get from parameter
						autoConvertInput = this.getNodeParameter('autoConvertInput', i) as string;
					}

					const detectedFormat = detectFormat(autoConvertInput);
					const converted = autoConvert(autoConvertInput);
					outputJson = {
						output: converted.output,
						detectedFormat,
						convertedFrom: converted.convertedFrom,
						convertedTo: converted.convertedTo,
						input: autoConvertInput,
					};
				}

				returnData.push({ json: outputJson });
			} catch (error) {
				if (error instanceof ToonParseError || error instanceof ToonSerializeError) {
					throw new NodeOperationError(this.getNode(), error.message, { itemIndex: i });
				}
				if (this.continueOnFail()) {
					returnData.push({
						json: {
							error: error.message,
						},
						pairedItem: { item: i },
					});
					continue;
				}
				throw error;
			}
		}

		return [returnData];
	}
}
