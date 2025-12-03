import yaml
import json
from collections import defaultdict

# Load both API specs
with open('TMF620_Product_Catalog_Management_API_v4.1.0_swagger.yaml', 'r', encoding='utf-8') as f:
    v4_spec = yaml.safe_load(f)

with open('TMF620-Product_Catalog_Management-v5.0.0.oas.yaml', 'r', encoding='utf-8') as f:
    v5_spec = yaml.safe_load(f)

# Extract schemas
v4_schemas = v4_spec.get('definitions', {})
v5_schemas = v5_spec.get('components', {}).get('schemas', {})

# Get base schema names (excluding _Create, _Update, _FVO, _MVO variants)
def get_base_name(schema_name):
    """Extract base entity name without suffixes"""
    for suffix in ['_Create', '_Update', '_FVO', '_MVO']:
        if schema_name.endswith(suffix):
            return schema_name[:-len(suffix)]
    return schema_name

def is_variant(schema_name):
    """Check if schema is a variant"""
    return any(schema_name.endswith(suffix) for suffix in ['_Create', '_Update', '_FVO', '_MVO'])

# Categorize v4 schemas
v4_base_schemas = {}
v4_variants = defaultdict(list)
for name in v4_schemas.keys():
    base_name = get_base_name(name)
    if is_variant(name):
        v4_variants[base_name].append(name)
    else:
        v4_base_schemas[name] = v4_schemas[name]

# Categorize v5 schemas
v5_base_schemas = {}
v5_variants = defaultdict(list)
for name in v5_schemas.keys():
    base_name = get_base_name(name)
    if is_variant(name):
        v5_variants[base_name].append(name)
    else:
        v5_base_schemas[name] = v5_schemas[name]

# Find schemas only in v4, only in v5, and in both
v4_only = set(v4_base_schemas.keys()) - set(v5_base_schemas.keys())
v5_only = set(v5_base_schemas.keys()) - set(v4_base_schemas.keys())
common = set(v4_base_schemas.keys()) & set(v5_base_schemas.keys())

print("=" * 100)
print("TMF620 Product Catalog Management API - Schema Comparison")
print("v4.1.0 (OAS 2.0) vs v5.0.0 (OAS 3.0)")
print("=" * 100)
print()

print(f"Summary:")
print(f"  v4.1.0 base schemas: {len(v4_base_schemas)}")
print(f"  v5.0.0 base schemas: {len(v5_base_schemas)}")
print(f"  Common schemas: {len(common)}")
print(f"  Only in v4.1.0: {len(v4_only)}")
print(f"  Only in v5.0.0: {len(v5_only)}")
print()

# Schemas only in v4.1.0
if v4_only:
    print("=" * 100)
    print("SCHEMAS ONLY IN v4.1.0")
    print("=" * 100)
    for schema in sorted(v4_only):
        print(f"\n• {schema}")
        if schema in v4_schemas:
            desc = v4_schemas[schema].get('description', 'No description')
            print(f"  Description: {desc[:120]}...")
    print()

# Schemas only in v5.0.0
if v5_only:
    print("=" * 100)
    print("SCHEMAS ONLY IN v5.0.0")
    print("=" * 100)
    for schema in sorted(v5_only):
        print(f"\n• {schema}")
        if schema in v5_schemas:
            # Handle allOf structures
            if 'allOf' in v5_schemas[schema]:
                for item in v5_schemas[schema]['allOf']:
                    if 'description' in item:
                        print(f"  Description: {item['description'][:120]}...")
                        break
            elif 'description' in v5_schemas[schema]:
                desc = v5_schemas[schema].get('description', 'No description')
                print(f"  Description: {desc[:120]}...")
    print()

# Detailed comparison for common schemas
print("=" * 100)
print("SIDE-BY-SIDE COMPARISON OF COMMON SCHEMAS")
print("=" * 100)

