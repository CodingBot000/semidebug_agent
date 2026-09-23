# Evidence: case_020_controller_fsm

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: fsm. Immutable integrity: True.
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
@@ -7,7 +7,7 @@
     else case (state)
         2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
-        2'd2: state <= 2'd1;
+        2'd2: state <= 2'd0;
         default: state <= 2'd0;
     endcase
 end
```

Regression: PASS

Duration: 1036 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
