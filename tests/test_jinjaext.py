"""Tests for the templatekit.jinjaext module.
"""

from templatekit.jinjaext import (
    convert_py_to_cpp_namespace_code,
    convert_py_namespace_to_cpp_header_def,
    convert_py_to_cpp_namespace)


def test_cpp_namespace_code():
    """Test convert_py_to_cpp_namespace_code.
    """
    python_namespace = 'lsst.example'

    expected = (
        'namespace lsst { example {\n'
        '\n'
        '}} // lsst::example'
    )

    assert expected == convert_py_to_cpp_namespace_code(python_namespace)


def test_cpp_header_def():
    """Test convert_py_namespace_to_cpp_header_def.
    """
    python_namespace = 'lsst.example'
    expected = 'LSST_EXAMPLE_H'
    assert expected == convert_py_namespace_to_cpp_header_def(python_namespace)


def test_cpp_namespace():
    """Test convert_py_to_cpp_namespace.
    """
    python_namespace = 'lsst.example'
    expected = 'lsst::example'
    assert expected == convert_py_to_cpp_namespace(python_namespace)
