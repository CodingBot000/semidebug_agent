# Evidence: case_005_counter_width_signedness

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: width_signedness. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | FAIL | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The counter is only 3 bits wide, so it wraps from 7 to 0 instead of reaching 8 and 9.

Widen the counter register to four bits so values 0 through 9 are representable.

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -1,4 +1,4 @@
-module counter(input wire clk, rst, en, output reg [2:0] count);
+module counter(input wire clk, rst, en, output reg [3:0] count);
 always @(posedge clk) begin
     if (rst) count <= 4'd0;
     else if (en) begin
```

Regression: PASS

Duration: 13868 ms; Provider calls: 1; tokens in/out: 6380/324.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
