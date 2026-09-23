# Evidence: case_012_arbiter_sequential

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The priority bit fails to advance after granting requester 0.

Set priority_bit to 1 after granting requester 0; retain the existing reset and requester-1 behavior.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -11,7 +11,7 @@
 end
 always @(posedge clk) begin
     if (rst) priority_bit <= 1'b0;
-    else if (grant[0]) priority_bit <= 1'b0;
+    else if (grant[0]) priority_bit <= 1'b1;
     else if (grant[1]) priority_bit <= 1'b0;
 end
 endmodule
```

Regression: PASS

Duration: 10397 ms; Provider calls: 1; tokens in/out: 6257/299.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
