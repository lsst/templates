"""Test the templatekit.repo.Repo class.
"""

import contextlib
import os
import pytest
from templatekit.repo import Repo, FileTemplate, ProjectTemplate


REPOPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
"""Directory path of the root of the templates repository.
"""


@contextlib.contextmanager
def work_dir(workdirname):
    """Temporarily change the current working directory (as a context manager).
    """
    prev_cwd = os.getcwd()
    os.chdir(workdirname)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def test_discovery_repo_at_root():
    """Test Repo.discover_repo given the root directory itself.
    """
    with work_dir(REPOPATH):
        repo = Repo.discover_repo(dirname='.')
        assert isinstance(repo, Repo)


def test_discover_repo_in_subdir():
    """Test Repo.discover_repo given a subdirectory of the root.
    """
    with work_dir(REPOPATH):
        repo = Repo.discover_repo(dirname='file_templates')
        assert isinstance(repo, Repo)


def test_discover_repo_invalid():
    """Test Repo.discover_repo an invalid starting directory.
    """
    with work_dir(REPOPATH):
        with pytest.raises(OSError):
            Repo.discover_repo(dirname=os.path.abspath('..'))


def test_file_templates_dirname():
    """Test the file_templates_dirname property.
    """
    with work_dir(REPOPATH):
        repo = Repo('.')
        assert os.path.isdir(repo.file_templates_dirname)


def test_project_templates_dirname():
    """Test the project_templates_dirname property.
    """
    with work_dir(REPOPATH):
        repo = Repo('.')
        assert os.path.isdir(repo.project_templates_dirname)


def test_iter_file_templates():
    """Test the iter_file_templates() method.
    """
    with work_dir(REPOPATH):
        repo = Repo('.')
        file_templates = list(repo.iter_file_templates())
        assert len(file_templates) > 0
        for file_template in file_templates:
            assert isinstance(file_template, FileTemplate)


def test_iter_project_templates():
    """Test the iter_project_templates() method.
    """
    with work_dir(REPOPATH):
        repo = Repo('.')
        project_templates = list(repo.iter_project_templates())
        assert len(project_templates) > 0
        for project_template in project_templates:
            assert isinstance(project_template, ProjectTemplate)


def test_getitem():
    """Test key access for templates.
    """
    with work_dir(REPOPATH):
        repo = Repo('.')
        with pytest.raises(KeyError):
            repo['whatwhat']

        copyright_template = repo['copyright']
        assert isinstance(copyright_template, FileTemplate)
        assert copyright_template.name == 'copyright'

        example_project_template = repo['example_project']
        assert isinstance(example_project_template, ProjectTemplate)
        assert example_project_template.name == 'example_project'


def test_contains():
    """Test contains delegated through __iter__.
    """
    with work_dir(REPOPATH):
        repo = Repo('.')

        assert 'copyright' in repo
        assert 'example_project' in repo
        assert 'whatwhat' not in repo
