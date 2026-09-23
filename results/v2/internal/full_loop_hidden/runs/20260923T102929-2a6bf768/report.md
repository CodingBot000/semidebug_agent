# Evidence: case_010_fifo_boundary

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

A pop without a push increments the occupancy count instead of decrementing it.

Rejected: Hunk truncated or invalid

Decrement count in the pop-only case.

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

The pop-only case increments occupancy instead of decrementing it.

Correct the pop-only count update. This diff replaces the malformed prior hunk with valid line counts and context.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -14,7 +14,7 @@
         if (push) begin mem[wr_ptr] <= data_in; wr_ptr <= wr_ptr + 2'd1; end
         if (pop) begin data_out <= mem[rd_ptr]; rd_ptr <= rd_ptr + 2'd1; end
         case ({push,pop})
             2'b10: count <= count + 3'd1;
-            2'b01: count <= count + 3'd1;
+            2'b01: count <= count - 3'd1;
             default: count <= count;
         endcase
```

Regression: PASS

Duration: 22264 ms; Provider calls: 2; tokens in/out: 13389/770.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
