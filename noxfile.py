# Nox configuration for repolyze
import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True

pyproject = nox.project.load_toml("pyproject.toml")

test_ci_deps = nox.project.dependency_groups(pyproject, "test-ci")
test_deps = nox.project.dependency_groups(pyproject, "test")
lint_deps = nox.project.dependency_groups(pyproject, "lint")
docs_deps = nox.project.dependency_groups(pyproject, "docs")

def install_repolyze(session):
    session.install(*test_ci_deps)
    session.install(*test_deps)
    session.install("-e", ".")


def base_test(session):
    install_repolyze(session)
    session.run("pytest", "tests", "-n", "auto")


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"])
def test_with_py_versions(session):
    """Run tests on multiple Python versions."""
    base_test(session)


@nox.session()
def lint(session):
	"""Run ruff linter."""
	session.install(*lint_deps)
	session.run("ruff", "check", ".")


@nox.session()
def docs(session):
    """Build the documentation."""
    session.install(*docs_deps)
    session.run(
        "sphinx-build",
        "-W",
        "-d",
        "docs/build/.doctrees",
        "-b",
        "html",
        "docs/source",
        "docs/build/html"
    )
