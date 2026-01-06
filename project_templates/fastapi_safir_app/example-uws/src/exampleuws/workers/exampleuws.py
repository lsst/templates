"""Worker for example-uws.

This is a standalone file intended to be injected into a stack container as
the arq worker definition. Only this module is allowed to use stack packages.
"""

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
from safir.logging import configure_logging
from structlog.stdlib import BoundLogger

from ..domain import WorkerExampleuwsModel

__all__ = ["WorkerSettings"]


def example_uws(
    params: WorkerExampleuwsModel, info: WorkerJobInfo, logger: BoundLogger
) -> list[WorkerResult]:
    """Perform the work.

    This is a queue worker for the example-uws service. It takes a serialized
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


configure_logging(
    name="exampleuws",
    profile=os.getenv("EXAMPLE_UWS_PROFILE", "development"),
    log_level=os.getenv("EXAMPLE_UWS_LOG_LEVEL", "INFO"),
)

WorkerSettings = build_worker(
    example_uws,
    WorkerConfig(
        arq_mode=ArqMode.production,
        arq_queue_url=os.environ["EXAMPLE_UWS_ARQ_QUEUE_URL"],
        arq_queue_password=os.getenv("EXAMPLE_UWS_ARQ_QUEUE_PASSWORD"),
        grace_period=timedelta(
            seconds=int(os.environ["EXAMPLE_UWS_GRACE_PERIOD"])
        ),
        parameters_class=WorkerExampleuwsModel,
        timeout=timedelta(seconds=int(os.environ["EXAMPLE_UWS_TIMEOUT"])),
    ),
    structlog.get_logger("exampleuws"),
)
"""arq configuration for the example-uws worker."""
