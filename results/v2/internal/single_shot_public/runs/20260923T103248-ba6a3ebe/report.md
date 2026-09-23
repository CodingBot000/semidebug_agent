# Evidence: case_009_fifo_reset

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

Reset initializes the FIFO occupancy to one instead of zero.

Initialize count to zero on reset so the FIFO reports empty immediately after reset.

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

Duration: 11989 ms; Provider calls: 1; tokens in/out: 6504/371.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
