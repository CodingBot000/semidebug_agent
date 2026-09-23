# Evidence: case_009_fifo_reset

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Reset initializes FIFO occupancy to one instead of zero.

Rejected: Hunk truncated or invalid

Initialize the occupancy counter to zero on reset, matching the reset pointers and empty indication.

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

## Attempt 2

Reset initializes FIFO occupancy to one instead of zero.

Reset the occupancy counter to zero so it agrees with the reset pointers and empty indication. The previous diff had an incorrect hunk line count.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -9,6 +9,6 @@
 assign empty = (count == 3'd0);
 always @(posedge clk) begin
     if (rst) begin
-        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd1; data_out <= 8'd0;
+        wr_ptr <= 2'd0; rd_ptr <= 2'd0; count <= 3'd0; data_out <= 8'd0;
     end else begin
         if (push) begin mem[wr_ptr] <= data_in; wr_ptr <= wr_ptr + 2'd1; end
```

Regression: PASS

Duration: 13299 ms; Provider calls: 2; tokens in/out: 10097/772.
Estimated cost: 0.0239828.

Scripted providers and replay output are not live AI benchmark results.
