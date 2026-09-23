.PHONY: bootstrap doctor test test-integration e2e test-all lint demo benchmark package
bootstrap:
	./scripts/bootstrap.sh
doctor:
	./scripts/doctor.sh
test:
	uv run pytest tests/unit -q
test-integration:
	./scripts/docker_run.sh pytest -p no:cacheprovider tests/integration -q
e2e:
	./scripts/docker_run.sh pytest -p no:cacheprovider tests/e2e -q
test-all:
	./scripts/docker_run.sh pytest -p no:cacheprovider -q
lint:
	uv run ruff check src tests evaluator scripts
	uv run ruff format --check src tests evaluator scripts
demo:
	./scripts/run_demo.sh --scripted
benchmark:
	./scripts/run_benchmark.sh
package:
	uv run python scripts/package_v2_submission.py
