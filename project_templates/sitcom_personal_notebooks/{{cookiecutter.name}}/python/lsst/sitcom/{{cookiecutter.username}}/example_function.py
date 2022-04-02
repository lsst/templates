def example_function(input_value, multiplier=10):
    """An example function that can be imported and called in a notebook.

    This function will return the input value multiplied by 10.
    """
    if not (isinstance(input_value, float) or isinstance(input_value, int)):
        raise IOError(f"Input value of {input_value} is not a float.")

    return input_value*multiplier
