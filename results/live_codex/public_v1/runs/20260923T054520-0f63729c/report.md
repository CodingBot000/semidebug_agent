# Evidence: case_018_controller_reset

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

Reset initializes the FSM to busy instead of idle.

Reset the FSM to idle (state 0), matching the reference behavior.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -5,3 +5,3 @@
 always @(posedge clk) begin
-    if (rst) state <= 2'd1;
+    if (rst) state <= 2'd0;
     else case (state)
```

Regression: PASS

Duration: 11856 ms; Provider calls: 1; tokens in/out: 6148/258.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
