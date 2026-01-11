"""
Tests for log service.
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ntclient.services.logs import log_add, log_analyze, log_view


class TestLogs(unittest.TestCase):
    """Test class for log service"""

    def setUp(self):
        """Setup temp dir"""
        self.test_dir = tempfile.mkdtemp()
        self.patcher = patch("ntclient.services.logs.NUTRA_HOME", self.test_dir)
        self.mock_home = self.patcher.start()

    def tearDown(self):
        """Cleanup"""
        self.patcher.stop()
        shutil.rmtree(self.test_dir)

    @patch("ntclient.services.logs.sql_food_details")
    def test_log_add(self, mock_sql):
        """Test adding to log"""
        # Mock food exists
        mock_sql.return_value = [
            (1001, 100, "Test Food", "", "", "", "", "", 0, "", 0, 0, 0, 0)
        ]

        log_add(1001, 150.0, "2099-01-01")

        log_path = os.path.join(self.test_dir, "2099-01-01.csv")
        self.assertTrue(os.path.exists(log_path))
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("1001,150.0", content)

    @patch("ntclient.services.logs.sql_food_details")
    def test_log_add_invalid_food(self, mock_sql):
        """Test adding invalid food"""
        mock_sql.return_value = []  # Food not found

        # Should print error and not create file (or not append)
        # Using print capture could be added, but for now check file state
        log_add(9999, 150.0, "2099-01-02")

        log_path = os.path.join(self.test_dir, "2099-01-02.csv")
        self.assertFalse(os.path.exists(log_path))

    @patch("ntclient.services.logs.sql_food_details")
    @patch("ntclient.services.logs.read_log")
    def test_log_view(self, mock_read, mock_sql):
        """Test viewing log"""
        mock_read.return_value = [{"id": "1001", "grams": "150.0"}]
        # Mock needs 3 elements: id, ..., name
        mock_sql.return_value = [(1001, 100, "Test Food")]

        # Just ensure no exception
        log_view("2099-01-01")

    @patch("ntclient.services.logs.day_analyze")
    def test_log_analyze(self, mock_analyze):
        """Test analyzing log"""
        # Create dummy log
        log_path = os.path.join(self.test_dir, "2099-01-01.csv")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("id,grams\n1001,100")

        log_analyze("2099-01-01")
        mock_analyze.assert_called_once()


if __name__ == "__main__":
    unittest.main()
