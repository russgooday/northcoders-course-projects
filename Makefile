VENV := venv
PYTHON := $(VENV)/bin/python3.12
PIP := $(VENV)/bin/pip

all: venv

$(VENV)/bin/activate: requirements.txt
	python3.12 -m venv $(VENV)
	$(PIP) install -r requirements.txt

venv: $(VENV)/bin/activate

clean:
	rm -rf $(VENV)
	rm -rf __pycache__

check-coverage:
	@echo "Checking coverage..."
	pytest --cov=. */tests --cov-fail-under=80

lint:
	@echo "Running linter..."
	pylint */src --fail-under=8

test:
	@echo "Running tests..."
	pytest rare_treasures_api/tests

.PHONY: all lint clean test check-coverage