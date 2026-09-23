# Final internal benchmark

This directory contains the final 30-case internal evaluation corpus. Each visible target test uses seed 7 and a short sequence. Each evaluator-only regression uses a different source file, seeds 17 and 103, a longer sequence and additional directed vectors. `src/semidebug/context/selector.py` sends only mutable RTL and visible target source to the provider. Hidden test source and detailed hidden failure output stay in the local evaluator artifacts.

The directory name is retained so saved run references remain valid; it does not identify a separate submitted product version.

`results/final/dataset_audit.json` records real EDA qualification: all six gold designs passed target and hidden regression, and all 30 buggy variants reproduced a failure. `results/final/pipeline_validation_summary.json` is a known-fix scripted pipeline check, not AI repair performance.
