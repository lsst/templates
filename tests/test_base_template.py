"""Test the templatekit.repo.BaseTemplate class.
"""

import os
import pytest
from templatekit.repo import BaseTemplate


def test_validation():
    """Test basic BaseTemplate instantiation/validation checks.

    Uses the actual templates repository data.
    """
    file_template_exists = BaseTemplate('file_templates/license_gplv3')
    assert isinstance(file_template_exists, BaseTemplate)

    project_template_exists = BaseTemplate('project_templates/example_project')
    assert isinstance(project_template_exists, BaseTemplate)

    with pytest.raises(OSError):
        BaseTemplate('file_templates/not_here')

    with pytest.raises(OSError):
        BaseTemplate('project_templates/not_here')


@pytest.mark.parametrize('path,expected', [
    ('file_templates/license_gplv3', 'license_gplv3'),
    ('project_templates/example_project', 'example_project')
])
def test_name(path, expected):
    """Test BaseTemplate.name.
    """
    template = BaseTemplate(path)
    assert expected == template.name


@pytest.mark.parametrize('path', [
    'file_templates/license_gplv3',
    'project_templates/example_project',
])
def test_cookiecutter_json_path(path):
    """Test BaseTemplate.cookiecutter_json_path.
    """
    template = BaseTemplate(path)
    assert os.path.isfile(template.cookiecutter_json_path)
