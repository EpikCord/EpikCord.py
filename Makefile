SRC_DIR = EpikCord
TEST_DIR = tests

PY_ENV = venv
PY_BIN = $(PY_ENV)/bin

all: reqs


$(PY_BIN)/%:
	python3 -m venv $(PY_ENV)
	chmod +x $(PY_BIN)/activate
	./$(PY_BIN)/activate

reqs: $(PY_BIN)/pip
	$(PY_BIN)/pip3 install -e .


$(PY_BIN)/nox: $(PY_BIN)/pip
	$(PY_BIN)/pip3 install nox


lint: $(PY_BIN)/nox
	$(PY_BIN)/nox -s lint mypy


pretty: $(PY_BIN)/nox
	$(PY_BIN)/nox -s format


dist: reqs
	python setup.py build sdist


clean:
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache

	rm -rf dist
	rm -rf build

	rm -rf *.egg-info


fclean: clean
	rm -rf $(PY_ENV)
	rm -rf .nox


.PHONY: py_test clean fclean reqs lint pretty

