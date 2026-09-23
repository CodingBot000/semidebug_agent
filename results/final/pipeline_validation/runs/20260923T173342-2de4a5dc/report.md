# Evidence: case_009_fifo_reset

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: reset. Immutable integrity: True.
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
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -9,7 +9,7 @@
 assign empty = (count == 3'd0);
 always @(posedge clk) begin
     if (rst) begin
-        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd1; data_out <= 8'd0;
+        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd0; data_out <= 8'd0;
     end else begin
         if (push) begin mem[wr_ptr] <= data_in; wr_ptr <= wr_ptr + 2'd1; end
         if (pop) begin data_out <= mem[rd_ptr]; rd_ptr <= rd_ptr + 2'd1; end
```

Regression: PASS

Duration: 1472 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
