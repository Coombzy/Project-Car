#!/usr/bin/env python3
"""Unit tests for the last_user and is_root helpers in check_prod_dockerfiles."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_prod_dockerfiles import is_root, last_user


class CheckProdDockerfiles(unittest.TestCase):
    def test_last_user_wins(self):
        text = "FROM x\nUSER first\nRUN echo\nuser second\n"
        self.assertEqual(last_user(text), "second")

    def test_comments_are_ignored(self):
        self.assertEqual(last_user("# USER commented\nUSER app # keep\n"), "app")
        self.assertIsNone(last_user("# USER commented\nRUN echo  # USER no\n"))
        self.assertIsNone(last_user("USER\nRUN echo\n"))

    def test_missing_user_is_root(self):
        self.assertIsNone(last_user("FROM x\nRUN echo\n"))
        self.assertTrue(is_root(None))

    def test_user_zero_and_root_are_root(self):
        for user in ("0", "root", "ROOT", "root:root", "0:0"):
            self.assertTrue(is_root(user), user)

    def test_non_root_user_is_not_root(self):
        for user in ("appuser", "1000", "app:group", "nobody"):
            self.assertFalse(is_root(user), user)


if __name__ == "__main__":
    outcome = unittest.main(argv=[sys.argv[0]], exit=False, verbosity=1).result
    if not outcome.wasSuccessful():
        sys.exit(1)
    print("ok")
