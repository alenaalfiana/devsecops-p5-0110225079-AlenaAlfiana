import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from library.cli import run


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = os.path.join(self.tmp.name, "d.json")

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *args):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = run(["--data", self.data, *args])
        return code, out.getvalue(), err.getvalue()

    def test_full_flow(self):
        code, out, _ = self._run("add", "9780132350884", "Clean Code", "Robert Martin", "2008")
        self.assertEqual(code, 0)
        self.assertIn("Buku ditambahkan", out)

        code, out, _ = self._run("search", "clean")
        self.assertIn("tersedia", out)

        code, out, _ = self._run("borrow", "9780132350884", "Budi")
        self.assertEqual(code, 0)

        code, out, _ = self._run("loans")
        self.assertIn("Budi", out)

        code, out, _ = self._run("return", "9780132350884")
        self.assertIn("dikembalikan", out)

    def test_error_exit_code(self):
        code, _, err = self._run("borrow", "1234567890", "Budi")
        self.assertEqual(code, 1)
        self.assertIn("Error", err)
