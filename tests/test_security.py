import os
import sys
import tempfile
import shutil
import unittest

# Ensure project root is on sys.path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils.security import SecurityManager  # noqa: E402


class TestSecurityManager(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.mkdtemp()
        self.sm = SecurityManager(self.workspace)

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)

    def test_allows_file_inside_workspace(self):
        path = os.path.join(self.workspace, "test.txt")
        self.assertTrue(self.sm.check_file_access(path))

    def test_blocks_file_outside_workspace(self):
        path = "/etc/passwd"
        self.assertFalse(self.sm.check_file_access(path))

    def test_blocks_path_traversal(self):
        path = os.path.join(self.workspace, "..", "evil.txt")
        self.assertFalse(self.sm.check_file_access(path))

    def test_safe_open_write_and_read(self):
        path = os.path.join(self.workspace, "data.txt")
        f = self.sm.safe_open(path, "w")
        self.assertIsNotNone(f)
        f.write("hello world")
        f.close()

        f = self.sm.safe_open(path, "r")
        self.assertIsNotNone(f)
        self.assertEqual(f.read(), "hello world")
        f.close()

    def test_safe_open_outside_workspace_returns_none(self):
        f = self.sm.safe_open("/etc/passwd", "r")
        self.assertIsNone(f)

    def test_safe_open_binary_mode(self):
        path = os.path.join(self.workspace, "binary.bin")
        f = self.sm.safe_open(path, "wb")
        self.assertIsNotNone(f)
        f.write(b"\x00\x01\x02")
        f.close()

        f = self.sm.safe_open(path, "rb")
        self.assertIsNotNone(f)
        self.assertEqual(f.read(), b"\x00\x01\x02")
        f.close()

    def test_safe_mkdir(self):
        dir_path = os.path.join(self.workspace, "subdir")
        self.assertTrue(self.sm.safe_mkdir(dir_path))
        self.assertTrue(os.path.isdir(dir_path))

    def test_safe_mkdir_outside_workspace_fails(self):
        self.assertFalse(self.sm.safe_mkdir("/tmp/should_not_exist_xyz"))

    def test_safe_remove(self):
        path = os.path.join(self.workspace, "to_remove.txt")
        with open(path, "w") as f:
            f.write("remove me")
        self.assertTrue(self.sm.safe_remove(path))
        self.assertFalse(os.path.exists(path))

    def test_safe_remove_outside_workspace_fails(self):
        self.assertFalse(self.sm.safe_remove("/etc/hosts"))

    def test_safe_rename(self):
        src = os.path.join(self.workspace, "old.txt")
        dst = os.path.join(self.workspace, "new.txt")
        with open(src, "w") as f:
            f.write("rename me")
        self.assertTrue(self.sm.safe_rename(src, dst))
        self.assertTrue(os.path.exists(dst))
        self.assertFalse(os.path.exists(src))

    def test_safe_copy(self):
        src = os.path.join(self.workspace, "src.txt")
        dst = os.path.join(self.workspace, "dst.txt")
        with open(src, "w") as f:
            f.write("copy me")
        self.assertTrue(self.sm.safe_copy(src, dst))
        self.assertTrue(os.path.exists(dst))
        with open(dst) as f:
            self.assertEqual(f.read(), "copy me")

    def test_check_directory_access(self):
        self.assertTrue(self.sm.check_directory_access(self.workspace))
        self.assertFalse(self.sm.check_directory_access("/etc"))


if __name__ == "__main__":
    unittest.main()
