import unittest
from tools.validation import *

class TestValidation(unittest.TestCase):
    def test_validate_type(self):
        self.assertIsNone(validate_type(123, int))
        self.assertIsNone(validate_type("string", str))
        self.assertIsNone(validate_type(1.23, float))
        self.assertIsNone(validate_type([], list))

        with self.assertRaises(TypeError): validate_type("string", int)
        with self.assertRaises(TypeError): validate_type(1.45, int)
        with self.assertRaises(TypeError): validate_type({4, 5, 6}, dict)

if __name__ == '__main__':
    unittest.main()
