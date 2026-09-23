# Evidence: case_008_fifo_sequential

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: sequential. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

The FIFO rejects writes when it is not full.

Rejected: Hunk truncated or invalid

Allow a write when wr_en is asserted and the FIFO is not full. Only rtl/fifo.v:6 changes.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -4,7 +4,7 @@
 reg [1:0] wr_ptr, rd_ptr;
 reg [2:0] count;
-wire push = wr_en && full;
+wire push = wr_en && !full;
 wire pop = rd_en && !empty;
 assign full = (count == 3'd4);
 assign empty = (count == 3'd0);
```

## Attempt 2

The FIFO accepts writes only when full, instead of when space is available.

Correct the write-accept condition at rtl/fifo.v:6. This proposal uses a valid six-line hunk against the original source.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -4,6 +4,6 @@
 reg [1:0] wr_ptr, rd_ptr;
 reg [2:0] count;
-wire push = wr_en && full;
+wire push = wr_en && !full;
 wire pop = rd_en && !empty;
 assign full = (count == 3'd4);
 assign empty = (count == 3'd0);
```

Regression: PASS

Duration: 13414 ms; Provider calls: 2; tokens in/out: 10074/739.
Estimated cost: 0.0236068.

Scripted providers and replay output are not live AI benchmark results.
