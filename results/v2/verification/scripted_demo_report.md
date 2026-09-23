# Evidence: demo_fifo_off_by_one_v2

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: boundary. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Scripted V2 demo proposal (known fix)

Known fix supplied only for the V2 hidden-regression demo

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -5,7 +5,7 @@
 reg [2:0] count;
 wire push = wr_en && !full;
 wire pop = rd_en && !empty;
-assign full = (count == 3'd3);
+assign full = (count == 3'd4);
 assign empty = (count == 3'd0);
 always @(posedge clk) begin
     if (rst) begin
```

Regression: PASS

Duration: 256 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
