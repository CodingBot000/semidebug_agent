# Evidence: case_020_controller_fsm

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

DONE transitions to BUSY instead of IDLE.

Change the DONE-state successor at rtl/controller.v:10 from BUSY to IDLE.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -8,5 +8,5 @@
         2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
-        2'd2: state <= 2'd1;
+        2'd2: state <= 2'd0;
         default: state <= 2'd0;
     endcase
```

Regression: PASS

Duration: 6156 ms; Provider calls: 1; tokens in/out: 3169/317.
Estimated cost: 0.0075423999999999995.

Scripted providers and replay output are not live AI benchmark results.
