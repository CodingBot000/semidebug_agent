# Evidence: case_020_controller_fsm

**MAX_RETRY** — provider `live-openai-api`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

Done state transitions to busy rather than idle

Rejected: Hunk truncated or invalid

Change the state-2 successor to idle at rtl/controller.v:10.

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

Duration: 4901 ms; Provider calls: 1; tokens in/out: 3169/294.
Estimated cost: 0.0035792.

Scripted providers and replay output are not live AI benchmark results.
