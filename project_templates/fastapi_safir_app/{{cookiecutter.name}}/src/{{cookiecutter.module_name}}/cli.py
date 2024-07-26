{%- if cookiecutter.uws_service == "True" %}
"""Administrative command-line interface."""

from __future__ import annotations

import click
import structlog
from safir.asyncio import run_with_asyncio
from safir.click import display_help

from .config import uws

__all__ = [
    "help",
    "init",
    "main",
]


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(message="%(version)s")
def main() -> None:
    """Administrative command-line interface for {{ cookiecutter.name }}."""


@main.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx: click.Context, topic: str | None) -> None:
    """Show help for any command."""
    display_help(main, ctx, topic)


@main.command()
@click.option(
    "--reset", is_flag=True, help="Delete all existing database data."
)
@run_with_asyncio
async def init(*, reset: bool) -> None:
    """Initialize the database storage."""
    logger = structlog.get_logger("{{ cookiecutter.module_name }}")
    await uws.initialize_uws_database(logger, reset=reset)
{%- endif %}
