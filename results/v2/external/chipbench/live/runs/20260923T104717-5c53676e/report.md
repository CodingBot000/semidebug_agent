# Evidence: chipbench_state_machine_Prob003_non-overlapping_sequence_detect

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: state_machine. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 |
|---|---|---|
| compile | PASS | PASS |
| simulation | PASS | PASS |
| lint | PASS | PASS |
| synthesis | PASS | PASS |

## Attempt 1

After a failed group, the FSM ignores the first bit of the next group.

Use the first bit sampled after a failed six-bit group to choose the next group's matching or failing path, as the successful-group transition already does.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -62,7 +62,7 @@
         sf5:
             nstate=sf6;
         sf6:
-			nstate=s1;
+			nstate=data?sf1:s1;
         default:
             nstate=idle;
         endcase
```

Regression: PASS

Duration: 19478 ms; Provider calls: 1; tokens in/out: 7037/619.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
