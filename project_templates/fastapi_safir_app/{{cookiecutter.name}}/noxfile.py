"""nox configuration for {{cookiecutter.name}}."""

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
        "{{cookiecutter.module_name}}.main:app",
        "--reload",
    )


@session(uv_groups=["dev"])
def test(session: nox.Session) -> None:
    """Test the Semaphore server."""
    session.run(
        "pytest",
        "--cov={{cookiecutter.module_name}}",
        "--cov-branch",
        "--cov-report=",
        *session.posargs,
        {%- if cookiecutter.flavor == "UWS" %}
        env={
            "{{ cookiecutter.name | upper | replace('-', '_') }}_ARQ_QUEUE_URL": "redis://localhost/0",
            "{{ cookiecutter.name | upper | replace('-', '_') }}_SERVICE_ACCOUNT": "{{cookiecutter.name}}@example.com",
            "{{ cookiecutter.name | upper | replace('-', '_') }}_STORAGE_URL": "gs://some-bucket",
            "{{ cookiecutter.name | upper | replace('-', '_') }}_WOBBLY_URL": "https://example.com/wobbly",
        },
        {%- endif %}
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
