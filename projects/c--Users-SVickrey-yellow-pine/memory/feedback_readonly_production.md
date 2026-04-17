---
name: Never modify production databases
description: Production databases (thermal_inspector, company_ops) are READ ONLY — never INSERT/UPDATE/DELETE. Use a separate yellow_pine database for training data.
type: feedback
---

Never modify data in the production `thermal_inspector` or `company_ops` databases. These power the ThermalInspector and inspection-master apps used in the field.

**Why:** Annotations, reports, images, and all related data are actively used by the inspection apps and team. Any modification could break production workflows or corrupt inspection records.

**How to apply:**
- All queries against production DBs must be SELECT only
- Training data exports, class label mappings, bbox conversions, experiment tracking — all go in the separate `yellow_pine` database
- Always maintain a mapping back to source `image_uuid` so we can trace provenance without modifying the source
