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

The FIFO asserts full at three entries instead of four.

Set the full threshold to the four-entry capacity.

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

Duration: 11754 ms; Provider calls: 1; tokens in/out: 6508/339.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
