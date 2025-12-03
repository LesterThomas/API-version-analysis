## Plan: ODA Component with Dual-Version TMF620 API Support (Simplified)

This plan outlines building an ODA-compliant component that exposes both TMF620 v4.1.0 and v5.0.0 APIs, stores data natively in v5.0.0 format in MongoDB, and provides simple translation for v4.1.0 operations.

### Steps

1. **Create ODA Component foundation with [component.yaml](component.yaml) defining both API versions, [package.json](package.json) for Node.js/Express project, and [src/server.js](src/server.js)** setting up Express with two router groups: `/tmf-api/productCatalogManagement/v4/*` and `/productCatalogManagement/v5/*`, MongoDB connection using Mongoose with v5.0.0 schemas as native models in [src/models/](src/models/)

2. **Implement simple field mapping adapters in [src/adapters/field-mapper.js](src/adapters/field-mapper.js)** using flat mapping objects for the critical renames (`catalog→productCatalog`, `Catalog_Create→ProductCatalog_FVO`, `RelatedParty→RelatedPartyRefOrPartyRoleRef`) and a generic `stripV5Fields()` function to remove v5-only properties (`externalIdentifier`, `intentSpecification`, `policy`, `allowedProductAction`) when translating v5→v4 responses—no recursive logic, just top-level property mapping

3. **Build v4.1.0 controllers in [src/controllers/v4/catalog.controller.js](src/controllers/v4/catalog.controller.js), [productOffering.controller.js](src/controllers/v4/productOffering.controller.js), etc.** that receive v4 requests, apply field renames via `fieldMapper.v4toV5(req.body)`, pass to shared MongoDB service layer, retrieve v5 data, apply `fieldMapper.v5toV4(result)` to strip v5 fields and rename back, return v4-compliant response—accept translation overhead for v4 API simplicity

4. **Build v5.0.0 controllers in [src/controllers/v5/productCatalog.controller.js](src/controllers/v5/productCatalog.controller.js), [productOffering.controller.js](src/controllers/v5/productOffering.controller.js), etc.** that directly read/write MongoDB with no translation layer, implement JSON Patch support using `fast-json-patch` library for PATCH operations, handle all v5 features natively (typed characteristics, external identifiers, intent specifications, policy arrays)

5. **Implement shared business logic in [src/services/catalog.service.js](src/services/catalog.service.js) and [src/services/productSpec.service.js](src/services/productSpec.service.js)** working exclusively with v5 MongoDB models, preserving v5-only fields when v4 clients POST/PATCH (option A: silent preservation for forward compatibility), and event publishers in [src/events/publisher.js](src/events/publisher.js) emitting both v4-format events to `/listener/catalog*Event` subscribers and v5-format events to `/listener/productCatalog*Event` subscribers

6. **Add Kubernetes deployment files in [kubernetes/deployment.yaml](kubernetes/deployment.yaml), [service.yaml](kubernetes/service.yaml), [ingress.yaml](kubernetes/ingress.yaml)** with MongoDB StatefulSet, create basic integration tests in [tests/v4-translation.test.js](tests/v4-translation.test.js) validating field mapping accuracy, generate Swagger UI documentation for both `/v4/api-docs` and `/v5/api-docs` endpoints, configure simple logging with Winston for monitoring v4 translation calls

7. **No Event subscription**. For the initial version of this component, don't attempt to support event subscription - just support the REST HTTP verbs.