import nox


@nox.session(name="install")
def installation(session: nox.Session):
    session.install("-r", "requirements.txt")
    session.install(".")


@nox.session(name="format")
def format_(session: nox.Session):
    session.install("black", "isort")
    session.run("isort", "EpikCord")
    session.run("black", "EpikCord")


@nox.session
def lint(session: nox.Session):
    session.install("ruff")
    session.run("ruff", "EpikCord")


@nox.session
def pyright(session: nox.Session):
    session.install("pyright")
    session.install("orjson", "types-orjson")
    session.install("-r", "requirements.txt")
    session.run("pyright", "EpikCord")


@nox.session(name="imports")
def check_circular_imports(session: nox.Session):
    session.install("pytest")
    session.install("-r", "requirements.txt")
    session.install(".")
    session.run("pytest", "tests/test_circular_imports.py")


@nox.session(name="unit")
def unit(session: nox.Session):
    session.install("pytest")
    session.install("-r", "requirements.txt")
    session.install(".")
    session.run("pytest", "tests/unit")


@nox.session(name="e2e")
def end_to_end(session: nox.Session):
    session.install("pytest")
    session.install("-r", "requirements.txt")
    session.install(".")
    session.run("pytest", "tests/e2e")


@nox.session(name="cov")
def coverage_report(session: nox.Session):
    session.install("pytest", "pytest-cov", "coverage")
    session.install("-r", "requirements.txt")
    session.install(".")
    session.run("pytest", "--cov=EpikCord", "tests")
    session.run("coverage", "xml")
