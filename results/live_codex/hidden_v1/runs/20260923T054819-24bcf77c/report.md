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

The FIFO increments occupancy on a pop-only cycle instead of decrementing it.

Rejected: Hunk truncated or invalid

Decrement count for a pop-only cycle.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -16,7 +16,7 @@
         case ({push,pop})
             2'b10: count <= count + 3'd1;
-            2'b01: count <= count + 3'd1;
+            2'b01: count <= count - 3'd1;
             default: count <= count;
         endcase
```

## Attempt 2

Pop-only cycles increment occupancy instead of decrementing it.

Correct the pop-only count update. The previous diff used a seven-line hunk header for five lines; this proposal uses the exact five-line hunk.

```diff
--- a/rtl/fifo.v
+++ b/rtl/fifo.v
@@ -16,5 +16,5 @@
         case ({push,pop})
             2'b10: count <= count + 3'd1;
-            2'b01: count <= count + 3'd1;
+            2'b01: count <= count - 3'd1;
             default: count <= count;
         endcase
```

Regression: PASS

Duration: 29485 ms; Provider calls: 2; tokens in/out: 13390/740.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
