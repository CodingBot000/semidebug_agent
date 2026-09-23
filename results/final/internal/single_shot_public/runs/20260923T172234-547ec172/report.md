# Evidence: case_013_arbiter_reset

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The reset value of priority_bit is reversed.

Set the synchronous reset value in rtl/arbiter.v:13 to the priority used by the reference after reset.

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

Duration: 7596 ms; Provider calls: 1; tokens in/out: 3470/424.
Estimated cost: 0.0049394.

Scripted providers and replay output are not live AI benchmark results.
