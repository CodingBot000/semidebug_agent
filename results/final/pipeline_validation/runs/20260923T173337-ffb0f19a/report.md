# Evidence: case_003_counter_boundary

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: boundary. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -2,7 +2,7 @@
 always @(posedge clk) begin
     if (rst) count <= 4'd0;
     else if (en) begin
-        if (count == 4'd8) count <= 4'd0;
+        if (count == 4'd9) count <= 4'd0;
         else count <= count + 4'd1;
     end
 end
```

Regression: PASS

Duration: 1034 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
