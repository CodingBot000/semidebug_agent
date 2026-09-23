# Evidence: case_014_arbiter_combinational

**MAX_RETRY** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: combinational. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: Iteration budget exhausted

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | NOT RUN |
| simulation | FAIL | NOT RUN |
| lint | PASS | NOT RUN |
| synthesis | PASS | NOT RUN |

## Attempt 1

The both-request grant selection is reversed relative to the priority state.

Rejected: Hunk truncated or invalid

Reverse the grant choices when both requests are asserted so priority_bit=0 selects requester 0 and priority_bit=1 selects requester 1.

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

Duration: 11061 ms; Provider calls: 1; tokens in/out: 6263/350.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
