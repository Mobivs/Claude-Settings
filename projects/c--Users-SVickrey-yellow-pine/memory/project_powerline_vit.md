---
name: Powerline defect detection vision model
description: Training a vision transformer/YOLO model for US power line inspections using autoresearch-style loop. Key concern is dataset relevance — public datasets use non-US equipment. Company has own annotated inspection images with magnification annotations (not standard bbox/segmentation annotations).
type: project
---

Project is to train a vision model for powerline defect detection using Karpathy's autoresearch ratchet loop pattern. Research doc lives in pm-docs/.

**Key issues identified (2026-03-26):**
- Public datasets (InsPLAD, CableInspect-AD) use non-US insulators and poles — different equipment than what the team inspects
- Team has their own inspection images with textual descriptions of defects
- Images have "magnification annotations" (zoom circles/callouts highlighting defect areas) rather than standard ML annotations (bounding boxes, segmentation masks)
- Images available both with and without the magnification annotations

**Actual DB stats (2026-03-26):**
- 62,584 total images (15,602 each of _Z, _P, _T, _W types)
- 2,561 total annotations across 1,326 unique images
- Defect annotations: 140 images (YELLOW=84, ORANGE=32, RED=24)
- GREEN annotations: 1,186 images (clean/no-defect)
- Inspector text is semi-structured, uppercase, includes recommendations
- Common findings: hot terminals, warm fuses, conductor tracking, leaking equipment, lightning arrestor leakage, missing wildlife guards, jumper issues, pole splitting

**Why:** The model needs to detect defects on US-standard utility equipment. Training on Brazilian (InsPLAD) or Canadian (CableInspect-AD) equipment may not transfer well due to different insulator types, pole designs, and hardware.

**How to apply:** Prioritize building a pipeline to convert the team's own annotated images into ML-ready training data. Public datasets may still be useful for pretraining/transfer learning but the final model must perform well on US equipment.
