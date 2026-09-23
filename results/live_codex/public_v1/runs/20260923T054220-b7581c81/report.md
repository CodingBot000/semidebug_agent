# Evidence: case_006_fifo_boundary

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The full flag asserts at occupancy 3 instead of the FIFO’s capacity of 4.

Compare count against 4, the capacity of the four-entry FIFO, rather than 3.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -8,1 +8,1 @@
-assign full = (count == 3'd3);
+assign full = (count == 3'd4);
```

Regression: PASS

Duration: 12603 ms; Provider calls: 1; tokens in/out: 6524/259.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
