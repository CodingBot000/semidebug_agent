# Evidence: case_004_counter_sequential

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

The enable condition is inverted, so the counter holds when en is asserted.

Count on enabled clock edges rather than disabled ones.

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -1,7 +1,7 @@
 module counter(input wire clk, rst, en, output reg [3:0] count);
 always @(posedge clk) begin
     if (rst) count <= 4'd0;
-    else if (!en) begin
+    else if (en) begin
         if (count == 4'd9) count <= 4'd0;
         else count <= count + 4'd1;
     end
```

Regression: PASS

Duration: 11203 ms; Provider calls: 1; tokens in/out: 6020/327.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
