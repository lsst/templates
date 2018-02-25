"""Scons builders for regenerating examples given template defaults.

This module provides two builders:

- ``build_file_template`` for single-file templates in the
  ``file_templates`` directory.

- ``build_project_template`` for cookiecutter (project) templates in the
  ``project_templates`` directory.

Again, Scons is only used by the templates repository to regenerate examples
given the template defaults. Users will use cookiecutter directly to generate
new projects from a template.
"""

__all__ = ('file_template_builder', 'cookiecutter_project_builder')

import os

from cookiecutter.main import cookiecutter
from cookiecutter.find import find_template
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


def emit_cookiecutter_sources(target, source, env):
    """Emit the full list of sources for a Cookiecutter project, based on
    the root ``cookiecutter.json`` source.

    This is a **Scons emitter** that is used with the
    `cookiecutter_project_builder` to establish a project template's full
    source list.
    """
    # Get the template directory (i.e., "{{ cookiecutter.project_name }}/")
    template_dir = find_template('.')
    # Get all the template files and add them to the sources
    for (_base_path, _dir_names, _file_names) in os.walk(template_dir):
        source.extend([os.path.join(_base_path, file_name)
                       for file_name in _file_names])
    return target, source


cookiecutter_project_builder = Builder(action=build_project_template,
                                       emitter=emit_cookiecutter_sources)
"""Scons builder for rendering a cookiecutter project template.

The action is `build_project_template` and the emitter is
`emit_cookiecutter_sources`, which sets up the full dependency tree for a
cookiecutter project.
"""
