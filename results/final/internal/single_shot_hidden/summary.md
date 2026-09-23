# Benchmark

Measurement: **live-ai-repair**

Fixed 3/6 cases.

```json
{
  "measurement": "live-ai-repair",
  "total": 6,
  "fixed": 3,
  "repair_success_rate": 0.5,
  "first_attempt_fix_rate": 0.5,
  "first_attempt_success_rate": 0.5,
  "final_success_rate": 0.5,
  "retry_rescue_count": 0,
  "semantic_retry_rescue_count": 0,
  "format_retry_rescue_count": 0,
  "regression_rejection_count": 0,
  "retry_reason_counts": {
    "PATCH_PARSE_RETRY": 3
  },
  "average_attempts": 1,
  "median_attempts": 1.0,
  "regression_integrity_rate": 1.0,
  "patch_attempts": 6,
  "invalid_patch_attempts": 3,
  "invalid_patch_rate": 0.5,
  "average_retry_count": 0,
  "median_repair_time_ms": 6473.5,
  "median_latency_ms": 6473.5,
  "average_llm_calls": 1,
  "input_tokens": 21304,
  "cached_input_tokens": 21286,
  "models": [
    "gpt-6-sol"
  ],
  "reasoning_efforts": [
    "low"
  ],
  "billing_modes": [
    "openai-api"
  ],
  "output_tokens": 2014,
  "estimated_cost": 0.0244332,
  "failure_breakdown": {
    "MAX_RETRY": 3
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
      "fixed": 1
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
