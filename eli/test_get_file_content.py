import os
import tempfile
import unittest

from config import MAX_CHARS
from functions.get_file_content import get_file_content


CALCULATOR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculator")


class TestGetFileContent(unittest.TestCase):
    def test_large_file_is_truncated(self) -> None:
        content = "x" * (MAX_CHARS + 100)
        with tempfile.TemporaryDirectory() as wd:
            with open(os.path.join(wd, "big.txt"), "w") as f:
                f.write(content)
            result = get_file_content(wd, "big.txt")
        self.assertTrue(result.startswith(content[:MAX_CHARS]))
        self.assertIn(f"truncated at {MAX_CHARS} characters", result)

    def test_small_file(self) -> None:
        result = get_file_content(CALCULATOR_DIR, "main.py")
        self.assertIn("def main()", result)
        self.assertNotIn("truncated", result)

    def test_file_in_subdirectory(self) -> None:
        result = get_file_content(CALCULATOR_DIR, "pkg/calculator.py")
        self.assertIn("class Calculator", result)

    def test_absolute_path_outside(self) -> None:
        result = get_file_content(CALCULATOR_DIR, "/bin/cat")
        self.assertTrue(result.startswith("Error: Cannot read"))

    def test_parent_traversal(self) -> None:
        result = get_file_content(CALCULATOR_DIR, "../main.py")
        self.assertTrue(result.startswith("Error: Cannot read"))

    def test_missing_file(self) -> None:
        result = get_file_content(CALCULATOR_DIR, "pkg/does_not_exist.py")
        self.assertTrue(result.startswith("Error: File not found"))

    def test_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as outside, tempfile.TemporaryDirectory() as wd:
            with open(os.path.join(outside, "secret.txt"), "w") as f:
                f.write("secret")
            os.symlink(outside, os.path.join(wd, "link"))
            result = get_file_content(wd, "link/secret.txt")
            self.assertTrue(result.startswith("Error: Cannot read"))


if __name__ == "__main__":
    unittest.main()
