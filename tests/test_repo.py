"""Test the templatekit.repo.Repo class.
"""

import os
from templatekit.repo import Repo, RepoTemplate


def test_file_templates_dirname():
    """Test the file_templates_dirname property.
    """
    repo = Repo('.')
    assert os.path.isdir(repo.file_templates_dirname)


def test_project_templates_dirname():
    """Test the project_templates_dirname property.
    """
    repo = Repo('.')
    assert os.path.isdir(repo.project_templates_dirname)


def test_iter_file_templates():
    """Test the iter_file_templates() method.
    """
    repo = Repo('.')
    file_templates = list(repo.iter_file_templates())
    assert len(file_templates) > 0
    for file_template in file_templates:
        assert isinstance(file_template, RepoTemplate)


def test_iter_project_templates():
    """Test the iter_project_templates() method.
    """
    repo = Repo('.')
    project_templates = list(repo.iter_project_templates())
    assert len(project_templates) > 0
    for project_template in project_templates:
        assert isinstance(project_template, RepoTemplate)
