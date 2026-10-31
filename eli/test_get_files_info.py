import os
import tempfile
import unittest

from functions.get_files_info import get_files_info


CALCULATOR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculator")


class TestGetFilesInfo(unittest.TestCase):
    def test_current_directory(self) -> None:
        result = get_files_info(CALCULATOR_DIR, ".")
        self.assertIn("- main.py: file_size=", result)
        self.assertIn("- pkg: file_size=", result)
        self.assertIn("is_dir=True", result)

    def test_subdirectory(self) -> None:
        result = get_files_info(CALCULATOR_DIR, "pkg")
        self.assertIn("- calculator.py: file_size=", result)
        self.assertIn("is_dir=False", result)

    def test_absolute_path_outside(self) -> None:
        result = get_files_info(CALCULATOR_DIR, "/bin")
        self.assertTrue(result.startswith("Error: Cannot list"))

    def test_parent_traversal(self) -> None:
        result = get_files_info(CALCULATOR_DIR, "../")
        self.assertTrue(result.startswith("Error: Cannot list"))

    def test_not_a_directory(self) -> None:
        result = get_files_info(CALCULATOR_DIR, "main.py")
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("is not a directory", result)

    def test_listing_is_sorted(self) -> None:
        with tempfile.TemporaryDirectory() as wd:
            for name in ["c.txt", "a.txt", "b.txt"]:
                open(os.path.join(wd, name), "w").close()
            names = [line.split(":")[0] for line in get_files_info(wd, ".").splitlines()]
            self.assertEqual(names, ["- a.txt", "- b.txt", "- c.txt"])

    def test_broken_entry_does_not_abort_listing(self) -> None:
        with tempfile.TemporaryDirectory() as wd:
            open(os.path.join(wd, "good.txt"), "w").close()
            os.symlink(os.path.join(wd, "missing"), os.path.join(wd, "broken"))
            result = get_files_info(wd, ".")
            self.assertIn("- broken: Error:", result)
            self.assertIn("- good.txt: file_size=0 bytes", result)


if __name__ == "__main__":
    unittest.main()
