FROM python:3.12-slim-bookworm@sha256:392307d22300de8b5986851a12d9176dfc0fc073e65bf6523ebd7dcbeb23564e
RUN apt-get update && apt-get install -y --no-install-recommends \
    iverilog=11.0-1.1+b1 verilator=5.006-3 yosys=0.23-6 git make && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml requirements.lock /app/
COPY src /app/src
RUN pip install --no-cache-dir -r requirements.lock && pip install --no-cache-dir --no-deps -e .
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["semidebug", "doctor"]
