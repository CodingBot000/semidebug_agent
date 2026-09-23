# Evidence: case_003_counter_boundary

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The counter wraps one enabled cycle too early: it resets at 8, but the expected sequence includes 9 before returning to 0.

Change the wrap threshold from 8 to 9 so an enabled count advances from 8 to 9, then wraps to 0 on the next enabled edge.

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

Duration: 11561 ms; Provider calls: 1; tokens in/out: 6020/348.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
