# Evidence: case_008_fifo_sequential

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Push is incorrectly enabled when the FIFO is full rather than when it has space.

Accept writes only when the FIFO is not full.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -6,1 +6,1 @@
-wire push = wr_en && full;
+wire push = wr_en && !full;
```

Regression: PASS

Duration: 13196 ms; Provider calls: 1; tokens in/out: 6523/250.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
