# Evidence: case_017_controller_fsm

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Finish transitions directly to idle instead of the done state.

Rejected: Hunk truncated or invalid

Change the busy-to-finished transition at rtl/controller.v:9 to enter state 2. The existing state-2 transition then returns to idle on the following clock.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -7,7 +7,7 @@
     else case (state)
         2'd0: if (start) state <= 2'd1;
-        2'd1: if (finish) state <= 2'd0;
+        2'd1: if (finish) state <= 2'd2;
         2'd2: state <= 2'd0;
         default: state <= 2'd0;
```

## Attempt 2

The finish transition skips the done state.

Change the state-1 finish transition at rtl/controller.v:9 to enter state 2. The existing transition at line 10 returns to idle on the next clock.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -7,5 +7,5 @@
     else case (state)
         2'd0: if (start) state <= 2'd1;
-        2'd1: if (finish) state <= 2'd0;
+        2'd1: if (finish) state <= 2'd2;
         2'd2: state <= 2'd0;
         default: state <= 2'd0;
```

Regression: PASS

Duration: 12867 ms; Provider calls: 2; tokens in/out: 6766/719.
Estimated cost: 0.016790799999999998.

Scripted providers and replay output are not live AI benchmark results.
