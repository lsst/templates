"""Scons builders for regenerating examples given template defaults.

This module provides two builders:

- ``build_file_template`` for single-file templates in the
  ``file_templates`` directory.

- ``build_project_template`` for cookiecutter (project) templates in the
  ``project_templates`` directory.

- ``line_format_builder`` for reformatting each line of a content file with
  a Python format expression.

Again, Scons is only used by the templates repository to regenerate examples
given the template defaults. Users will use cookiecutter directly to generate
new projects from a template.
"""

__all__ = ('file_template_builder', 'cookiecutter_project_builder',
           'line_format_builder')

import os

from cookiecutter.main import cookiecutter
from cookiecutter.find import find_template
from SCons.Script import Builder

from .filerender import render_and_write_file_template
from .textutils import reformat_content_lines


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
        The construction environment used for building the target. The
        following construction environment variables are used:

        - ``cookiecutter_context``: a `dict` of key-value pairs, matching
          one or more fields from the ``cookiecutter.json`` file. Use these
          key-value pairs to override one or more of the defaults from the
          project template's ``cookiecutter.json`` file.
    """
    cookiecutter_json_source = str(source[0])

    template_dir = os.path.dirname(cookiecutter_json_source)

    construction_vars = env.Dictionary()
    if 'cookiecutter_context' in construction_vars:
        context_overrides = construction_vars['cookiecutter_context']
    else:
        context_overrides = None

    cookiecutter(
        template_dir,
        output_dir=template_dir,
        overwrite_if_exists=True,
        no_input=True,
        extra_context=context_overrides)


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


def format_content(target, source, env, line_format=None,
                   header=None, footer=None):
    """Scons builder action for rendering a Python comment from a plain
    text file.

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

    try:
        line_format = env['line_format']
    except KeyError:
        line_format = '{}'

    try:
        header = env['header']
    except KeyError:
        header = None

    try:
        footer = env['footer']
    except KeyError:
        footer = None

    with open(source_path) as fh:
        content = fh.read()
    formatted_content = reformat_content_lines(content, line_format,
                                               header=header, footer=footer)
    with open(target_path, 'w') as fh:
        fh.write(formatted_content)


line_format_builder = Builder(action=format_content)
"""Scons builder for reformatting the lines of the source file.

This builder uses the following settings from the constructor environment:

- ``line_format``: Python format statement that each line of the content is
  processed with. The default format argument is the original content line.
  For example, ``# {}`` turns the content into a Python comment.

- ``header``: Text content that can be added above the original content.

- ``footer``: Text content that can be added before the original content.
"""
