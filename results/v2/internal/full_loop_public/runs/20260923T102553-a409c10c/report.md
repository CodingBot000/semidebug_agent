# Evidence: case_013_arbiter_reset

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

The reset value of priority_bit is inverted relative to the reference behavior.

Reset priority_bit to 0 to match the reference arbitration state.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -12,5 +12,5 @@
 always @(posedge clk) begin
-    if (rst) priority_bit <= 1'b1;
+    if (rst) priority_bit <= 1'b0;
     else if (grant[0]) priority_bit <= 1'b1;
     else if (grant[1]) priority_bit <= 1'b0;
 end
```

Regression: PASS

Duration: 11016 ms; Provider calls: 1; tokens in/out: 6257/350.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
