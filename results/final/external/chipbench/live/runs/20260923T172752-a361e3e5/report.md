# Evidence: chipbench_arithmetic_Prob002_extraneous_items_sequence_detect

**FIXED** — provider `live-openai-api`, model `gpt-6-sol`.

Category: arithmetic. Immutable integrity: True.
Reasoning: low; billing: openai-api.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | PASS | PASS |
| simulation | PASS | PASS | PASS |
| lint | PASS | PASS | PASS |
| synthesis | PASS | PASS | PASS |

## Attempt 1

The shift direction is reversed, and both registered comparisons examine the window from before the current input is shifted in.

Shift the new input into bit 0 and compare the window that will be stored at the current edge. The existing asynchronously reset match registers then report detection for that edge's nine-bit window.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -14,7 +14,7 @@
 			begin 
 				match_f <= 1'b0;
 			end
-		else if (a_tem[8:6] == 3'b011)
+		else if (a_tem[7:5] == 3'b011)
 			begin
 				match_f <= 1'b1;
 			end
@@ -28,7 +28,7 @@
 			begin 
 				match_b <= 1'b0;
 			end
-		else if (a_tem[2:0] == 3'b110)
+		else if ({a_tem[1:0], a} == 3'b110)
 			begin
 				match_b <= 1'b1;
 			end
@@ -44,7 +44,7 @@
 			end
 		else 
 			begin
-				a_tem <= {a, a_tem[7:0]};
+				a_tem <= {a_tem[7:0], a};
 			end
 			
 	assign match = match_b && match_f;
```

Regression: FAIL

## Attempt 2

The shift register loads new bits at the wrong end, while the existing registered comparisons may already provide the expected sequential timing.

In rtl/TopModule.sv:47, shift the sampled input into bit 0 so the oldest stored bit occupies bit 8. Preserve the existing registered comparison timing at lines 17 and 31.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -44,7 +44,7 @@
 			end
 		else 
 			begin
-				a_tem <= {a, a_tem[7:0]};
+				a_tem <= {a_tem[7:0], a};
 			end
 			
 	assign match = match_b && match_f;
```

Regression: PASS

Duration: 20087 ms; Provider calls: 2; tokens in/out: 11067/1209.
Estimated cost: 0.030292799999999998.

Scripted providers and replay output are not live AI benchmark results.
