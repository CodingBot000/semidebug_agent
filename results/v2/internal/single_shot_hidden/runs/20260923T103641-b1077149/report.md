# Evidence: case_020_controller_fsm

**MAX_RETRY** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

The DONE state incorrectly transitions to BUSY instead of IDLE.

Rejected: Hunk truncated or invalid

Make the DONE-to-IDLE transition match the reference FSM.

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

Duration: 10734 ms; Provider calls: 1; tokens in/out: 6132/314.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
