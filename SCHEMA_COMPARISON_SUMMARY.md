# TMF620 Product Catalog Management API - Schema Comparison

## Version Comparison: v4.1.0 (OAS 2.0) vs v5.0.0 (OAS 3.0)

---

## Executive Summary

- **v4.1.0 base schemas:** 112
- **v5.0.0 base schemas:** 129  
- **Common schemas:** 91
- **Only in v4.1.0:** 21
- **Only in v5.0.0:** 38

---

## Key Structural Changes

### 1. Schema Variant Pattern (v5.0.0)
v5.0.0 introduces systematic schema variants:
- **_FVO (First Value Object)**: For creating entities (includes required fields)
- **_MVO (Modification Value Object)**: For updating entities (PATCH operations)
- **Base schemas**: For retrieval (GET operations)

This tripled the total number of schemas from 112 to 271, but only 129 are unique base entities.

### 2. Event Structure Refactoring
In v5.0.0, event schemas were refactored:
- Event properties moved to a base `Event` schema
- Individual events now extend `BaseEvent` via `allOf`
- Removed inline event properties (eventId, eventTime, correlationId, etc.) from each event
- Cleaner inheritance model

---

## Schemas Only in v4.1.0 (Removed in v5.0.0)

### Main Resource Variants (21 schemas)
These were replaced by the _FVO/_MVO pattern in v5.0.0:

1. **Catalog_Create** → replaced by `Catalog_FVO`
2. **Catalog_Update** → replaced by `Catalog_MVO`
3. **Category_Create** → replaced by `Category_FVO`
4. **Category_Update** → replaced by `Category_MVO`
5. **ProductOffering_Create** → replaced by `ProductOffering_FVO`
6. **ProductOffering_Update** → replaced by `ProductOffering_MVO`
7. **ProductOfferingPrice_Create** → replaced by `ProductOfferingPrice_FVO`
8. **ProductOfferingPrice_Update** → replaced by `ProductOfferingPrice_MVO`
9. **ProductSpecification_Create** → replaced by `ProductSpecification_FVO`
10. **ProductSpecification_Update** → replaced by `ProductSpecification_MVO`

### Removed Entities (11 schemas)
1. **Any** - Empty placeholder schema removed
2. **CharacteristicSpecificationBase** - Merged into CharacteristicSpecification hierarchy
3. **ConstraintRef** - Removed reference type
4. **EventSubscription** - Event subscription mechanism changed
5. **EventSubscriptionInput** - Event subscription mechanism changed
6. **POPAlteration** - Product Offering Price alteration entity removed
7. **POPCharge** - Product Offering Price charge entity removed
8. **ProductPriceValue** - Price value structure changed
9. **ProductSpecificationCharacteristic** - Replaced by CharacteristicSpecification
10. **ProductSpecificationCharacteristicRelationship** - Replaced by CharacteristicSpecificationRelationship
11. **RelatedParty** - Replaced by RelatedPartyRefOrPartyRoleRef

### Removed Event Types (1 schema)
1. **CatalogBatchEvent** - Batch event type removed in v5.0.0

---

## Schemas Only in v5.0.0 (New Additions)

### New Base Infrastructure (7 schemas)
1. **BaseEvent** - Base class for all events with common event properties
2. **Entity** - Base entity class with id/href
3. **EntityRef** - Base reference class
4. **Event** - Event wrapper structure
5. **Extensible** - Base extensible class with @type, @baseType, @schemaLocation
6. **Hub** - Hub subscription entity
7. **JsonPatch** / **JsonPatchOperations** - JSON Patch support for PATCH operations

### New Characteristic Value Specifications (16 schemas)
Typed characteristic value specifications for strongly-typed values:

1. **BooleanCharacteristicValueSpecification**
2. **BooleanArrayCharacteristicValueSpecification**
3. **FloatCharacteristicValueSpecification**
4. **FloatArrayCharacteristicValueSpecification**
5. **IntegerCharacteristicValueSpecification**
6. **IntegerArrayCharacteristicValueSpecification**
7. **NumberCharacteristicValueSpecification**
8. **NumberArrayCharacteristicValueSpecification**
9. **StringCharacteristicValueSpecification**
10. **StringArrayCharacteristicValueSpecification**
11. **MapCharacteristicValueSpecification**
12. **MapArrayCharacteristicValueSpecification**
13. **ObjectCharacteristicValueSpecification**
14. **ObjectArrayCharacteristicValueSpecification**

### New Product Entities (5 schemas)
1. **AllowedProductAction** - Defines actions allowed on products
2. **BundledGroupProductOffering** - New bundling structure for grouped offerings
3. **BundledGroupProductOfferingOption** - Options for grouped bundle
4. **Characteristic** - Generic characteristic entity
5. **CharacteristicRelationship** - Relationships between characteristics

### New Specification Entities (2 schemas)
1. **CharacteristicSpecification** - Replaces CharacteristicSpecificationBase
2. **CharacteristicSpecificationRelationship** - Relationships between specs

### New Reference Types (6 schemas)
1. **ExternalIdentifier** - External system identifiers
2. **IntentSpecificationRef** - Intent-based specification reference
3. **PartyRef** - Party reference
4. **PartyRefOrPartyRoleRef** - Polymorphic party reference
5. **PartyRoleRef** - Party role specific reference
6. **PolicyRef** - Policy reference
7. **RelatedPartyRefOrPartyRoleRef** - Replaces RelatedParty

