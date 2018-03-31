from setuptools import setup, find_packages

package_name = 'lsst-templatekit'
description = 'Tookit for rendering LSST project templates.'
author = 'Association of Universities for Research in Astronomy'
author_email = 'sqre-admin@lists.lsst.org'
license = 'MIT'
url = 'https://github.com/lsst/templates'
pypi_classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
]
keywords = ['lsst', 'cookiecutter']
version = '0.1.0b1'

# Core dependencies
install_requires = [
    'cookiecutter==1.6.0',
    'Jinja2==2.10',
    'scons==3.0.1',
    'click>=6.7,<7.0',
    'pyperclip>=1.6.0,<1.7.0'
]

# Test dependencies
tests_require = [
    'pytest==3.4.1',
    'pytest-flake8==0.9.1',
]
tests_require += install_requires

# Setup-time dependencies
setup_requires = [
    'pytest-runner>=2.11.1,<3'
]

setup(
    name=package_name,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    classifiers=pypi_classifiers,
    keywords=keywords,
    packages=find_packages(exclude=['docs', 'tests', 'file_templates',
                                    'project_templates']),
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    entry_points={
        'console_scripts': ['templatekit = templatekit.scripts.main:main']
    }
)
