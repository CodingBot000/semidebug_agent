# Evidence: case_005_counter_width_signedness

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | FAIL | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The three-bit output truncates the count before it reaches nine.

Widen the counter register and output from three bits to four, leaving its reset, enable, and rollover logic unchanged.

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -1,4 +1,4 @@
-module counter(input wire clk, rst, en, output reg [2:0] count);
+module counter(input wire clk, rst, en, output reg [3:0] count);
 always @(posedge clk) begin
     if (rst) count <= 4'd0;
     else if (en) begin
```

Regression: PASS

Duration: 6991 ms; Provider calls: 1; tokens in/out: 3437/350.
Estimated cost: 0.0041928.

Scripted providers and replay output are not live AI benchmark results.
