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

Change the increment branch at rtl/counter.v:4 to execute when en is asserted, leaving reset, wraparound, and disabled-cycle hold behavior unchanged.

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

Duration: 6577 ms; Provider calls: 1; tokens in/out: 3057/368.
Estimated cost: 0.0042968.

Scripted providers and replay output are not live AI benchmark results.
