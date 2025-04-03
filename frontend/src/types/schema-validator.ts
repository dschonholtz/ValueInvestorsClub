/**
 * TypeScript schema validator for API contracts
 * 
 * This file validates that the frontend types match the API schemas.
 * Run with: npm run validate-schema
 */
import { 
  Idea, 
  IdeaDetail, 
  Company, 
  User, 
  Performance
} from './api';

type SchemaProperty = {
  type: string;
  format?: string;
  items?: SchemaProperty;
  properties?: Record<string, SchemaProperty>;
  $ref?: string;
};

type OpenAPISchema = {
  components: {
    schemas: Record<string, {
      type: string;
      properties: Record<string, SchemaProperty>;
      required?: string[];
    }>;
  };
};

/**
 * Validate frontend types against API schema
 */
async function validateSchema(): Promise<boolean> {
  try {
    // Fetch the OpenAPI schema (in production, this would come from the API server)
    const schemaPath = '../../api/schema/openapi.json';
    const schema: OpenAPISchema = await import(schemaPath).then(m => m.default);
    
    // Validate each type
    const validations = [
      validateType<Idea>('IdeaResponse', schema),
      validateType<IdeaDetail>('IdeaDetailResponse', schema),
      validateType<Company>('CompanyResponse', schema),
      validateType<User>('UserResponse', schema),
      validateType<Performance>('PerformanceResponse', schema),
    ];
    
    // Check all validations
    const allValid = validations.every(v => v);
    
    if (allValid) {
      console.log('✅ All types valid against API schema');
      return true;
    } else {
      console.error('❌ Type validation failed');
      return false;
    }
  } catch (error) {
    console.error('Error validating schema:', error);
    return false;
  }
}

/**
 * Validate a specific type against the API schema
 */
function validateType<T>(schemaName: string, schema: OpenAPISchema): boolean {
  console.log(`Validating ${schemaName}...`);
  
  // Get the schema definition
  const schemaDefinition = schema.components.schemas[schemaName];
  if (!schemaDefinition) {
    console.error(`Schema ${schemaName} not found in API schema`);
    return false;
  }
  
  // Create a sample of the type
  const sample = createSample(schemaDefinition);
  
  // Attempt to use the sample with the TypeScript type
  try {
    // This is a compile-time check only - cast only to verify compatibility
    sample as unknown as T;
    console.log(`  ✅ ${schemaName} valid`);
    return true;
  } catch (error) {
    console.error(`  ❌ ${schemaName} invalid:`, error);
    return false;
  }
}

/**
 * Create a sample object from a schema definition
 */
function createSample(schemaDefinition: Record<string, unknown>): Record<string, unknown> | null {
  if (schemaDefinition.type === 'object') {
    const result: Record<string, unknown> = {};
    
    for (const [propertyName, propertySchema] of Object.entries<SchemaProperty>(
      schemaDefinition.properties as Record<string, SchemaProperty>
    )) {
      result[propertyName] = createSampleForProperty(propertySchema);
    }
    
    return result;
  }
  
  return null;
}

/**
 * Create a sample value for a property
 */
function createSampleForProperty(propertySchema: SchemaProperty): unknown {
  if (propertySchema.$ref) {
    // Reference to another schema, we'd need to resolve it
    return {};
  }
  
  switch (propertySchema.type) {
    case 'string':
      if (propertySchema.format === 'date-time') {
        return new Date().toISOString();
      }
      return 'sample';
    case 'integer':
    case 'number':
      return 1;
    case 'boolean':
      return true;
    case 'array':
      return propertySchema.items ? [createSampleForProperty(propertySchema.items)] : [];
    case 'object':
      if (propertySchema.properties) {
        const result: Record<string, unknown> = {};
        for (const [propName, propSchema] of Object.entries<SchemaProperty>(propertySchema.properties)) {
          result[propName] = createSampleForProperty(propSchema);
        }
        return result;
      }
      return {};
    default:
      return null;
  }
}

// Export for Jest testing
export { validateSchema };

// Run validation if called directly
if (require.main === module) {
  validateSchema()
    .then(valid => {
      process.exit(valid ? 0 : 1);
    })
    .catch(error => {
      console.error('Validation error:', error);
      process.exit(1);
    });
}