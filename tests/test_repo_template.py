"""Test the templatekit.repo.RepoTemplate class.
"""

import os
import pytest
from templatekit.repo import RepoTemplate


def test_validation():
    """Test basic RepoTemplate instantiation/validation checks.

    Uses the actual templates repository data.
    """
    file_template_exists = RepoTemplate('file_templates/license_gplv3')
    assert isinstance(file_template_exists, RepoTemplate)

    project_template_exists = RepoTemplate('project_templates/example_project')
    assert isinstance(project_template_exists, RepoTemplate)

    with pytest.raises(OSError):
        RepoTemplate('file_templates/not_here')

    with pytest.raises(OSError):
        RepoTemplate('project_templates/not_here')


@pytest.mark.parametrize('path,expected', [
    ('file_templates/license_gplv3', 'license_gplv3'),
    ('project_templates/example_project', 'example_project')
])
def test_name(path, expected):
    """Test RepoTemplate.name.
    """
    template = RepoTemplate(path)
    assert expected == template.name


@pytest.mark.parametrize('path', [
    'file_templates/license_gplv3',
    'project_templates/example_project',
])
def test_cookiecutter_json_path(path):
    """Test RepoTemplate.cookiecutter_json_path.
    """
    template = RepoTemplate(path)
    assert os.path.isfile(template.cookiecutter_json_path)
