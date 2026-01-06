{%- if cookiecutter.flavor == "UWS" -%}
"""Domain models for {{ cookiecutter.name }}."""

from pydantic import BaseModel

__all__ = ["Worker{{ cookiecutter.module_name | capitalize }}Model"]


class Worker{{ cookiecutter.module_name | capitalize }}Model(BaseModel):
    """Parameter model for backend workers.

    Add fields here for all the parameters passed to backend jobs.
    """
{%- endif %}
