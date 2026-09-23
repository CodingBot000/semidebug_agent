# Evidence: case_017_controller_fsm

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The finish transition skips the done state.

Change the busy-state finish transition to enter the existing one-cycle done state before returning to idle.

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

Duration: 13212 ms; Provider calls: 1; tokens in/out: 6148/325.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
