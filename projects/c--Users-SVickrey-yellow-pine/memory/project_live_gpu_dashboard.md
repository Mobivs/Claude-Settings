---
name: Live GPU monitoring dashboard
description: Real-time GPU stats via pynvml + SSE streaming on dashboard at /gpu and main dashboard badge
type: project
---

GPU monitoring uses pynvml (NVML driver bindings) instead of nvidia-smi subprocess. SSE endpoint at `/api/gpu-stream` pushes snapshots every 1 second. The `/gpu` page has rolling charts (5 min history) for utilization, VRAM, temperature (C/F), and power. Main dashboard badge also uses SSE instead of polling.

**Why:** Polling every 5 seconds via nvidia-smi subprocess was wasteful and laggy. pynvml reads take ~1ms with zero subprocess overhead.

**How to apply:** If adding new GPU metrics, add them to `_gpu_snapshot()` in `dashboard/server.py`. The SSE stream will automatically include them.
