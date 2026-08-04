"""Job parameter dependencies."""

from typing import Annotated

from fastapi import Form

from .models import ExampleuwsParameters

__all__ = [
    "post_params_dependency",
]


async def post_params_dependency(
    *,
    # Add POST parameters here. All of them should be Form() parameters.
    # Use str | None for single-valued attributes and list[str] | None for
    # parameters that can be given more than one time.
    some_param: Annotated[str | None, Form(title="Some parameter")],
) -> ExampleuwsParameters:
    """Parse POST parameters for a new job."""
    # Populate class with the values of all form parameters that were set.
    return ExampleuwsParameters()
