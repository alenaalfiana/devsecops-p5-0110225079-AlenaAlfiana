import unittest

from library.validators import (
    ValidationError,
    validate_isbn,
    validate_member,
    validate_title,
    validate_year,
)


class ValidatorTests(unittest.TestCase):
    def test_isbn_valid_with_dash(self):
        self.assertEqual(validate_isbn("978-0-13-235088-4"), "9780132350884")

    def test_isbn_invalid(self):
        with self.assertRaises(ValidationError):
            validate_isbn("abc123")

    def test_title_empty(self):
        with self.assertRaises(ValidationError):
            validate_title("   ")

    def test_year_range(self):
        self.assertEqual(validate_year(2020), 2020)
        with self.assertRaises(ValidationError):
            validate_year(5)

    def test_member(self):
        self.assertEqual(validate_member(" Budi Santoso "), "Budi Santoso")
        with self.assertRaises(ValidationError):
            validate_member("123; DROP TABLE")


if __name__ == "__main__":
    unittest.main()
