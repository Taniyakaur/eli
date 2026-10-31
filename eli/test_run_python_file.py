import os
import tempfile
import unittest

from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.wd = self._tmp.name

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, path: str, content: str) -> None:
        with open(os.path.join(self.wd, path), "w") as f:
            f.write(content)

    def test_captures_stdout(self) -> None:
        self.write("hello.py", "print('hello')")
        result = run_python_file(self.wd, "hello.py")
        self.assertIn("STDOUT:\nhello", result)
        self.assertNotIn("exited with code", result)

    def test_passes_args(self) -> None:
        self.write("echo.py", "import sys; print(' '.join(sys.argv[1:]))")
        result = run_python_file(self.wd, "echo.py", ["3", "+", "5"])
        self.assertIn("3 + 5", result)

    def test_reports_stderr_and_exit_code(self) -> None:
        self.write("fail.py", "import sys; sys.stderr.write('boom'); sys.exit(2)")
        result = run_python_file(self.wd, "fail.py")
        self.assertIn("Process exited with code 2", result)
        self.assertIn("STDERR:\nboom", result)

    def test_no_output(self) -> None:
        self.write("quiet.py", "")
        self.assertIn("No output produced", run_python_file(self.wd, "quiet.py"))

    def test_runs_from_working_directory(self) -> None:
        self.write("cwd.py", "import os; print(os.getcwd())")
        result = run_python_file(self.wd, "cwd.py")
        self.assertIn(os.path.realpath(self.wd), result)

    def test_parent_traversal(self) -> None:
        result = run_python_file(self.wd, "../main.py")
        self.assertTrue(result.startswith("Error: Cannot execute"))

    def test_missing_file(self) -> None:
        result = run_python_file(self.wd, "nonexistent.py")
        self.assertIn("does not exist", result)

    def test_not_a_python_file(self) -> None:
        self.write("notes.txt", "hi")
        result = run_python_file(self.wd, "notes.txt")
        self.assertIn("is not a Python file", result)


if __name__ == "__main__":
    unittest.main()
