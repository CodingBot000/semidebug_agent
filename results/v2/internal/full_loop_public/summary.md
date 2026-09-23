# Benchmark

Measurement: **live-ai-repair**

Fixed 24/24 cases.

```json
{
  "measurement": "live-ai-repair",
  "total": 24,
  "fixed": 24,
  "repair_success_rate": 1.0,
  "first_attempt_fix_rate": 0.875,
  "first_attempt_success_rate": 0.875,
  "final_success_rate": 1.0,
  "retry_rescue_count": 3,
  "semantic_retry_rescue_count": 0,
  "format_retry_rescue_count": 3,
  "regression_rejection_count": 0,
  "retry_reason_counts": {
    "PATCH_PARSE_RETRY": 3
  },
  "average_attempts": 1.125,
  "median_attempts": 1.0,
  "regression_integrity_rate": 1.0,
  "patch_attempts": 27,
  "invalid_patch_attempts": 3,
  "invalid_patch_rate": 0.1111111111111111,
  "average_retry_count": 0.125,
  "median_repair_time_ms": 11531.0,
  "median_latency_ms": 11531.0,
  "average_llm_calls": 1.125,
  "input_tokens": 168855,
  "cached_input_tokens": 43008,
  "models": [
    "gpt-6-sol"
  ],
  "reasoning_efforts": [
    "low"
  ],
  "billing_modes": [
    "chatgpt-subscription"
  ],
  "output_tokens": 8893,
  "estimated_cost": null,
  "failure_breakdown": {},
  "categories": {
    "boundary": {
      "total": 2,
      "fixed": 2
    },
    "combinational": {
      "total": 5,
      "fixed": 5
    },
    "connectivity": {
      "total": 3,
      "fixed": 3
    },
    "fsm": {
      "total": 2,
      "fixed": 2
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
      "total": 1,
      "fixed": 1
    },
    "width_signedness": {
      "total": 1,
      "fixed": 1
    }
  },
  "retry_distribution": {
    "0": 21,
    "1": 3
  }
}
```
