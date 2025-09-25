{%- if cookiecutter.flavor == "UWS" -%}
"""Worker for UWS database updates."""

from __future__ import annotations

import structlog
from safir.logging import configure_logging

from ..config import config, uws

__all__ = ["WorkerSettings"]


configure_logging(
    name="{{ cookiecutter.module_name }}",
    profile=config.log_profile,
    log_level=config.log_level,
)

WorkerSettings = uws.build_worker(structlog.get_logger("{{ cookiecutter.module_name }}"))
"""arq configuration for the UWS database worker."""
{%- endif %}
