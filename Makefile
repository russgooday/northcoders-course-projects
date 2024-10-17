VENV := venv
PYTHON := $(VENV)/bin/python3.13
PIP := $(VENV)/bin/pip

all: venv

$(VENV)/bin/activate: requirements.txt
	python3.13 -m venv $(VENV)
	$(PIP) install -r requirements.txt

venv: $(VENV)/bin/activate

clean:
	rm -rf $(VENV)
	rm -rf __pycache__

check-coverage:
	@echo "Checking coverage..."
	pytest --cov=countem --cov=iterators --cov=heapify --cov-fail-under=80

lint:
	@echo "Running linter..."
	pylint */src

test:
	@echo "Running tests..."
	pytest rare_treasures_api/tests

.PHONY: all lint clean test check-coverage