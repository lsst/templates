"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.

Key functionality is:

1. Create intermediate ``__init__.py`` files for packages with two or more
   namespace layers.

2. Move ``include/root.h`` to its proper subdirectory and name.

3. Remove C++ directories if ``cookiecutter.uses_cpp`` is False.
"""
import os
import shutil
import sys

from templatekit.jinjaext import (
    convert_py_namespace_to_includes_dir,
    convert_py_namespace_to_header_filename)


# These variables are interpolated by cookiecutter before this hook is run
package_name = '{{ cookiecutter.package_name }}'
python_namespace = '{{ cookiecutter.python_module }}'
python_sub_dirs = '{{ cookiecutter.python_sub_dirs }}'
uses_cpp = True if ('{{ cookiecutter.uses_cpp }}' is True
                    or '{{ cookiecutter.uses_cpp }}' == 'True') else False
uses_python = True if ('{{ cookiecutter.uses_python }}' is True
                       or '{{ cookiecutter.uses_python }}' == 'True') else False  # noqa: E501

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

# Move include/root.h to a directory and name based on the namespace.
initial_header_path = os.path.join('include', 'root.h')
if os.path.exists(initial_header_path):
    new_include_dir = os.path.join(
        'include',
        convert_py_namespace_to_includes_dir(python_namespace))
    if not os.path.exists(new_include_dir):
        os.makedirs(new_include_dir)
    new_header_filename = os.path.join(
        new_include_dir,
        convert_py_namespace_to_header_filename(python_namespace))
    if os.path.exists(new_header_filename):
        os.remove(new_header_filename)
    shutil.move(initial_header_path, new_header_filename)
    print('(post-gen hook) Moved root.h to {}'.format(new_header_filename))

# Remove C++ directories if cookiecutter.uses_cpp is False
if not uses_cpp:
    cpp_dirnames = ('lib', 'src', 'include')
    for dirname in cpp_dirnames:
        print('(post-gen hook) Removing {0} directory'.format(dirname))
        shutil.rmtree(dirname, ignore_errors=True)

# Remove Python-specific directories and files if cookiecutter.uses_python
# is False
if not uses_python:
    python_dirnames = (
        'python',
        os.path.join('doc', python_namespace),
        'bin.src',
        'tests',
    )
    python_filenames = {
        '.travis.yml',
        'setup.cfg',
    }
    for dirname in python_dirnames:
        print('(post-gen hook) Removing {0} directory'.format(dirname))
        shutil.rmtree(dirname, ignore_errors=True)
    for filename in python_filenames:
        print('(post-gen hook) Removing {0} file'.format(filename))
        try:
            os.remove(filename)
        except OSError:
            pass

# Remove the package documentation directory if module documentation
# directories are available
if uses_python or uses_cpp:
    package_doc_dirname = os.path.join('doc', package_name)
    print('(post-gen hook) Removing {0} directory'.format(package_doc_dirname))
    shutil.rmtree(package_doc_dirname, ignore_errors=True)
