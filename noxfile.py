import nox


@nox.session(name="format")
def format_(session: nox.Session):
    session.install("black", "isort")
    session.run("isort", "EpikCord")
    session.run("black", "EpikCord")


@nox.session
def lint(session: nox.Session):
    session.install("flake8")
    session.run("flake8", "EpikCord")


@nox.session
def mypy(session: nox.Session):
    session.install("mypy")
    session.run("mypy", "EpikCord")
