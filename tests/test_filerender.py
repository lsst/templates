"""Tests for the templatekit.filerender module.
"""

import os
from templatekit.filerender import render_file_template


def test_render_file_template():
    """Test render_file_template().

    This test uses file_templates/stack_license_py/template.py.jinja as an
    example project.
    """
    template_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '../file_templates/stack_license_py/template.py.jinja'))

    expected_content_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '../file_templates/stack_license_py/example.py'))
    with open(expected_content_path) as fh:
        expected_content = fh.read()

    content = render_file_template(template_path)
    assert expected_content == content
