PYTHON		= python3
MAIN		= a_maze_ing.py
CONFIG		= config.txt
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install rich flake8 mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

build:
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build
	cp dist/mazegen-1.0.0-py3-none-any.whl . 2>/dev/null || true
	cp dist/mazegen-1.0.0.tar.gz . 2>/dev/null || true

install-pkg:
	$(PYTHON) -m pip install dist/mazegen-1.0.0-py3-none-any.whl

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache dist/ build/ *.egg-info mazegen.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict build install-pkg
