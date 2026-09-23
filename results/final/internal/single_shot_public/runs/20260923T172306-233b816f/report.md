# Evidence: case_019_controller_combinational

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The done output decodes the busy state instead of the completion state.

Change only the done state decode at rtl/controller.v:4 to match the completion state.

```diff
--- a/rtl/controller.v
+++ b/rtl/controller.v
@@ -1,7 +1,7 @@
 module controller(input wire clk, rst, start, finish, output wire busy, done);
 reg [1:0] state;
 assign busy = (state == 2'd1);
-assign done = (state == 2'd1);
+assign done = (state == 2'd2);
 always @(posedge clk) begin
     if (rst) state <= 2'd0;
     else case (state)
```

Regression: PASS

Duration: 5857 ms; Provider calls: 1; tokens in/out: 3169/326.
Estimated cost: 0.0038992.

Scripted providers and replay output are not live AI benchmark results.
