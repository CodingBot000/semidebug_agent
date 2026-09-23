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

The reset value of priority_bit is inverted relative to the reference.

Set the reset priority to 0 so simultaneous requests initially grant requester 0, matching the reference state.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -10,7 +10,7 @@
     endcase
 end
 always @(posedge clk) begin
-    if (rst) priority_bit <= 1'b1;
+    if (rst) priority_bit <= 1'b0;
     else if (grant[0]) priority_bit <= 1'b1;
     else if (grant[1]) priority_bit <= 1'b0;
 end
```

Regression: PASS

Duration: 11012 ms; Provider calls: 1; tokens in/out: 6253/324.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
