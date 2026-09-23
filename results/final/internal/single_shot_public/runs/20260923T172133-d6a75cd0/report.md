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

The synchronous reset uses the opposite polarity from the testbench.

Make the synchronous reset active high, matching the testbench's expected state update.

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

Duration: 6880 ms; Provider calls: 1; tokens in/out: 3055/374.
Estimated cost: 0.0043564.

Scripted providers and replay output are not live AI benchmark results.
