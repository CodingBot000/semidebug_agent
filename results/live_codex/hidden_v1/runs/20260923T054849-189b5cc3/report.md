# Evidence: case_015_arbiter_combinational

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

The default case incorrectly grants requester 0 when req is 00.

Rejected: Hunk truncated or invalid

Return no grant when neither requester is active.

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

The default case grants requester 0 when req is 00.

Return no grant when neither requester is active, using a valid six-line diff hunk.

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

Duration: 25247 ms; Provider calls: 2; tokens in/out: 12897/659.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
