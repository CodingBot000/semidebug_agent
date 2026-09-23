# Evidence: case_005_counter_width_signedness

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: width_signedness. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | FAIL | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

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

Duration: 1248 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
