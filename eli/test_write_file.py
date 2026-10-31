import os
import tempfile
import unittest

from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.wd = self._tmp.name

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def read(self, path: str) -> str:
        with open(os.path.join(self.wd, path)) as f:
            return f.read()

    def test_overwrite_existing_file(self) -> None:
        with open(os.path.join(self.wd, "notes.txt"), "w") as f:
            f.write("old content")
        result = write_file(self.wd, "notes.txt", "new content")
        self.assertTrue(result.startswith("Successfully wrote"))
        self.assertEqual(self.read("notes.txt"), "new content")

    def test_creates_parent_directories(self) -> None:
        result = write_file(self.wd, "a/b/new.txt", "hello")
        self.assertIn("5 characters written", result)
        self.assertEqual(self.read("a/b/new.txt"), "hello")

    def test_absolute_path_outside(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            target = os.path.join(outside, "escape.txt")
            result = write_file(self.wd, target, "nope")
            self.assertTrue(result.startswith("Error: Cannot write"))
            self.assertFalse(os.path.exists(target))

    def test_parent_traversal(self) -> None:
        result = write_file(self.wd, "../escape.txt", "nope")
        self.assertTrue(result.startswith("Error: Cannot write"))

    def test_directory_target(self) -> None:
        os.mkdir(os.path.join(self.wd, "subdir"))
        result = write_file(self.wd, "subdir", "nope")
        self.assertIn("is a directory", result)


if __name__ == "__main__":
    unittest.main()
