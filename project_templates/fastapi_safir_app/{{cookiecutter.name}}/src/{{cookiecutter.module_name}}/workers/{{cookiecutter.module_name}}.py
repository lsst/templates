{%- if cookiecutter.flavor == "UWS" -%}
"""Worker for {{ cookiecutter.name }}.

This is a standalone file intended to be injected into a stack container as
the arq worker definition. Only this module is allowed to use stack packages.
"""

from __future__ import annotations

import os
from datetime import timedelta

import structlog
from safir.arq import ArqMode
from safir.arq.uws import (
    WorkerConfig,
    WorkerFatalError,
    WorkerJobInfo,
    WorkerResult,
    build_worker,
)
from structlog.stdlib import BoundLogger

from ..domain import Worker{{ cookiecutter.module_name | capitalize }}Model

__all__ = ["WorkerSettings"]


def {{ cookiecutter.name | replace('-', '_') }}(
    params: Worker{{ cookiecutter.module_name | capitalize }}Model, info: WorkerJobInfo, logger: BoundLogger
) -> list[WorkerResult]:
    """Perform the work.

    This is a queue worker for the {{ cookiecutter.name }} service. It takes a serialized
    request, converts it into a suitable in-memory format, and then dispatches
    it to the scientific code that performs the cutout. The results are stored
    in a GCS bucket, and the details of the output are returned as the result
    of the worker.

    Parameters
    ----------
    params
        Cutout parameters.
    info
        Information about the UWS job we're executing.
    logger
        Logger to use for logging.

    Returns
    -------
    list of WorkerResult
        Results of the job.

    Raises
    ------
    WorkerFatalError
        Raised if the cutout failed for unknown reasons, or due to internal
        errors. This is the normal failure exception, since we usually do not
        know why the backend code failed and make the pessimistic assumption
        that the failure is not transient.
    WorkerUsageError
        Raised if the cutout failed due to deficiencies in the parameters
        submitted by the user that could not be detected by the frontend
        service.
    """
    logger.info("Starting request")
    try:
        # Replace this with a call to the function that does the work.
        result_url = "https://example.com/"
    except Exception as e:
        raise WorkerFatalError(f"{type(e).__name__}: {e!s}") from e
    logger.info("Request successful")

    # Change the result ID to something reasonable, set the MIME type to an
    # appropriate value, and ideally also set the result size if that's
    # available.
    return [
        WorkerResult(
            result_id="main", url=result_url, mime_type="application/fits"
        )
    ]


WorkerSettings = build_worker(
    {{ cookiecutter.name | replace('-', '_') }},
    WorkerConfig(
        arq_mode=ArqMode.production,
        arq_queue_url=os.environ["{{ cookiecutter.name | upper | replace('-', '_') }}_ARQ_QUEUE_URL"],
        arq_queue_password=os.getenv("{{ cookiecutter.name | upper | replace('-', '_') }}_ARQ_QUEUE_PASSWORD"),
        grace_period=timedelta(
            seconds=int(os.environ["{{ cookiecutter.name | upper | replace('-', '_') }}_GRACE_PERIOD"])
        ),
        parameters_class=Worker{{ cookiecutter.module_name | capitalize }}Model,
        timeout=timedelta(seconds=int(os.environ["{{ cookiecutter.name | upper | replace('-', '_') }}_TIMEOUT"])),
    ),
    structlog.get_logger("{{ cookiecutter.module_name }}"),
)
"""arq configuration for the {{ cookiecutter.name }} worker."""
{%- endif %}
