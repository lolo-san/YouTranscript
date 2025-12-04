.PHONY: help install sync lint run

# --- Environment setup ---

install:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv via curl..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@echo "Installing project dependencies..."
	uv sync

sync:
	@echo "Syncing and upgrading dependencies..."
	uv sync --upgrade

# --- Code quality ---

lint:
	@echo "Linting and formatting code..."
	uvx black src/
	uv run pylint src/ --disable=C,R,W0718

# --- Running the application ---

# Path to cuDNN libraries in the virtual environment (required for whisperx/CUDA)
CUDNN_LIB_PATH := $(shell pwd)/.venv/lib/python3.12/site-packages/nvidia/cudnn/lib

run:
	@echo "Running the application..."
	LD_LIBRARY_PATH=$(CUDNN_LIB_PATH):$$LD_LIBRARY_PATH uv run streamlit run src/youtube-transcript.py

