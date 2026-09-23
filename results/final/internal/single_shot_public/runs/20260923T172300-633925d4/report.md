# Evidence: case_018_controller_reset

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Synchronous reset selects busy instead of idle

Change the synchronous reset value at rtl/controller.v:6 from busy (1) to idle (0).

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

Duration: 5808 ms; Provider calls: 1; tokens in/out: 3169/310.
Estimated cost: 0.0037392.

Scripted providers and replay output are not live AI benchmark results.
