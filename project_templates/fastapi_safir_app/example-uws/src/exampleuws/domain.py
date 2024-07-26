
"""Domain models for example-uws."""

from __future__ import annotations

from pydantic import BaseModel

__all__ = ["WorkerExampleuwsModel"]


class WorkerExampleuwsModel(BaseModel):
    """Parameter model for backend workers.

    Add fields here for all the parameters passed to backend jobs.
    """
