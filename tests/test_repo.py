"""Test the templatekit.repo.Repo class.

All these tests assume they are being run from the root of a lsst/templates
directory clone.
"""

import os
import pytest
from templatekit.repo import Repo, RepoTemplate


def test_discovery_repo_at_root():
    """Test Repo.discover_repo given the root directory itself.
    """
    repo = Repo.discover_repo(dirname='.')
    assert isinstance(repo, Repo)


def test_discover_repo_in_subdir():
    """Test Repo.discover_repo given a subdirectory of the root.
    """
    repo = Repo.discover_repo(dirname='file_templates')
    assert isinstance(repo, Repo)


def test_discover_repo_invalid():
    """Test Repo.discover_repo an invalid starting directory.
    """
    with pytest.raises(OSError):
        Repo.discover_repo(dirname=os.path.abspath('..'))


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
