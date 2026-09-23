# Evidence: case_006_fifo_boundary

**MAX_RETRY** — provider `live-openai-api`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

The full flag asserts at three entries instead of four.

Rejected: Hunk truncated or invalid

Change the full threshold to the four-entry capacity at rtl/fifo.v:8.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -6,7 +6,7 @@
 wire push = wr_en && !full;
 wire pop = rd_en && !empty;
-assign full = (count == 3'd3);
+assign full = (count == 3'd4);
 assign empty = (count == 3'd0);
 always @(posedge clk) begin
```

Duration: 6491 ms; Provider calls: 1; tokens in/out: 4828/357.
Estimated cost: 0.004541.

Scripted providers and replay output are not live AI benchmark results.
