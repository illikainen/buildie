PYTHON ?= python3
PYTHON_FILES := $(shell find . -type f -name '*.py' -o -name 'buildie')

all:

fix:
	$(PYTHON) -m black --line-length 79 $(PYTHON_FILES)
	$(PYTHON) -m isort $(PYTHON_FILES)

test:
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m black --check --line-length 79 --quiet $(PYTHON_FILES)
	$(PYTHON) -m isort --check-only $(PYTHON_FILES)
	$(PYTHON) -m pycodestyle --ignore E203 $(PYTHON_FILES)
	$(PYTHON) -m pylint $(PYTHON_FILES)

.PHONY: all test
