# Evidence: case_010_fifo_boundary

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

Pop-only operations increment occupancy instead of decrementing it.

Rejected: Hunk truncated or invalid

Change the pop-only count update at rtl/fifo.v:18 to subtract one. This proposal has not been independently validated.

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

Duration: 7044 ms; Provider calls: 1; tokens in/out: 4864/395.
Estimated cost: 0.0049282.

Scripted providers and replay output are not live AI benchmark results.
