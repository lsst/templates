"""Subcommand for making something from a template.
"""

__all__ = ('make',)

import os
import click
from cookiecutter.main import cookiecutter

from ..filerender import render_file_template
from ..repo import FileTemplate


@click.command()
@click.argument('name', metavar='<template name>', required=True)
@click.option('-o', '--output', 'output_path',
              type=click.Path(resolve_path=True),
              help="Filepath to render a file template into, or directory "
                   "to create a project in.")
@click.pass_obj
def make(state, name, output_path):
    """Make a file or project from a template called <template name>.

    --output is optional. When provided for a file template, templatekit
    renders the output into that file path. For a project template, this is
    the directory the project's directory is created in (default is the
    current working directory).
    """
    repo = state['repo']
    try:
        template = repo[name]
    except KeyError:
        message = ("Template {0!r} isn't known. Run `templatekit list` to "
                   "list available templates.".format(name))
        raise click.UsageError(message)

    if isinstance(template, FileTemplate):
        _handle_file_template(template, output_path)
    else:
        _handle_project_template(template, output_path)


def _handle_file_template(template, output_path):
    """Handle rendering and output for a file template.
    """
    rendered_text = render_file_template(template.source_path,
                                         use_defaults=False)

    if output_path is None:
        # Just output to the console
        print()
        print(rendered_text)

    else:
        # Write to a file
        base_dir = os.path.dirname(output_path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        with open(output_path, 'w') as fh:
            fh.write(rendered_text)


def _handle_project_template(template, output_path):
    """Handle rendering and output for a project template.
    """
    template_dir = template.path

    if output_path is None:
        # If user didn't provide an output directory, use the current
        # working directory
        output_path = os.getcwd()

    cookiecutter(
        template_dir,
        output_dir=output_path,
        overwrite_if_exists=False,
        no_input=False,
        extra_context=None)
