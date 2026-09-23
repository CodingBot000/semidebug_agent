# Evidence: case_001_counter_syntax

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: syntax. Immutable integrity: True.
Reasoning: unspecified; billing: unspecified.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | FAIL | PASS |
| simulation | NOT RUN | PASS |
| lint | FAIL | PASS |
| synthesis | FAIL | PASS |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -3,7 +3,7 @@
     if (rst) count <= 4'd0;
     else if (en) begin
         if (count == 4'd9) count <= 4'd0;
-        else count <= count + 4'd1
+        else count <= count + 4'd1;
     end
 end
 endmodule
```

Regression: PASS

Duration: 1153 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
