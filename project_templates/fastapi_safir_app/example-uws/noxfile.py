"""nox configuration for example-uws."""

import nox
from nox_uv import session

# Default sessions.
nox.options.sessions = ["lint", "typing", "test"]

# Other nox defaults.
nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True


@session(name="coverage-report", uv_groups=["dev"])
def coverage_report(session: nox.Session) -> None:
    """Generate a code coverage report from the test suite."""
    session.run("coverage", "report", *session.posargs)


@session(uv_only_groups=["lint"], uv_no_install_project=True)
def lint(session: nox.Session) -> None:
    """Run pre-commit hooks."""
    session.run("prek", "run", "--all-files", *session.posargs)


@session
def run(session: nox.Session) -> None:
    """Run a local development server."""
    session.run(
        "uvicorn",
        "exampleuws.main:app",
        "--reload",
    )


@session(uv_groups=["dev"])
def test(session: nox.Session) -> None:
    """Test the Semaphore server."""
    session.run(
        "pytest",
        "--cov=exampleuws",
        "--cov-branch",
        "--cov-report=",
        *session.posargs,
        env={
            "EXAMPLE_UWS_ARQ_QUEUE_URL": "redis://localhost/0",
            "EXAMPLE_UWS_SERVICE_ACCOUNT": "example-uws@example.com",
            "EXAMPLE_UWS_STORAGE_URL": "gs://some-bucket",
            "EXAMPLE_UWS_WOBBLY_URL": "https://example.com/wobbly",
        },
    )


@session(uv_groups=["dev", "typing"])
def typing(session: nox.Session) -> None:
    """Run mypy."""
    session.run(
        "mypy",
        *session.posargs,
        "noxfile.py",
        "src",
        "tests",
    )
