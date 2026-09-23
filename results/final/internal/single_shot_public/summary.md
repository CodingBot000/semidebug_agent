# Benchmark

Measurement: **live-ai-repair**

Fixed 20/24 cases.

```json
{
  "measurement": "live-ai-repair",
  "total": 24,
  "fixed": 20,
  "repair_success_rate": 0.8333333333333334,
  "first_attempt_fix_rate": 0.8333333333333334,
  "first_attempt_success_rate": 0.8333333333333334,
  "final_success_rate": 0.8333333333333334,
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
  "patch_attempts": 24,
  "invalid_patch_attempts": 4,
  "invalid_patch_rate": 0.16666666666666666,
  "average_retry_count": 0,
  "median_repair_time_ms": 6246.5,
  "median_latency_ms": 6246.5,
  "average_llm_calls": 1,
  "input_tokens": 82902,
  "cached_input_tokens": 82830,
  "models": [
    "gpt-6-sol"
  ],
  "reasoning_efforts": [
    "low"
  ],
  "billing_modes": [
    "openai-api"
  ],
  "output_tokens": 8363,
  "estimated_cost": 0.10034,
  "failure_breakdown": {
    "MAX_RETRY": 4
  },
  "categories": {
    "boundary": {
      "total": 2,
      "fixed": 1
    },
    "combinational": {
      "total": 5,
      "fixed": 3
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
      "fixed": 4
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
    "0": 24
  }
}
```
