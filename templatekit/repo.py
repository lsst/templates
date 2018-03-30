"""Template repository APIs.
"""

__all__ = ('RepoTemplate',)

import os
import logging


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
