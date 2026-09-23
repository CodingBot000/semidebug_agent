# Evidence: case_012_arbiter_sequential

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Granting requester 0 fails to rotate priority.

Set priority_bit after granting requester 0 so a subsequent simultaneous request favors requester 1.

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

Duration: 6280 ms; Provider calls: 1; tokens in/out: 3839/328.
Estimated cost: 0.0040532.

Scripted providers and replay output are not live AI benchmark results.
