# Evidence: case_027_pulse_combinational

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

The pulse condition uses the previous high level rather than detecting a low-to-high transition.

Rejected: Hunk truncated or invalid

Invert the stored previous-sample condition to produce a one-cycle pulse on an enabled rising edge.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -4,7 +4,7 @@
     if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
         previous <= signal_in;
-        pulse_out <= enable && signal_in && previous;
+        pulse_out <= enable && signal_in && !previous;
     end
 end
```

## Attempt 2

The pulse condition checks for a previously high input instead of a rising edge.

Invert the previous-sample check. This is the same RTL correction as the prior attempt, with a valid six-line unified-diff hunk.

```diff
--- a/rtl/pulse.v
+++ b/rtl/pulse.v
@@ -4,6 +4,6 @@
     if (rst) begin previous <= 1'b0; pulse_out <= 1'b0; end
     else begin
         previous <= signal_in;
-        pulse_out <= enable && signal_in && previous;
+        pulse_out <= enable && signal_in && !previous;
     end
 end
```

Regression: PASS

Duration: 21731 ms; Provider calls: 2; tokens in/out: 12455/655.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
