# Evidence: case_009_fifo_reset

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Reset initializes occupancy to one instead of zero.

Initialize the FIFO occupancy to zero on reset.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -12,1 +12,1 @@
-        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd1; data_out <= 8'd0;
+        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd0; data_out <= 8'd0;
```

Regression: PASS

Duration: 11626 ms; Provider calls: 1; tokens in/out: 6524/269.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
