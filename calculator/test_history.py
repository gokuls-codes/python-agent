import unittest
from pkg.history import save_to_history, load_history
import os

class TestHistory(unittest.TestCase):
    def setUp(self):
        if os.path.exists("history.txt"):
            os.remove("history.txt")

    def test_save_and_load(self):
        save_to_history("5 + 5")
        save_to_history("10 * 2")
        history = load_history()
        self.assertEqual(history, ["5 + 5", "10 * 2"])

    def tearDown(self):
        if os.path.exists("history.txt"):
            os.remove("history.txt")

if __name__ == "__main__":
    unittest.main()
