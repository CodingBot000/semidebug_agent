# Evidence: case_019_controller_combinational

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The done output decodes the busy state instead of the completion state.

Decode done from state 2, leaving the FSM transitions and busy output unchanged.

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

Duration: 12891 ms; Provider calls: 1; tokens in/out: 6150/323.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