### New Event Types (6 schemas)
1. **ExportJobCreateEvent** / **ExportJobCreateEventPayload**
2. **ExportJobStateChangeEvent** / **ExportJobStateChangeEventPayload**
3. **ImportJobCreateEvent** / **ImportJobCreateEventPayload**
4. **ImportJobStateChangeEvent** / **ImportJobStateChangeEventPayload**

### Renamed Core Entity (1 schema)
1. **ProductCatalog** - Renamed from "Catalog" for clarity

---

## Major Property Changes in Common Schemas

### Pattern: Removal of Polymorphic Properties
Most entities in v5.0.0 removed inline polymorphic properties that moved to base classes:
- `@baseType` → moved to `Extensible` base class
- `@schemaLocation` → moved to `Extensible` base class
- `@type` → moved to `Extensible` base class
- `@referredType` → moved to reference base classes
- `id`, `href` → moved to `Entity` or `EntityRef` base classes

This was done via `allOf` composition instead of inline properties.

### Key Entity Changes

#### **Catalog → ProductCatalog**
Renamed for consistency with other ProductXxx entities.

**New properties in v5.0.0:**
- `externalIdentifier` (array) - External system identifiers

#### **Category**
**New properties in v5.0.0:**
- `externalIdentifier` (array)

#### **ProductOffering**
**New properties in v5.0.0:**
- `allowedProductAction` (array) - Actions allowed on this offering
- `externalIdentifier` (array)
- `intentOffering` (boolean) - Is this an intent-based offering?
- `intentSpecification` (ref) - Reference to intent specification

#### **ProductOfferingPrice**
**Removed properties:**
- Many inline properties moved to base classes via allOf

**New properties in v5.0.0:**
- `externalIdentifier` (array)

#### **ProductSpecification**
**New properties in v5.0.0:**
- `category` (array) - Categories this spec belongs to
- `externalIdentifier` (array)
- `intentSpecification` (ref) - Intent specification reference
- `policy` (array) - Policies applied to this specification

#### **ProductSpecificationRelationship**
**New properties in v5.0.0:**
- `characteristic` (array) - Characteristics of the relationship
- `version` (string) - Version information

---

## Type System Improvements

### v5.0.0 introduces stronger typing:

1. **Discriminators**: All polymorphic types use `discriminator` with `propertyName: '@type'`
2. **oneOf/allOf**: Better composition using JSON Schema features
3. **Typed Characteristics**: 16 new typed characteristic value specifications
4. **Reference Variants**: Separate _FVO and _MVO variants for create vs. update operations

---

## Event Model Changes

### v4.1.0 Event Pattern
Each event had inline properties:
```yaml
CatalogCreateEvent:
  properties:
    eventId: string
    eventTime: string
    eventType: string
    correlationId: string
    domain: string
    title: string
    description: string
    priority: string
    timeOcurred: string
    event: ref:CatalogCreateEventPayload
```

### v5.0.0 Event Pattern
Events extend BaseEvent:
```yaml
CatalogCreateEvent:
  allOf:
    - $ref: '#/components/schemas/BaseEvent'
    - type: object
      properties:
        event: ref:ProductCatalogCreateEventPayload
```

Properties moved to `BaseEvent` which extends `Event`, providing:
- Better inheritance
- Less duplication
- Easier maintenance
- Consistent event structure

---

## API Path Changes

### Renamed in v5.0.0:
- `/catalog` → `/productCatalog`
- `Catalog` resource → `ProductCatalog` resource

### Removed in v5.0.0:
- `/listener/catalogBatchEvent` - Batch events removed

### Added in v5.0.0:
- `/listener/productCatalogCreateEvent`
- `/listener/productCatalogAttributeValueChangeEvent`
- `/listener/productCatalogStateChangeEvent`
- `/listener/productCatalogDeleteEvent`
- `/listener/exportJobCreateEvent`
- `/listener/exportJobStateChangeEvent`
- `/listener/importJobCreateEvent`
- `/listener/importJobStateChangeEvent`

---

## Migration Considerations

### Breaking Changes:
1. **Catalog renamed to ProductCatalog** - All references must be updated
2. **Event structure changed** - Event listeners need updates
3. **RelatedParty removed** - Use RelatedPartyRefOrPartyRoleRef
4. **POPAlteration/POPCharge removed** - Price structure changed
5. **_Create/_Update suffixes** → **_FVO/_MVO pattern**

### New Capabilities:
1. **Intent-based specifications** - Support for intent-driven product specifications
2. **Typed characteristics** - Strong typing for characteristic values
3. **External identifiers** - Better integration with external systems
4. **Policy references** - Policy-driven product specifications
5. **Allowed actions** - Define what actions can be taken on products
6. **JSON Patch support** - RFC 6902 JSON Patch for updates

### Compatibility:
- v5.0.0 is NOT backward compatible with v4.1.0
- Schema structure changed significantly
- Base path changed: `/tmf-api/productCatalogManagement/v4/` → `/productCatalogManagement/v5/`
- Entity names changed (Catalog → ProductCatalog)

---

## Recommendations

1. **Plan for major version upgrade** - This is not a minor update
2. **Update all client code** - Resource names and structures changed
3. **Test event subscriptions** - Event model completely refactored
4. **Leverage new typing** - Use typed characteristic specifications
5. **Review intent-based features** - Consider using intent specifications
6. **Update documentation** - Reflect ProductCatalog naming
7. **Use JSON Patch** - Take advantage of RFC 6902 support for updates

---

*Generated: December 3, 2025*
