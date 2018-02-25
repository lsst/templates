"""Scons builders.
"""

__all__ = ('file_template_builder', 'cookiecutter_project_builder')

import os

from cookiecutter.main import cookiecutter
from SCons.Script import Builder

from .filerender import render_and_write_file_template


def build_file_template(target, source, env):
    """Scons builder action for rendering a single-file template.

    Parameters
    ----------
    target : `list` of `Scons.Script.Node`
        A list of Node objects corresponding to examples to be built.
    source : `list` of `Scons.Script.Node`
        A list of Node objects corresponding to file templates.
    env : `Scons.Script.Environment`
        The construction environment used for building the target.
    """
    target_path = str(target[0])
    source_path = str(source[0])

    render_and_write_file_template(source_path, target_path)


file_template_builder = Builder(action=build_file_template,
                                suffix='',
                                src_suffix='.jinja')
"""Scons builder for rendering a single-file template examples.
"""


def build_project_template(target, source, env):
    """Scons builder action for rendering a cookiecutter project template.

    Parameters
    ----------
    target : `list` of `Scons.Script.Node`
        A list of Node objects corresponding to examples to be built.
    source : `list` of `Scons.Script.Node`
        A list of Node objects containing only the ``cookiecutter.json`` file
        node.
    env : `Scons.Script.Environment`
        The construction environment used for building the target.
    """
    # target_path = str(target[0])
    cookiecutter_json_source = str(source[0])

    template_dir = os.path.dirname(cookiecutter_json_source)

    cookiecutter(
        template_dir,
        output_dir=template_dir,
        overwrite_if_exists=True,
        no_input=True)


cookiecutter_project_builder = Builder(action=build_project_template)
"""Scons builder for rendering a cookiecutter project template.
"""
