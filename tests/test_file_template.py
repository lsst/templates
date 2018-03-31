"""Test the FileTemplate class.

See also: test_base_template.py for testing the base class.
"""

import os
from templatekit.repo import FileTemplate


def test_source_path():
    template = FileTemplate('file_templates/copyright')
    source_path = template.source_path

    assert os.path.basename(source_path) == 'COPYRIGHT.jinja'
