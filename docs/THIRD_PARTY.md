# Third-party software

The project and original RTL/testbenches use MIT. External EDA tools are installed, not bundled into the submission ZIP.

| Component | License | Primary source |
|---|---|---|
| Icarus Verilog | GPL-2.0-or-later; some runtime components LGPL-2.1-or-later | https://github.com/steveicarus/iverilog/blob/master/COPYING |
| Verilator | LGPL-3.0-only OR Artistic-2.0 | https://verilator.org/guide/latest/copyright.html |
| Yosys | ISC | https://github.com/YosysHQ/yosys/blob/main/COPYING |
| Python | PSF | https://docs.python.org/3/license.html |
| Pydantic / pydantic-core | MIT | https://github.com/pydantic/pydantic/blob/main/LICENSE |
| HTTPX / HTTP Core | BSD-3-Clause | https://github.com/encode/httpx/blob/master/LICENSE.md |
| python-dotenv | BSD-3-Clause | https://github.com/theskumar/python-dotenv/blob/main/LICENSE |
| pytest | MIT | https://github.com/pytest-dev/pytest/blob/main/LICENSE |
| Ruff / uv | MIT OR Apache-2.0 | https://github.com/astral-sh/ruff |
| ChipBench Verilog Debugging | MIT | https://github.com/zhongkaiyu/ChipBench/blob/b4ba3a06759804ec88c26c3cf15b28b9a90b3443/LICENSE |
| HWE-bench (feasibility research only) | Apache-2.0 harness; subject assets may differ | https://github.com/pku-liang/hwe-bench/blob/10c78a87e1f92695d78d15b1464a6107dcac8837/LICENSE |

Resolved dependency versions are in uv.lock and requirements.lock. Distribution EDA versions and the build image ID are recorded in results/environment.json and results/docker_environment.json. Transitive dependency license inventory is generated from installed package metadata during final packaging.

The V2 ChipBench selection pins upstream commit `b4ba3a06759804ec88c26c3cf15b28b9a90b3443` and SHA256 for 12 prompt/reference/test triplets in `external/chipbench/selection_manifest.json`. The selected upstream files are downloaded for local evaluation only. The submission ZIP includes the selection manifest and importer, not ChipBench prompts, tests or reference solutions. HWE-bench data and subject repository files have not been downloaded or redistributed.
