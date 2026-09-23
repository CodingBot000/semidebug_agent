# Evidence: case_004_counter_sequential

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

The enable condition is inverted.

Change the increment-and-wrap branch at rtl/counter.v:4 to execute when en is asserted. With en low, the register retains its value.

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

Duration: 7791 ms; Provider calls: 1; tokens in/out: 3057/342.
Estimated cost: 0.007568399999999999.

Scripted providers and replay output are not live AI benchmark results.
