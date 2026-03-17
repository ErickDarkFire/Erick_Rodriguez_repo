# -*- coding: utf-8 -*-

"""
Mock up testing examples.
"""
import unittest
from unittest.mock import patch, mock_open, MagicMock
import subprocess

from mockup_exercises import (
    fetch_data_from_api,
    read_data_from_file,
    execute_command,
    perform_action_based_on_time,
)


class TestFetchDataFromApi(unittest.TestCase):
    """
    Fetch data from API unittest class.
    """

    @patch("mockup_exercises.requests.get")
    def test_fetch_data_from_api_success(self, mock_get):
        """
        Success case.
        """
        # Set up the mock response
        mock_get.return_value.json.return_value = {"key": "value"}

        # Mock the requests.get method
        # with patch("requests.get") as mock_get:
        #     mock_get.return_value.status_code = 200
        #     mock_get.return_value.json.return_value = [
        #         {"id": 1, "title": "Title 1", "body": "Body 1"},
        #         {"id": 2, "title": "Title 2", "body": "Body 2"},
        #     ]

        # patch_get = patch('requests.get')
        # mock_get = patch_get.start()
        # mock_get.return_value.status_code = 200
        # mock_get.return_value.json.return_value = [
        #     {"id": 1, "title": "Title 1", "body": "Body 1"},
        #     {"id": 2, "title": "Title 2", "body": "Body 2"},
        # ]
        # patch_get.stop()

        # Call the function under test
        result = fetch_data_from_api("https://api.example.com/data")

        # Assert that the function returns the expected result
        self.assertEqual(result, {"key": "value"})

        # Assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with("https://api.example.com/data", timeout=10)


class TestPerformActionBasedOnTime(unittest.TestCase):
    """
    Perform Action Based On Time unittest class.
    """

    @patch("mockup_exercises.time.time")
    def test_perform_action_based_on_time_action_a(self, mock_time):
        """
        Action A.
        """
        # Set up the mock response
        mock_time.return_value = 5

        # Call the function under test
        result = perform_action_based_on_time()

        # Assert that the function returns the expected result
        self.assertEqual(result, "Action A")

    @patch("mockup_exercises.time.time")
    def test_perform_action_based_on_time_action_b(self, mock_time):
        """
        Action B.
        """
        # Set up the mock response
        mock_time.return_value = 15

        # Call the function under test
        result = perform_action_based_on_time()

        # Assert that the function returns the expected result
        self.assertEqual(result, "Action B")


class TestFetchDataFromApiErrors(unittest.TestCase):
    """
    Additional test cases for fetch_data_from_api.
    """

    @patch("mockup_exercises.requests.get")
    def test_fetch_data_from_api_exception(self, mock_get):
        """
        Exception case when request fails.
        """
        mock_get.side_effect = Exception("API error")

        with self.assertRaises(Exception):
            fetch_data_from_api("https://api.example.com/data")


class TestReadDataFromFile(unittest.TestCase):
    """
    Read data from file unittest class.
    """

    @patch("builtins.open", new_callable=mock_open, read_data="file content")
    def test_read_data_from_file_success(self, mock_file):
        """
        Success case.
        """
        result = read_data_from_file("test.txt")

        self.assertEqual(result, "file content")
        mock_file.assert_called_once_with("test.txt", encoding="utf-8")

    @patch("builtins.open")
    def test_read_data_from_file_not_found(self, mock_file):
        """
        FileNotFoundError case.
        """
        mock_file.side_effect = FileNotFoundError("File not found")

        with self.assertRaises(FileNotFoundError):
            read_data_from_file("test.txt")


class TestExecuteCommand(unittest.TestCase):
    """
    Execute command unittest class.
    """

    @patch("mockup_exercises.subprocess.run")
    def test_execute_command_success(self, mock_run):
        """
        Success case.
        """
        mock_process = MagicMock()
        mock_process.stdout = "command output"
        mock_run.return_value = mock_process

        result = execute_command(["ls", "-l"])

        self.assertEqual(result, "command output")
        mock_run.assert_called_once_with(
            ["ls", "-l"], capture_output=True, check=False, text=True
        )

    @patch("mockup_exercises.subprocess.run")
    def test_execute_command_called_process_error(self, mock_run):
        """
        CalledProcessError case.
        """
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")

        with self.assertRaises(subprocess.CalledProcessError):
            execute_command(["ls", "-l"])
