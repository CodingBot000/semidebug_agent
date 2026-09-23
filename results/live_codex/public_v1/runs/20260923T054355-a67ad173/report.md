# Evidence: case_013_arbiter_reset

**FIXED** — provider `live-codex-cli`, model `gpt-6-sol`.

Category: reset. Immutable integrity: True.
Reasoning: low; billing: chatgpt-subscription.
Failure reason: none

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | NOT RUN | PASS |
| simulation | FAIL | NOT RUN | PASS |
| lint | PASS | NOT RUN | PASS |
| synthesis | PASS | NOT RUN | PASS |

## Attempt 1

Reset initializes priority_bit to the opposite value from the reference model.

Rejected: Hunk truncated or invalid

Initialize the arbitration priority to requester 0 on reset, matching the reference behavior.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -12,7 +12,7 @@
 always @(posedge clk) begin
-    if (rst) priority_bit <= 1'b1;
+    if (rst) priority_bit <= 1'b0;
     else if (grant[0]) priority_bit <= 1'b1;
     else if (grant[1]) priority_bit <= 1'b0;
 end
```

## Attempt 2

Reset initializes the arbitration priority opposite to the reference model.

Set the reset priority to 0 to match the reference model. This corrects the prior proposal's malformed hunk without claiming it passed validation.

```diff
--- a/rtl/arbiter.v
+++ b/rtl/arbiter.v
@@ -12,5 +12,5 @@
 always @(posedge clk) begin
-    if (rst) priority_bit <= 1'b1;
+    if (rst) priority_bit <= 1'b0;
     else if (grant[0]) priority_bit <= 1'b1;
     else if (grant[1]) priority_bit <= 1'b0;
 end
```

Regression: PASS

Duration: 27755 ms; Provider calls: 2; tokens in/out: 12954/741.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
