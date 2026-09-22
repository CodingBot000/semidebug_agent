# Evidence: case_003_counter_boundary

**REPEATED_PATCH** — provider `scripted-test-double`, model `not-an-ai-model`.

Category: boundary. Immutable integrity: True.
Failure reason: Provider repeated a previous diff

| Check | Baseline | Attempt 1 | Attempt 2 |
|---|---|---|---|
| compile | PASS | PASS | NOT RUN |
| simulation | FAIL | FAIL | NOT RUN |
| lint | PASS | PASS | NOT RUN |
| synthesis | PASS | PASS | NOT RUN |

## Attempt 1

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -2,7 +2,7 @@
 always @(posedge clk) begin
     if (rst) count <= 4'd0;
     else if (en) begin
-        if (count == 4'd8) count <= 4'd0;
+        if (count == 4'd7) count <= 4'd0;
         else count <= count + 4'd1;
     end
 end
```

## Attempt 2

Scripted evaluator proposal (known fix)

Known fix supplied by evaluator to test pipeline only

```diff
--- a/rtl/counter.v
+++ b/rtl/counter.v
@@ -2,7 +2,7 @@
 always @(posedge clk) begin
     if (rst) count <= 4'd0;
     else if (en) begin
-        if (count == 4'd8) count <= 4'd0;
+        if (count == 4'd7) count <= 4'd0;
         else count <= count + 4'd1;
     end
 end
```

Duration: 294 ms; Provider calls: 4; tokens in/out: 0/0.
Estimated cost: unknown/unconfigured.

Scripted providers and replay output are not live AI benchmark results.
