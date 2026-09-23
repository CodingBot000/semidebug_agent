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

Missing statement terminator after the increment assignment

Terminate the existing increment assignment in rtl/counter.v:6.

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

Duration: 6092 ms; Provider calls: 1; tokens in/out: 1971/279.
Estimated cost: 0.0031896.

Scripted providers and replay output are not live AI benchmark results.
