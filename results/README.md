# Evaluation evidence

The submission uses only the OpenAI API measurements under `results/final/`. Scripted pipeline qualification is labeled separately from model performance, and every selected external failure remains in the denominator.

- `final/internal/`: 30-case feedback-loop and independent one-shot API measurements.
- `final/external/`: selected ChipBench qualification and 12-case API measurement.
- `final/evidence/`: representative success, retry and final-failure traces.
- `final/verification/`: executed source checks and logs.

Older measurements outside `results/final/` are retained locally as development history and are not included in the submission package.
