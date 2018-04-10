"""Test the templatekit.repo.BaseTemplate class.
"""

import os
import pytest
from templatekit.repo import BaseTemplate


def _make_repo_path(repo_rel_path):
    """Make an absolute path to a template directory given a
    repo-relative path.
    """
    return os.path.join(os.path.dirname(__file__), '..', repo_rel_path)


def test_validation():
    """Test basic BaseTemplate instantiation/validation checks.

    Uses the actual templates repository data.
    """
    file_template_exists = BaseTemplate(
        _make_repo_path('file_templates/license_gplv3'))
    assert isinstance(file_template_exists, BaseTemplate)

    project_template_exists = BaseTemplate(
        _make_repo_path('file_templates/license_gplv3'))
    assert isinstance(project_template_exists, BaseTemplate)

    with pytest.raises(OSError):
        BaseTemplate(_make_repo_path('file_templates/not_here'))

    with pytest.raises(OSError):
        BaseTemplate(_make_repo_path('project_templates/not_here'))


@pytest.mark.parametrize('path,expected', [
    (_make_repo_path('file_templates/license_gplv3'), 'license_gplv3'),
    (_make_repo_path('project_templates/example_project'), 'example_project')
])
def test_name(path, expected):
    """Test BaseTemplate.name.
    """
    template = BaseTemplate(path)
    assert expected == template.name


@pytest.mark.parametrize('path', [
    _make_repo_path('file_templates/license_gplv3'),
    _make_repo_path('project_templates/example_project'),
])
def test_cookiecutter_json_path(path):
    """Test BaseTemplate.cookiecutter_json_path.
    """
    template = BaseTemplate(path)
    assert os.path.isfile(template.cookiecutter_json_path)
