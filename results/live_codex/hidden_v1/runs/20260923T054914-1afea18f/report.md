# Evidence: case_020_controller_fsm

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

The done state transitions to busy instead of idle.

Rejected: Hunk truncated or invalid

Make the done-state transition return to idle, matching the reference FSM.

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
```

## Attempt 2

The done state returns to busy instead of idle.

Correct the done-state transition to idle. Unlike the rejected proposal, the hunk header accurately counts its six context and changed lines.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -7,6 +7,6 @@
     else case (state)
         2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
-        2'd2: state <= 2'd1;
+        2'd2: state <= 2'd0;
         default: state <= 2'd0;
     endcase
```

Regression: PASS

Duration: 28226 ms; Provider calls: 2; tokens in/out: 12697/704.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
