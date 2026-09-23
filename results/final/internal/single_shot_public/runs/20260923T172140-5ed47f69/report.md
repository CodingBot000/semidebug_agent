# Evidence: case_003_counter_boundary

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The counter wraps one count too early.

Change the terminal-count comparison at rtl/counter.v:5 from 8 to 9. This proposal has not been independently validated.

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

Duration: 7007 ms; Provider calls: 1; tokens in/out: 3048/346.
Estimated cost: 0.004075.

Scripted providers and replay output are not live AI benchmark results.
