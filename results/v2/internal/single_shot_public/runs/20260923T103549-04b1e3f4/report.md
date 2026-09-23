# Evidence: case_029_pulse_reset

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Reset drives pulse_out high, but the reference expects it low.

Set the registered output low during reset to match the reference behavior.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -4,1 +4,1 @@
-    if (rst) begin previous <= 1'b0; pulse_out <= 1'b1; end
+    if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
```

Regression: PASS

Duration: 10217 ms; Provider calls: 1; tokens in/out: 6038/272.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
