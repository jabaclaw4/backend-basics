import unittest

from processing.preprocessing import (
    DEFAULT_DESCRIPTION,
    is_expensive,
    is_warm_clothes_needed,
    normalize_description,
)


class PreprocessingTest(unittest.TestCase):
    def test_warm_clothes(self):
        self.assertTrue(is_warm_clothes_needed(-3.2))
        self.assertFalse(is_warm_clothes_needed(0))
        self.assertFalse(is_warm_clothes_needed(15))

    def test_expensive(self):
        self.assertTrue(is_expensive(100.5))
        self.assertFalse(is_expensive(100))
        self.assertFalse(is_expensive(92.15))

    def test_default_description(self):
        self.assertEqual(normalize_description(""), DEFAULT_DESCRIPTION)
        self.assertEqual(normalize_description(None), DEFAULT_DESCRIPTION)
        self.assertEqual(normalize_description(" clear sky "), "clear sky")


if __name__ == "__main__":
    unittest.main()