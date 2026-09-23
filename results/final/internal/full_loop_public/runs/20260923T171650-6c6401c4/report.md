# Evidence: case_001_counter_syntax

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: syntax. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | FAIL | PASS |
| simulation | NOT RUN | PASS |
| lint | FAIL | PASS |
| synthesis | FAIL | PASS |

## Attempt 1

Missing semicolon after the increment assignment

Add the missing statement terminator at rtl/counter.v:6 without changing the counter logic.

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

Duration: 7567 ms; Provider calls: 1; tokens in/out: 1971/290.
Estimated cost: 0.0048763999999999995.

Scripted providers and replay output are not live AI benchmark results.
