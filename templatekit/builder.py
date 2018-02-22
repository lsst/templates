"""Scons builders.
"""

__all__ = ('file_template_builder',)

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
