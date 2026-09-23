# Evidence: case_015_arbiter_combinational

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

The default case grants requester 0 when neither requester is active.

Rejected: Hunk truncated or invalid

Make the unmatched request value, 00, produce no grant.

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

Duration: 9032 ms; Provider calls: 1; tokens in/out: 6257/284.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
