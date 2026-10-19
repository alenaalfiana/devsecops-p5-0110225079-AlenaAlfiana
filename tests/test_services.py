import os
import tempfile
import unittest

from library.services import LibraryError, LibraryService
from library.storage import JsonStorage


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "data.json")
        self.service = LibraryService(JsonStorage(self.path))
        self.service.add_book("9780132350884", "Clean Code", "Robert Martin", 2008)

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_duplicate(self):
        with self.assertRaises(LibraryError):
            self.service.add_book("9780132350884", "Clean Code", "Robert Martin", 2008)

    def test_search(self):
        self.assertEqual(len(self.service.search("clean")), 1)
        self.assertEqual(self.service.search("python"), [])

    def test_borrow_and_return(self):
        self.service.borrow("9780132350884", "Budi")
        self.assertEqual(len(self.service.active_loans()), 1)
        with self.assertRaises(LibraryError):
            self.service.borrow("9780132350884", "Sari")
        self.service.return_book("9780132350884")
        self.assertEqual(self.service.active_loans(), [])

    def test_return_without_loan(self):
        with self.assertRaises(LibraryError):
            self.service.return_book("9780132350884")

    def test_borrow_unknown_book(self):
        with self.assertRaises(LibraryError):
            self.service.borrow("1234567890", "Budi")

    def test_persistence(self):
        self.service.borrow("9780132350884", "Budi")
        reloaded = LibraryService(JsonStorage(self.path))
        self.assertEqual(len(reloaded.books), 1)
        self.assertFalse(reloaded.books[0].available)
        self.assertEqual(len(reloaded.active_loans()), 1)
