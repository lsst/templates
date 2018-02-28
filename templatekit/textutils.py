"""Generic utilities for working with text content.
"""

__all__ = ('reformat_content_lines',)


def reformat_content_lines(content, fmt, header=None, footer=None):
    """Apply a (new-style) Python format expression to each line of a string
    content block.

    Also optionally add a header and/or footer to the content block.

    Parameters
    ----------
    fmt : `str`
        Python format statement that each line of the content is processed
        with. The default format argument is the original content line.
        For example, ``# {}`` turns the content into a Python comment.
    header : `str`, optional
        Text content that can be added above the original content.
    footer : `str`, optional
        Text content that can be added before the original content
    """
    # Take any final newline off the end of the content so there isn't an
    # empty final line
    content_lines = content.rstrip().split('\n')
    output_lines = []

    if header is not None:
        output_lines.append(header)

    for line in content_lines:
        output_lines.append(fmt.format(line).rstrip())

    if footer is not None:
        output_lines.append(footer)

    # Always include a final newline
    return '\n'.join(output_lines) + '\n'
