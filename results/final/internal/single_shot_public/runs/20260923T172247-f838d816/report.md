# Evidence: case_016_controller_fsm

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: fsm. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Idle-to-busy transition tests the wrong polarity of start.

Change the idle-state transition condition at rtl/controller.v:8 to respond to asserted start.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -5,7 +5,7 @@
 always @(posedge clk) begin
     if (rst) state <= 2'd0;
     else case (state)
-        2'd0: if (!start) state <= 2'd1;
+        2'd0: if (start) state <= 2'd1;
         2'd1: if (finish) state <= 2'd2;
         2'd2: state <= 2'd0;
         default: state <= 2'd0;
```

Regression: PASS

Duration: 5905 ms; Provider calls: 1; tokens in/out: 3169/345.
Estimated cost: 0.004089199999999999.

Scripted providers and replay output are not live AI benchmark results.
