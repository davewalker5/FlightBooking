import unittest
from unittest.mock import patch
from src.booking_app.data_entry import trimmed_input


class TestInputUtils(unittest.TestCase):
    @patch("builtins.input", side_effect=["Test String"])
    def test_string_with_no_whitespace(self, _):
        s = trimmed_input("")
        self.assertEqual("Test String", s)

    @patch("builtins.input", side_effect=["    Test String"])
    def test_leading_whitespace_is_removed(self, _):
        s = trimmed_input("")
        self.assertEqual("Test String", s)

    @patch("builtins.input", side_effect=["Test String    "])
    def test_trailing_whitespace_is_removed(self, _):
        s = trimmed_input("")
        self.assertEqual("Test String", s)

    @patch("builtins.input", side_effect=["    Test String    "])
    def test_leading_and_trailing_whitespace_is_removed(self, _):
        s = trimmed_input("")
        self.assertEqual("Test String", s)
