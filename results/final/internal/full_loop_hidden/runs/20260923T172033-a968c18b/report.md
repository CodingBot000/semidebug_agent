# Evidence: case_010_fifo_boundary

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Pop-only cycles incorrectly increment FIFO occupancy.

Rejected: Hunk truncated or invalid

Change the pop-only occupancy update at rtl/fifo.v:18 to decrement count. The push-only and simultaneous-operation cases remain unchanged.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -15,7 +15,7 @@
         if (pop) begin data_out <= mem[rd_ptr]; rd_ptr <= rd_ptr + 2'd1; end
         case ({push,pop})
             2'b10: count <= count + 3'd1;
-            2'b01: count <= count + 3'd1;
+            2'b01: count <= count - 3'd1;
             default: count <= count;
         endcase
```

## Attempt 2

Pop-only cycles incorrectly increment occupancy.

Correct the pop-only count update at rtl/fifo.v:18. Unlike the prior attempt, this diff has a six-line hunk matching its context.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -15,6 +15,6 @@
         if (pop) begin data_out <= mem[rd_ptr]; rd_ptr <= rd_ptr + 2'd1; end
         case ({push,pop})
             2'b10: count <= count + 3'd1;
-            2'b01: count <= count + 3'd1;
+            2'b01: count <= count - 3'd1;
             default: count <= count;
         endcase
```

Regression: PASS

Duration: 12104 ms; Provider calls: 2; tokens in/out: 10148/734.
Estimated cost: 0.023704799999999998.

Scripted providers and replay output are not live AI benchmark results.
