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

Reset the state register to idle (0), matching the reference behavior.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -3,7 +3,7 @@
 assign busy = (state == 2'd1);
 assign done = (state == 2'd2);
 always @(posedge clk) begin
-    if (rst) state <= 2'd1;
+    if (rst) state <= 2'd0;
     else case (state)
         2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
```

Regression: PASS

Duration: 10738 ms; Provider calls: 1; tokens in/out: 6130/302.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
