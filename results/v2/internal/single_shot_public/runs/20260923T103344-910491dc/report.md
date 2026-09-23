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

The idle-to-busy transition uses the opposite start polarity from the reference model.

Make the idle state advance to busy on asserted start, matching the reference transition.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -8,1 +8,1 @@
-        2'd0: if (!start) state <= 2'd1;
+        2'd0: if (start) state <= 2'd1;
```

Regression: PASS

Duration: 11316 ms; Provider calls: 1; tokens in/out: 6132/274.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
