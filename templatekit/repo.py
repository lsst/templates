"""Template repository APIs.
"""

__all__ = ('Repo', 'RepoTemplate')

import os
import logging


class Repo(object):
    """Template repository.

    Parameters
    ----------
    root : `str`
        Path to the root directory of the template repository. Use ``'.'``
        as the current working directory.
    """

    def __init__(self, root):
        super().__init__()
        self._log = logging.getLogger(__name__)
        self.root = root

    @property
    def file_templates_dirname(self):
        """Path of the ``file_templates`` directory in the repository (`str`).
        """
        return os.path.join(self.root, 'file_templates')

    @property
    def project_templates_dirname(self):
        """Path of the ``project_templates`` directory in the repository
        (`str`).
        """
        return os.path.join(self.root, 'project_templates')

    def iter_file_templates(self):
        """Iterate over file templates in the repository.

        These templates are in the ``file_templates`` directory of the
        repository and either template a single file, or a snippet of one.

        Yields
        ------
        template : `RepoTemplate`
            Template object.
        """
        dir_items = self._list_directory_items(self.file_templates_dirname)
        for template_dir in dir_items:
            try:
                template = RepoTemplate(template_dir)
            except (OSError, ValueError) as err:
                # Not a template directory
                message = ('Found file_template directory {0!r} but it is not '
                           'a recognizable template. {1!s}')
                logging.warning(message.format(template_dir, err))
                continue
            yield template

    def iter_project_templates(self):
        """Iterate over project templates in the repository.

        These templates are in the ``project_templates`` directory of the
        repository and template full project directory trees and contents.

        Yields
        ------
        template : `RepoTemplate`
            Template object.
        """
        dir_items = self._list_directory_items(self.project_templates_dirname)
        for template_dir in dir_items:
            try:
                template = RepoTemplate(template_dir)
            except (OSError, ValueError) as err:
                # Not a template directory
                message = ('Found project_template directory {0!r} but it is '
                           'not a recognizable template. {1!s}')
                logging.warning(message.format(template_dir, err))
                continue
            yield template

    def _list_directory_items(self, dirname):
        fs_items = os.listdir(dirname)
        fs_items.sort()
        fs_items = [os.path.join(dirname, item) for item in fs_items]
        return [fs_item for fs_item in fs_items if os.path.isdir(fs_item)]


class RepoTemplate(object):
    """Template (file or project) in the templates repo.

    Parameters
    ----------
    path : `str`
        Path of the template's directory.

    Raises
    ------
    OSError
        Raised if ``path`` is not a directory.
    ValueError
        Raised if ``path`` is a directory that does not contain a recognizable
        template.
    """

    def __init__(self, path):
        super().__init__()
        self._log = logging.getLogger(__name__)
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            message = 'File template directory {} not found.'.format(self.path)
            raise OSError(message)

        self._validate_template_dir()

    def _validate_template_dir(self):
        """Run a quick set of checks that this is in fact a template
        repository, with a cookiecutter.json directory, etc.
        """
        if not os.path.isfile(self.cookiecutter_json_path):
            message = 'cookiecutter.json not found in {}'.format(self.path)
            raise ValueError(message)

    def __str__(self):
        return 'RepoTemplate({0!r})'.format(self.name)

    def __repr__(self):
        return 'RepoTemplate({0!r})'.format(self.path)

    @property
    def name(self):
        """Name of the template (`str`).
        """
        return os.path.split(self.path)[-1]

    @property
    def cookiecutter_json_path(self):
        """Path of the cookiecutter.json file (`str`).
        """
        return os.path.join(self.path, 'cookiecutter.json')
