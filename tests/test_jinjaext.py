"""Tests for the templatekit.jinjaext module.
"""

from templatekit.jinjaext import convert_py_to_cpp_namespace_code


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
