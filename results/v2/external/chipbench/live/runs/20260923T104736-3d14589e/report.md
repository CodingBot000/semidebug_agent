# Evidence: chipbench_state_machine_Prob004_continuous_input_sequence_detect2

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: state_machine. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|---|
| compile | PASS | PASS | PASS | PASS |
| simulation | PASS | PASS | PASS | PASS |
| lint | PASS | PASS | PASS | PASS |
| synthesis | PASS | PASS | PASS | PASS |

## Attempt 1

The FSM discards partial or complete matches on invalid cycles and loses an overlapping prefix after 01101.

Preserve the FSM state on invalid cycles and retain the overlapping 01 prefix after 01101.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -54,1 +54,1 @@
-			else nstate = idle;					//Data invalid, stay in s3_d011
+			else nstate = s3_d011;				//Data invalid, stay in s3_d011
@@ -59,1 +59,1 @@
-					else nstate = idle;			//Data valid but is 1, does not match target sequence, next state is idle
+					else nstate = s2_d01;		//Data valid but is 1, suffix 01 matches the first two bits
@@ -61,1 +61,1 @@
-			else nstate = idle;					//Data invalid, next state is idle
+			else nstate = s4_d0110;			//Data invalid, stay in s4_d0110
```

Regression: FAIL

## Attempt 2

The completed-match state should not hold match high through invalid cycles; it should retain the trailing 0 as a prefix instead.

Preserve an incomplete 011 prefix across invalid cycles. After a completed 0110, retain its trailing 0 as the next prefix rather than holding the match state; retain the overlapping 01 prefix after a subsequent valid 1.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -54 +54 @@
-			else nstate = idle;					//Data invalid, stay in s3_d011
+			else nstate = s3_d011;				//Data invalid, stay in s3_d011
@@ -59 +59 @@
-					else nstate = idle;			//Data valid but is 1, does not match target sequence, next state is idle
+					else nstate = s2_d01;		//Data valid but is 1, suffix 01 remains matched
@@ -61 +61 @@
-			else nstate = idle;					//Data invalid, next state is idle
+			else nstate = s1_d0;				//Data invalid, retain trailing 0 as prefix
```

Regression: FAIL

## Attempt 3

An invalid cycle incorrectly discards the partial 011 match.

Keep the partial 011 match when data_valid is low; leave completed-match transitions at their original baseline behavior.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -54 +54 @@
-			else nstate = idle;					//Data invalid, stay in s3_d011
+			else nstate = s3_d011;				//Data invalid, stay in s3_d011
```

Regression: PASS

Duration: 62093 ms; Provider calls: 3; tokens in/out: 23828/2120.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
