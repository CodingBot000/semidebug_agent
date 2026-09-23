# Evidence: case_001_counter_syntax

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: syntax. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | FAIL | PASS |
| simulation | NOT RUN | PASS |
| lint | FAIL | PASS |
| synthesis | FAIL | PASS |

## Attempt 1

The increment assignment is missing a semicolon, causing the parser to reject the following `end`.

Terminate the increment assignment in the only mutable RTL file.

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

Duration: 11616 ms; Provider calls: 1; tokens in/out: 6243/301.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
