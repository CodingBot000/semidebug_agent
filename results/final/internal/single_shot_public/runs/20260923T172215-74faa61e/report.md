# Evidence: case_009_fifo_reset

**MAX_RETRY** — provider `live-openai-api`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

Reset initializes occupancy to one instead of zero.

Rejected: Hunk truncated or invalid

Initialize the occupancy counter to zero on reset in rtl/fifo.v:12.

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
```

Duration: 5950 ms; Provider calls: 1; tokens in/out: 4828/329.
Estimated cost: 0.004261.

Scripted providers and replay output are not live AI benchmark results.
