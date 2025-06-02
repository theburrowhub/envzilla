PYTHON=python3.11
VENV=.venv
UV=$(VENV)/bin/uv
PIP=$(VENV)/bin/pip

.PHONY: init install test run clean

init:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install uv

install: init
	$(UV) pip install -e .[dev]

test:
	$(UV) pip install pytest
	$(VENV)/bin/pytest -q

run:
	$(VENV)/bin/envzilla

clean:
	rm -rf $(VENV) dist *.egg-info
	echo "Cleaned build and virtual environment"
