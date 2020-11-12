"""Post project creation hook for cookiecutter.

This script runs from the root directory of the created project itself. In
addition, cookiecutter interpolates Jinja2 templates to insert any necessary
variables.

Key functionality is:

1. Move ``include/root.h`` to its proper subdirectory and name.

2. Remove C++ directories if ``cookiecutter.uses_cpp`` is False.

3. Remove Python-specific directories if ``cookiecutter.uses_python`` is False.

4. If The package is not part of a Stack, re-arrange the package's
   documentation so that it can be deployed standalone.
"""
import os
import shutil

from templatekit.jinjaext import (
    convert_py_namespace_to_includes_dir,
    convert_py_namespace_to_header_filename)


# These variables are interpolated by cookiecutter before this hook is run
package_name = '{{ cookiecutter.package_name }}'
stack_name = '{{ cookiecutter.stack_name }}'
python_namespace = '{{ cookiecutter.python_module }}'
python_sub_dirs = '{{ cookiecutter.python_sub_dirs }}'
uses_cpp = True if ('{{ cookiecutter.uses_cpp }}' is True
                    or '{{ cookiecutter.uses_cpp }}' == 'True') else False
uses_python = True if ('{{ cookiecutter.uses_python }}' is True
                       or '{{ cookiecutter.uses_python }}' == 'True') else False  # noqa: E501

python_sub_dir_parts = python_sub_dirs.split('/')

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
    print('(post-gen hook) Moved root.h to {new_header_filename}')

if not uses_cpp:
    # Remove C++ directories if cookiecutter.uses_cpp is False
    cpp_dirnames = ('lib', 'src', 'include')
    for dirname in cpp_dirnames:
        print(f'(post-gen hook) Removing {dirname} directory')
        shutil.rmtree(dirname, ignore_errors=True)

    # Remove C++ -related files
    cpp_files = (os.path.join('doc', 'SConscript'),
                 os.path.join('doc', 'doxygen.conf.in'),
                 os.path.join('ups', f'{package_name}.cfg'))
    for filename in cpp_files:
        print(f'(post-gen hook) Removing {filename} file')
        try:
            os.remove(filename)
        except OSError:
            print(f'(post-gen hool) Failed to remove {filename}')
            pass

# Remove Python-specific directories and files if cookiecutter.uses_python
# is False
if not uses_python:
    python_dirnames = (
        'python',
        os.path.join('doc', python_namespace),
        'bin.src',
        'tests',
        '.github',
    )
    python_filenames = {
        'setup.cfg',
    }
    for dirname in python_dirnames:
        print(f'(post-gen hook) Removing {dirname} directory')
        shutil.rmtree(dirname, ignore_errors=True)
    for filename in python_filenames:
        print(f'(post-gen hook) Removing {filename} file')
        try:
            os.remove(filename)
        except OSError:
            pass

# Remove the package documentation directory if module documentation
# directories are available
if uses_python or uses_cpp:
    package_doc_dirname = os.path.join('doc', package_name)
    print(f'(post-gen hook) Removing {package_doc_dirname} directory')
    shutil.rmtree(package_doc_dirname, ignore_errors=True)

# If the package is not part of a stack, then make either its package or
# module documentation directory the homepage at the root of doc/ for
# standalone deployment.
if stack_name == "None":
    root_path = os.path.join('doc', 'index.rst')
    if uses_python or uses_cpp:
        # Use the module documentation directory as the root
        new_root_path = os.path.join('doc', python_namespace, 'index.rst')
        print('(post-gen hook) Creating a standalone doc directory '
              'with the module homepage.')
    else:
        # Use the package documentation directory as the root
        new_root_path = os.path.join('doc', package_name, 'index.rst')
        print('(post-gen hook) Creating a standalone doc directory '
              'with the package homepage.')

    # Replace the original root with the new one
    os.remove(root_path)
    os.rename(new_root_path, root_path)

    # Delete either the original module or package documentation directory
    shutil.rmtree(os.path.dirname(new_root_path), ignore_errors=True)
