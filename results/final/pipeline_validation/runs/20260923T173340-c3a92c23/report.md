# Evidence: case_007_fifo_connectivity

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: connectivity. Immutable integrity: True.
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
@@ -12,7 +12,7 @@
         wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd0; data_out <= 8'd0;
     end else begin
         if (push) begin mem[wr_ptr] <= data_in; wr_ptr <= wr_ptr + 2'd1; end
-        if (pop) begin data_out <= mem[wr_ptr]; rd_ptr <= rd_ptr + 2'd1; end
+        if (pop) begin data_out <= mem[rd_ptr]; rd_ptr <= rd_ptr + 2'd1; end
         case ({push,pop})
             2'b10: count <= count + 3'd1;
             2'b01: count <= count - 3'd1;
```

Regression: PASS

Duration: 1075 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
