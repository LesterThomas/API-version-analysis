# TMF620 Product Catalog Management API Version Analysis

This repository contains a detailed comparison between two versions of the TMF620 Product Catalog Management API:
- **v4.1.0** (OpenAPI Specification 2.0 / Swagger)
- **v5.0.0** (OpenAPI Specification 3.0)

## Contents

- `TMF620_Product_Catalog_Management_API_v4.1.0_swagger.json` - v4.1.0 API specification (JSON)
- `TMF620_Product_Catalog_Management_API_v4.1.0_swagger.yaml` - v4.1.0 API specification (YAML)
- `TMF620-Product_Catalog_Management-v5.0.0.oas.yaml` - v5.0.0 API specification (YAML)
- `schema_comparison.py` - Python script to compare schemas between versions
- `convert_json_to_yaml.py` - Utility script to convert JSON to YAML
- `SCHEMA_COMPARISON_SUMMARY.md` - Comprehensive comparison report

## Key Findings

### Version Statistics
- **v4.1.0**: 112 base schemas
- **v5.0.0**: 129 base schemas (271 total including variants)
- **Common schemas**: 91
- **Removed in v5.0.0**: 21 schemas
- **Added in v5.0.0**: 38 new schemas

### Major Changes
1. **Catalog renamed to ProductCatalog** - Breaking change for all clients
2. **New schema variant pattern** - Introduction of _FVO and _MVO suffixes
3. **Event model refactoring** - Cleaner inheritance with BaseEvent
4. **Typed characteristics** - 16 new typed characteristic value specifications
5. **Intent-based specifications** - Support for intent-driven products
6. **JSON Patch support** - RFC 6902 compliance for PATCH operations

## Usage

### Run the Comparison

```bash
python schema_comparison.py
```

This will output a detailed side-by-side comparison of all schemas, showing:
- Properties common to both versions
- Properties removed in v5.0.0
- Properties added in v5.0.0
- Type changes between versions

### Convert Specifications

```bash
python convert_json_to_yaml.py
```

Converts the JSON specification to YAML format.

## Analysis Report

See [SCHEMA_COMPARISON_SUMMARY.md](SCHEMA_COMPARISON_SUMMARY.md) for the complete analysis including:
- Detailed schema comparisons
- Migration considerations
- Breaking changes
- New capabilities
- Recommendations

## About TMF620

TMF620 Product Catalog Management is part of the TM Forum Open API suite. It provides a standardized API for managing product catalogs, including:
- Product offerings
- Product specifications
- Pricing
- Categories
- Import/export jobs
- Event notifications

## License

The API specifications are provided by TM Forum. This analysis is for educational and comparison purposes.

## Author

Lester Thomas
