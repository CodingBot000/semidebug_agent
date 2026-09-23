# Evidence: case_006_fifo_boundary

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The full flag asserts at three entries instead of four.

Compare count with four so the fourth write is accepted and full asserts only afterward.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -6,5 +6,5 @@
 wire push = wr_en && !full;
 wire pop = rd_en && !empty;
-assign full = (count == 3'd3);
+assign full = (count == 3'd4);
 assign empty = (count == 3'd0);
 always @(posedge clk) begin
```

Regression: PASS

Duration: 6992 ms; Provider calls: 1; tokens in/out: 4828/321.
Estimated cost: 0.0109004.

Scripted providers and replay output are not live AI benchmark results.
