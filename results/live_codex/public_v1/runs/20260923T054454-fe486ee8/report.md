# Evidence: case_016_controller_fsm

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

The idle-to-busy transition uses the wrong start polarity.

Change only the idle-state transition condition to match the reference behavior.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -7,3 +7,3 @@
     else case (state)
-        2'd0: if (!start) state <= 2'd1;
+        2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
```

Regression: PASS

Duration: 12748 ms; Provider calls: 1; tokens in/out: 6150/279.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
