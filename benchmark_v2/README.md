# V2 internal benchmark

This directory is a deterministic derivative of the frozen V1 `benchmark/` cases. Rebuild it in a fresh checkout with `uv run python evaluator/build_v2_dataset.py`; the generator refuses to overwrite an existing output directory.

The buggy RTL is unchanged. Each visible target test uses seed 7 and a short sequence. Each evaluator-only regression uses a different source file, seeds 17 and 103, a longer sequence and additional directed vectors. `src/semidebug/context/selector.py` sends only mutable RTL and visible target source to the provider. Hidden test source and detailed hidden failure output stay in the local evaluator artifacts.

`results/v2/dataset_audit.json` records real EDA qualification: all six gold designs passed target and hidden regression, and all 30 buggy variants reproduced a failure. `results/v2/pipeline_validation_summary.json` is a known-fix scripted pipeline check, not AI repair performance. V1 files and results remain separate.
