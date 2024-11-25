"""Job parameter dependencies."""

from typing import Annotated

from fastapi import Depends
from safir.uws import UWSJobParameter, uws_post_params_dependency

__all__ = [
    "post_params_dependency",
]


async def post_params_dependency(
    *,
    # Add POST parameters here. All of them should be Form() parameters.
    # Use str | None for single-valued attributes and str | list[str] | None
    # for parameters that can be given more than one time.
    params: Annotated[
        list[UWSJobParameter], Depends(uws_post_params_dependency)
    ],
) -> list[UWSJobParameter]:
    """Parse POST parameters into job parameters."""
    return [
        p
        for p in params
        if p.parameter_id in set()  # Replace with set of parameter names
    ]
