# Evidence: case_008_fifo_sequential

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | FAIL | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

The FIFO write enable is inverted: writes are accepted only when full.

Accept a write when write-enable is asserted and the FIFO is not full.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -3,7 +3,7 @@
 reg [7:0] mem [0:3];
 reg [1:0] wr_ptr, rd_ptr;
 reg [2:0] count;
-wire push = wr_en && full;
+wire push = wr_en && !full;
 wire pop = rd_en && !empty;
 assign full = (count == 3'd4);
 assign empty = (count == 3'd0);
```

Regression: PASS

Duration: 14406 ms; Provider calls: 1; tokens in/out: 6505/335.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
