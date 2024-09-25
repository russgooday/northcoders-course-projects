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
	find . -type f -name '*.pyc' -delete

check-coverage:
	@echo "Checking coverage..."
	pytest --cov=countem --cov=iterators --cov=heapify --cov-fail-under=80

lint:
	@echo "Running linter..."
	pylint */src

test:
	@echo "Running tests..."
	pytest

.PHONY: all lint clean test check-coverage