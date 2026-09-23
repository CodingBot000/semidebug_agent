# Evidence: case_018_controller_reset

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: reset. Immutable integrity: True.
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
@@ -3,7 +3,7 @@
 assign busy = (state == 2'd1);
 assign done = (state == 2'd2);
 always @(posedge clk) begin
-    if (rst) state <= 2'd1;
+    if (rst) state <= 2'd0;
     else case (state)
         2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
```

Regression: PASS

Duration: 1147 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
