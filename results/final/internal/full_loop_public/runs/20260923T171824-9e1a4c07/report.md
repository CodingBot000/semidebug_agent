# Evidence: case_014_arbiter_combinational

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

The two-request grant selection is reversed.

Rejected: Hunk truncated or invalid

Reverse the grant choices when both requests are asserted in rtl/arbiter.v:8.

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

## Attempt 2

The simultaneous-request grant choices are reversed.

Swap the two grant choices at rtl/arbiter.v:8. This is the same RTL hypothesis as the unvalidated prior attempt, with corrected unified-diff hunk counts.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -5,6 +5,6 @@
     case (req)
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
-        2'b11: grant = priority_bit ? 2'b01 : 2'b10;
+        2'b11: grant = priority_bit ? 2'b10 : 2'b01;
         default: grant = 2'b00;
     endcase
```

Regression: PASS

Duration: 13879 ms; Provider calls: 2; tokens in/out: 7369/768.
Estimated cost: 0.018486799999999998.

Scripted providers and replay output are not live AI benchmark results.
