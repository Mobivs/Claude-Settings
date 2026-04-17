---
name: RTX 5090 GPU upgrade proposal
description: Business justification for upgrading from RTX 3080 Ti (12GB) to RTX 5090 (32GB); presentation Monday 2026-03-30
type: project
---

Proposal saved at `pm-docs/GPU Upgrade Proposal - RTX 5090.md`. Two versions were written: technical (detailed VRAM calculations) and boss-friendly (simplified for non-technical audience). User is presenting Monday 2026-03-30.

**Why:** 12GB VRAM is the single biggest training bottleneck. YOLOv8m@1280 can only do batch=3, larger models (YOLOv8l/x) won't fit at all, and higher resolutions (1600/2048px) are impossible. The 5090's 32GB (2.67x) unlocks all of these.

**How to apply:** If approved, when the 5090 is installed, run `scripts/benchmark_vram.py` to get new limits. The VRAM monitoring system will automatically adapt — Sonnet will see the larger headroom and use bigger batches.
