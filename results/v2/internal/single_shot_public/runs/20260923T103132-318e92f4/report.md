# Evidence: case_002_counter_reset

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

The reset polarity is inverted in the RTL.

Make the synchronous reset active high to match the testbench's expected behavior.

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

Duration: 12261 ms; Provider calls: 1; tokens in/out: 6018/384.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
