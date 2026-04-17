---
name: GREEN annotation meaning varies by report_type
description: In the thermal_inspector DB, GREEN means different things for construction vs thermal reports — critical for correct training label assignment
type: feedback
---

GREEN annotations have different meanings depending on `report_type`:
- **construction (visual) GREEN** = lowest-level discrepancy, still a defect. Use as positive defect training data.
- **thermal GREEN** = "this is normal/good" — inspector annotates to show contrast with a bad area. Use as negative (clean) example for thermal anomaly detection.

**Why:** Different inspectors use the annotation system differently. Visual inspectors mark all discrepancies including minor ones as GREEN. Thermal inspectors use GREEN to highlight the normal baseline alongside the actual defect.

**How to apply:** When exporting annotations for training, filter by `report_type`:
- For visual defect model: ALL construction annotations (GREEN through RED) are positive defect examples
- For thermal model: only YELLOW/ORANGE/RED are defect examples; GREEN is negative/normal
