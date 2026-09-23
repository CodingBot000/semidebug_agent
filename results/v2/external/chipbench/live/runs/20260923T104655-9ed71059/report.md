# Evidence: chipbench_assignment_Prob003_non-overlapping_sequence_detect

**PATCH_REJECTED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: assignment. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: Two consecutive invalid patches

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | NOT RUN |
| simulation | PASS | NOT RUN | NOT RUN |
| lint | FAIL | NOT RUN | NOT RUN |
| synthesis | PASS | NOT RUN | NOT RUN |

## Attempt 1

The `sf6` state value is too large for the four-bit state register and aliases `s4`.

Rejected: Hunk truncated or invalid

Assign `sf6` a distinct value representable in four bits.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -21,7 +21,7 @@
            sf3=4'd9,
            sf4=4'd10,
            sf5=4'd11,
-           sf6=4'd20;
+           sf6=4'd12;
 
 always @(posedge clk or negedge rst_n)
```

## Attempt 2

`sf6` is assigned a value that cannot fit in four bits, causing it to alias `s4`.

Rejected: Exact baseline context mismatch; fuzzy apply forbidden

Give `sf6` an unused value representable by the four-bit state register. This proposal uses a corrected one-line diff hunk against the original source.

```diff
--- a/rtl/TopModule.sv
+++ b/rtl/TopModule.sv
@@ -24,1 +24,1 @@
-           sf6=4'd20;
+           sf6=4'd12;
```

Duration: 21109 ms; Provider calls: 2; tokens in/out: 14594/730.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
