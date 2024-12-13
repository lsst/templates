{%- if cookiecutter.flavor == "UWS" -%}
"""Job parameter dependencies."""

from typing import Annotated

from fastapi import Depends

from .models import {{ cookiecutter.module_name | capitalize }}Parameters

__all__ = [
    "post_params_dependency",
]


async def post_params_dependency(
    *,
    # Add POST parameters here. All of them should be Form() parameters.
    # Use str | None for single-valued attributes and list[str] | None for
    # parameters that can be given more than one time.
) -> {{ cookiecutter.module_name | capitalize }}Parameters:
    # Populate class with the values of all form parameters that were set.
    return {{ cookiecutter.module_name | capitalize }}Parameters()
{%- endif %}
