"""Tests for the templatekit.filerender module.
"""

import os
from templatekit.filerender import render_file_template


def _make_repo_path(repo_rel_path):
    """Make an absolute path to a template directory given a
    repo-relative path.
    """
    return os.path.join(os.path.dirname(__file__), '..', repo_rel_path)


def test_render_file_template():
    """Test render_file_template().

    This test uses file_templates/stack_license_preamble_txt/template.txt.jinja
    as an example project.
    """
    template_path = _make_repo_path(
        'file_templates/stack_license_preamble_txt/template.txt.jinja')

    expected_content_path = _make_repo_path(
        'file_templates/stack_license_preamble_txt/example.txt')
    with open(expected_content_path) as fh:
        expected_content = fh.read()

    content = render_file_template(template_path, use_defaults=True)
    assert expected_content == content
