"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.
"""
import os
import shutil
import sys


# This variable is interpolated by cookiecutter before this hook is run
python_sub_dirs = '{{ cookiecutter.python_sub_dirs }}'
uses_cpp = True if ('{{ cookiecutter.uses_cpp }}' is True
                    or '{{ cookiecutter.uses_cpp }}' == 'True') else False

python_sub_dir_parts = python_sub_dirs.split('/')

# Path of the python/lsst/__init__.py file. This file is the __init__.py that
# we might neeed to copy to other intermediate namespace directories.
root_init_path = os.path.join('python', python_sub_dir_parts[0], '__init__.py')
if not os.path.isfile(root_init_path):
    print('(post-gen hook) Could not find root __init__.py at {}'
          .format(root_init_path))
    sys.exit(1)

# Create __init__.py files for intermediate sub-package directories.
# Only interpolate the sub-package directories if there are two or more
# namespace layers. For example, `lsst.example` doesn't need an extra
# __init__.py; the cookiecutter template will already create
# python/lsst/example/__init__.py
# But for `lsst.example.subpackage`, we need to copy
# python/lsst/__init__.py to python/lsst/example/__init__.py
if len(python_sub_dir_parts) > 2:
    for i in range(1, len(python_sub_dir_parts) - 1):
        package_dirname = os.path.join('python', *python_sub_dir_parts[0:i+1])
        if not os.path.exists(package_dirname):
            os.makedirs(package_dirname)
        init_path = os.path.join(package_dirname, '__init__.py')
        shutil.copy(root_init_path, init_path)
        print('(post-gen hook) Copied {0} to {1}'
              .format(root_init_path, init_path))


# Remove C++ directories if cookiecutter.uses_cpp is False
if not uses_cpp:
    cpp_dirnames = ('lib', 'src', 'include')
    for dirname in cpp_dirnames:
        print('(post-gen hook) Removing {0} directory'.format(dirname))
        shutil.rmtree(dirname, ignore_errors=True)
