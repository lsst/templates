import unittest
import logging

from lsst.sitcom.{{ cookiecutter.username }}.example_function import example_function

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class TestModel(unittest.TestCase):

    def test_example_function(self):
        """Check that proper value is returned."""
        multiplier = 11
        value = 10
        expected_result = 110
        logger.debug(f'Multiplier is {multiplier}, value is {value}')
        result = example_function(value, multiplier=multiplier)
        self.assertTrue(result, expected_result)

    def test_input_error(self):
        """Test that error handling raises an error when a string is declared."""
        value = '10'  # strings are not supported
        with self.assertRaises(IOError):
            example_function(value)
