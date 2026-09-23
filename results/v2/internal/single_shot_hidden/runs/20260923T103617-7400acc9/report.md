# Evidence: case_010_fifo_boundary

**MAX_RETRY** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: boundary. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

A pop increments occupancy instead of decrementing it.

Rejected: Hunk truncated or invalid

Decrement count on a pop-only cycle; leave simultaneous push/pop occupancy unchanged.

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

Duration: 14415 ms; Provider calls: 1; tokens in/out: 6506/315.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
