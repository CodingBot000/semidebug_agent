# Evidence: case_019_controller_combinational

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: combinational. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -1,7 +1,7 @@
 module controller(input wire clk, rst, start, finish, output wire busy, done);
 reg [1:0] state;
 assign busy = (state == 2'd1);
-assign done = (state == 2'd1);
+assign done = (state == 2'd2);
 always @(posedge clk) begin
     if (rst) state <= 2'd0;
     else case (state)
```

Regression: PASS

Duration: 1009 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
