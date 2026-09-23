# Evidence: case_017_controller_fsm

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

The busy state exits directly to idle instead of entering the done state.

Change the finish transition at rtl/controller.v:9 to enter the existing done state for one clock cycle; line 10 already returns that state to idle.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -6,7 +6,7 @@
     if (rst) state <= 2'd0;
     else case (state)
         2'd0: if (start) state <= 2'd1;
-        2'd1: if (finish) state <= 2'd0;
+        2'd1: if (finish) state <= 2'd2;
         2'd2: state <= 2'd0;
         default: state <= 2'd0;
     endcase
```

Regression: PASS

Duration: 6777 ms; Provider calls: 1; tokens in/out: 3169/384.
Estimated cost: 0.0044792.

Scripted providers and replay output are not live AI benchmark results.