def extract_properties(schema):
    """Extract properties from a schema, handling allOf structures"""
    props = {}
    
    if 'properties' in schema:
        props.update(schema['properties'])
    
    if 'allOf' in schema:
        for item in schema['allOf']:
            if '$ref' not in item and 'properties' in item:
                props.update(item['properties'])
    
    return props

def get_property_type(prop):
    """Get a simple type representation of a property"""
    if '$ref' in prop:
        ref = prop['$ref'].split('/')[-1]
        return f"ref:{ref}"
    elif 'type' in prop:
        return prop['type']
    elif 'allOf' in prop:
        return 'allOf'
    elif 'oneOf' in prop:
        return 'oneOf'
    else:
        return 'complex'

# Sort common schemas and compare
for schema_name in sorted(common):
    v4_schema = v4_schemas[schema_name]
    v5_schema = v5_schemas[schema_name]
    
    v4_props = extract_properties(v4_schema)
    v5_props = extract_properties(v5_schema)
    
    v4_prop_names = set(v4_props.keys())
    v5_prop_names = set(v5_props.keys())
    
    all_props = sorted(v4_prop_names | v5_prop_names)
    
    # Skip if no meaningful properties
    if not all_props or all_props == ['@baseType', '@schemaLocation', '@type', '@referredType']:
        continue
    
    print(f"\n{'─' * 100}")
    print(f"Schema: {schema_name}")
    print(f"{'─' * 100}")
    
    # Description comparison
    v4_desc = v4_schema.get('description', 'N/A')
    v5_desc = ''
    if 'description' in v5_schema:
        v5_desc = v5_schema['description']
    elif 'allOf' in v5_schema:
        for item in v5_schema['allOf']:
            if 'description' in item:
                v5_desc = item['description']
                break
    
    if v4_desc != 'N/A' or v5_desc:
        print(f"\nDescription:")
        if v4_desc and len(v4_desc) > 80:
            print(f"  v4.1.0: {v4_desc[:80]}...")
        else:
            print(f"  v4.1.0: {v4_desc}")
        
        if v5_desc and len(v5_desc) > 80:
            print(f"  v5.0.0: {v5_desc[:80]}...")
        else:
            print(f"  v5.0.0: {v5_desc}")
    
    print(f"\nProperties Comparison:")
    print(f"  {'Property':<40} {'v4.1.0 Type':<25} {'v5.0.0 Type':<25}")
    print(f"  {'-'*40} {'-'*25} {'-'*25}")
    
    only_in_v4 = v4_prop_names - v5_prop_names
    only_in_v5 = v5_prop_names - v4_prop_names
    common_props = v4_prop_names & v5_prop_names
    
    # Show common properties first
    for prop in sorted(common_props):
        v4_type = get_property_type(v4_props[prop])
        v5_type = get_property_type(v5_props[prop])
        marker = "" if v4_type == v5_type else " ⚠️"
        print(f"  {prop:<40} {v4_type:<25} {v5_type:<25}{marker}")
    
    # Show properties only in v4
    for prop in sorted(only_in_v4):
        v4_type = get_property_type(v4_props[prop])
        print(f"  {prop:<40} {v4_type:<25} {'REMOVED':<25} ❌")
    
    # Show properties only in v5
    for prop in sorted(only_in_v5):
        v5_type = get_property_type(v5_props[prop])
        print(f"  {prop:<40} {'NEW IN v5':<25} {v5_type:<25} ✨")
    
    # Show variants information
    if schema_name in v4_variants or schema_name in v5_variants:
        print(f"\n  Variants:")
        if schema_name in v4_variants:
            print(f"    v4.1.0: {', '.join(sorted(v4_variants[schema_name]))}")
        if schema_name in v5_variants:
            print(f"    v5.0.0: {', '.join(sorted(v5_variants[schema_name]))}")

print("\n" + "=" * 100)
print("END OF COMPARISON")
print("=" * 100)
