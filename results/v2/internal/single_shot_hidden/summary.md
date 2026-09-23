# Benchmark

Measurement: **live-ai-repair**

Fixed 2/6 cases.

```json
{
  "measurement": "live-ai-repair",
  "total": 6,
  "fixed": 2,
  "repair_success_rate": 0.3333333333333333,
  "first_attempt_fix_rate": 0.3333333333333333,
  "first_attempt_success_rate": 0.3333333333333333,
  "final_success_rate": 0.3333333333333333,
  "retry_rescue_count": 0,
  "semantic_retry_rescue_count": 0,
  "format_retry_rescue_count": 0,
  "regression_rejection_count": 0,
  "retry_reason_counts": {
    "PATCH_PARSE_RETRY": 4
  },
  "average_attempts": 1,
  "median_attempts": 1.0,
  "regression_integrity_rate": 1.0,
  "patch_attempts": 6,
  "invalid_patch_attempts": 4,
  "invalid_patch_rate": 0.6666666666666666,
  "average_retry_count": 0,
  "median_repair_time_ms": 10867.0,
  "median_latency_ms": 10867.0,
  "average_llm_calls": 1,
  "input_tokens": 38793,
  "cached_input_tokens": 21504,
  "models": [
    "gpt-6-sol"
  ],
  "reasoning_efforts": [
    "low"
  ],
  "billing_modes": [
    "chatgpt-subscription"
  ],
  "output_tokens": 1864,
  "estimated_cost": null,
  "failure_breakdown": {
    "MAX_RETRY": 4
  },
  "categories": {
    "boundary": {
      "total": 1,
      "fixed": 0
    },
    "combinational": {
      "total": 1,
      "fixed": 0
    },
    "connectivity": {
      "total": 1,
      "fixed": 1
    },
    "fsm": {
      "total": 1,
      "fixed": 0
    },
    "syntax": {
      "total": 1,
      "fixed": 0
    },
    "width_signedness": {
      "total": 1,
      "fixed": 1
    }
  },
  "retry_distribution": {
    "0": 6
  }
}
```
