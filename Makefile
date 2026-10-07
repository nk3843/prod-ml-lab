.PHONY: setup data lab
setup:
	uv sync
data:
	uv run python scripts/download_data.py
lab:
	uv run jupyter lab notebooks/
