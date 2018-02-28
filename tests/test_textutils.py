"""Tests for the templatekit.textutils module.
"""

from templatekit.textutils import reformat_content_lines


def test_reformat_content_lines():
    """Test reformatting text (a Python comment block).
    """
    sample = (
        'Line 1\n'
        'Line 2\n'
    )
    expected = (
        '# Line 1\n'
        '# Line 2\n'
    )
    result = reformat_content_lines(sample, '# {}')
    assert result == expected


def test_reformat_content_lines_no_final_newline():
    """Same as `test_reformat_content_lines` except the original content
    lacks a final newline.
    """
    sample = (
        'Line 1\n'
        'Line 2'
    )
    expected = (
        '# Line 1\n'
        '# Line 2\n'
    )
    result = reformat_content_lines(sample, '# {}')
    assert result == expected


def test_reformat_content_lines_header_footer():
    """Test reformatting text and including a header and footer (like a C++
    comment block).
    """
    sample = (
        'Line 1\n'
        'Line 2\n'
    )
    expected = (
        '/*\n'
        ' * Line 1\n'
        ' * Line 2\n'
        ' */\n'
    )
    result = reformat_content_lines(sample, ' * {}', header="/*", footer=" */")
    assert result == expected


def test_reformat_content_lines_header_footer_no_final_newline():
    """Same as `test_reformat_content_lines_header_footer` except the original
    content lacks a final newline.
    """
    sample = (
        'Line 1\n'
        'Line 2'
    )
    expected = (
        '/*\n'
        ' * Line 1\n'
        ' * Line 2\n'
        ' */\n'
    )
    result = reformat_content_lines(sample, ' * {}', header="/*", footer=" */")
    assert result == expected
