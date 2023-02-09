SRC_DIR = EpikCord
TEST_DIR = tests

PY_ENV = venv
PY_BIN = $(PY_ENV)/bin

PIP = $(PY_BIN)/pip

CMD_NOT_FOUND = $(error $(strip $(1)) is required for this rule)
CHECK_CMD = $(if $(shell command -v $(1)),, $(call CMD_NOT_FOUND, $(1)))

SRC = $(shell find $(SRC_DIR) -type f -name "*.py")

REQS = ._deps.lock
FORMAT_CODE = ._format_code.lock

all: $(REQS) $(FORMAT_CODE)

$(PY_ENV):
	$(call CHECK_CMD, python3)
	@ python3 -m venv $@

$(REQS): $(PY_ENV)
	$(call CHECK_CMD, $(PIP))
	@ $(PIP) install -e .
	@ $(PIP) install -r requirements.txt
	@ $(PIP) install -r dev.requirements.txt
	@ touch $@

$(FORMAT_CODE): $(SRC)
	@ $(info $(words $?) files changed since last auto-format)
	@ $(PY_BIN)/black $(SRC_DIR)
	@ touch $@

NOX_RULES := install
NOX_RULES += format
NOX_RULES += lint
NOX_RULES += pyright
NOX_RULES += imports
NOX_RULES += unit
NOX_RULES += e2e
NOX_RULES += cov

define _CREATE_NR
$(2): $(REQS)
	$(PY_BIN)/nox -s $(1)

.PHONY: $(2)
endef

CREATE_NOX_RULE = $(eval $(call _CREATE_NR, $(1), $(addprefix nox_, $(1))))
$(foreach nr, $(NOX_RULES), $(call CREATE_NOX_RULE, $(nr)))

nox_all: $(foreach nr, $(NOX_RULES), $(addprefix nox_, $(nr))))

.PHONY: nox_all

NOX_DIR = .nox
BUILD_DIRS = build *.egg-info
PY_TEST_CACHE = .pytest_cache

clean:
	@ find $(SRC_DIR) -type f -name "*.pyc" -exec rm -rf {} +
	@ $(RM) -r $(NOX_DIR) $(BUILD_DIRS)
	@ $(RM) $(REQS) $(FORMAT_CODE)
	@ $(RM) -r $(PY_TEST_CACHE)

fclean: clean
	@ $(RM) -r $(VENV)

.PHONY: clean fclean

re: fclean all

.PHONY: re
