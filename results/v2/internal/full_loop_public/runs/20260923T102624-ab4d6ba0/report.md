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

The busy state transitions directly to idle on finish, skipping the done state.

Change the finish transition to enter the existing done state. This proposal is unvalidated.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -9,1 +9,1 @@
-        2'd1: if (finish) state <= 2'd0;
+        2'd1: if (finish) state <= 2'd2;
```

Regression: PASS

Duration: 10671 ms; Provider calls: 1; tokens in/out: 6130/279.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
