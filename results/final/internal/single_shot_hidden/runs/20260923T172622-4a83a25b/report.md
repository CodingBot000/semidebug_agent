# Evidence: case_015_arbiter_combinational

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

The no-request case incorrectly grants requester 0.

Rejected: Hunk truncated or invalid

Set the default grant to zero for the no-request case at rtl/arbiter.v:9.

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

Duration: 5776 ms; Provider calls: 1; tokens in/out: 3482/323.
Estimated cost: 0.0039318.

Scripted providers and replay output are not live AI benchmark results.
