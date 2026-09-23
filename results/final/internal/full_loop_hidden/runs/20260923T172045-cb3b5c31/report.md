# Evidence: case_015_arbiter_combinational

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

The no-request case incorrectly grants requester 0.

Rejected: Hunk truncated or invalid

Set the default grant to zero when no request matches an explicit case.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -6,7 +6,7 @@
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
         2'b11: grant = priority_bit ? 2'b10 : 2'b01;
-        default: grant = 2'b01;
+        default: grant = 2'b00;
     endcase
 end
```

## Attempt 2

The no-request case incorrectly grants requester 0.

Change the default grant to zero. The diff uses corrected hunk line counts.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -6,6 +6,6 @@
         2'b01: grant = 2'b01;
         2'b10: grant = 2'b10;
         2'b11: grant = priority_bit ? 2'b10 : 2'b01;
-        default: grant = 2'b01;
+        default: grant = 2'b00;
     endcase
 end
```

Regression: PASS

Duration: 12210 ms; Provider calls: 2; tokens in/out: 7382/732.
Estimated cost: 0.0181528.

Scripted providers and replay output are not live AI benchmark results.
