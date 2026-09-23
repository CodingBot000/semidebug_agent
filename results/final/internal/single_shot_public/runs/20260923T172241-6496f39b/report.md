# Evidence: case_014_arbiter_combinational

**MAX_RETRY** — provider `live-openai-api`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

The simultaneous-request grant selection is reversed.

Rejected: Hunk truncated or invalid

Reverse the two grant choices for simultaneous requests in rtl/arbiter.v:8.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -5,7 +5,7 @@
     case (req)
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
-        2'b11: grant = priority_bit ? 2'b01 : 2'b10;
+        2'b11: grant = priority_bit ? 2'b10 : 2'b01;
         default: grant = 2'b00;
     endcase
```

Duration: 5863 ms; Provider calls: 1; tokens in/out: 3482/381.
Estimated cost: 0.0045118.

Scripted providers and replay output are not live AI benchmark results.
