# Evidence: case_002_counter_reset

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Reset polarity is reversed in the RTL.

Change the synchronous reset condition at rtl/counter.v:3 to match the testbench's active-high reset expectation.

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -1,6 +1,6 @@
 module counter(input wire clk, rst, en, output reg [3:0] count);
 always @(posedge clk) begin
-    if (!rst) count <= 4'd0;
+    if (rst) count <= 4'd0;
     else if (en) begin
         if (count == 4'd9) count <= 4'd0;
         else count <= count + 4'd1;
```

Regression: PASS

Duration: 7647 ms; Provider calls: 1; tokens in/out: 3055/356.
Estimated cost: 0.007704399999999999.

Scripted providers and replay output are not live AI benchmark results.
