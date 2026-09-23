# Evidence: case_008_fifo_sequential

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The write enable condition is inverted.

Change the write condition in rtl/fifo.v:6 to accept writes while the FIFO is not full.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -6,1 +6,1 @@
-wire push = wr_en && full;
+wire push = wr_en && !full;
```

Regression: PASS

Duration: 7133 ms; Provider calls: 1; tokens in/out: 4827/299.
Estimated cost: 0.0039608.

Scripted providers and replay output are not live AI benchmark results.
