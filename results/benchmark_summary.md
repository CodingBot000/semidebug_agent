# Benchmark

Measurement: **scripted-test-not-ai-performance**

Fixed 30/30 cases.

```json
{
  "measurement": "scripted-test-not-ai-performance",
  "total": 30,
  "fixed": 30,
  "repair_success_rate": 1.0,
  "first_attempt_fix_rate": 1.0,
  "regression_integrity_rate": 1.0,
  "patch_attempts": 30,
  "invalid_patch_attempts": 0,
  "invalid_patch_rate": 0.0,
  "average_retry_count": 0,
  "median_repair_time_ms": 360.5,
  "average_llm_calls": 2,
  "input_tokens": 0,
  "output_tokens": 0,
  "estimated_cost": null,
  "failure_breakdown": {},
  "categories": {
    "boundary": {
      "total": 3,
      "fixed": 3
    },
    "combinational": {
      "total": 6,
      "fixed": 6
    },
    "connectivity": {
      "total": 4,
      "fixed": 4
    },
    "fsm": {
      "total": 3,
      "fixed": 3
    },
    "reset": {
      "total": 5,
      "fixed": 5
    },
    "sequential": {
      "total": 5,
      "fixed": 5
    },
    "syntax": {
      "total": 2,
      "fixed": 2
    },
    "width_signedness": {
      "total": 2,
      "fixed": 2
    }
  },
  "retry_distribution": {
    "0": 30
  }
}
```
