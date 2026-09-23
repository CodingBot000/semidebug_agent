# Evidence: case_008_fifo_sequential

**FIXED** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: sequential. Immutable integrity: True.
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

Duration: 1029 ms; Provider calls: 2; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
