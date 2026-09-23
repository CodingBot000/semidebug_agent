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

The pulse condition detects a high level held across cycles rather than a rising edge.

Rejected: Hunk truncated or invalid

Detect an enabled rising edge by requiring the prior sampled input to be low.

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

The pulse condition uses the previous input without negation, detecting a sustained high rather than a rising edge.

Require the prior sampled input to be low to detect an enabled rising edge. The diff uses a corrected six-line hunk.

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

Duration: 24833 ms; Provider calls: 2; tokens in/out: 12479/657.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
