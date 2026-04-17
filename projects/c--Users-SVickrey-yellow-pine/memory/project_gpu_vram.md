---
name: GPU VRAM management system
description: VRAM benchmarking, per-experiment monitoring, and Sonnet prompt integration for batch size optimization on RTX 3080 Ti
type: project
---

Peak VRAM is now tracked per experiment via pynvml background thread (2s sampling). Stored in `experiments.peak_vram_mb` and `experiments.vram_total_mb`. Sonnet sees VRAM headroom in experiment history and prompt instructs it to maximize batch within safe limits.

**Why:** Sonnet repeatedly proposed batch sizes that exceeded GPU VRAM (batch=8 on YOLOv8m@1280), locking up training. Hardcoded limits were guesses. Now we have benchmarked limits (autobatch inference / 6) and empirical per-experiment feedback.

**How to apply:** The system is self-correcting — as VRAM data accumulates, Sonnet learns optimal batch sizes for any model/resolution combo. When the GPU is upgraded (5090 planned), Sonnet will automatically see the larger VRAM and use bigger batches without code changes.
