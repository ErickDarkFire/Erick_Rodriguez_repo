# -*- coding: utf-8 -*-

"""
White-box unit testing examples.
"""
import subprocess
import unittest
from unittest.mock import patch, MagicMock

from mockup_exercises import (
    fetch_data_from_api,
    read_data_from_file,
    execute_command,
    perform_action_based_on_time,
)


class TestTime(unittest.TestCase):
    """
    Check time function with mock
    """

    @patch("mockup_exercises.time.time")
    def test_a(self, mock):
        mock.return_value = 6

        result = perform_action_based_on_time()

        self.assertEqual(result, "Action A")

    @patch("mockup_exercises.time.time")
    def test_b(self, mock):
        mock.return_value = 11

        result = perform_action_based_on_time()

        self.assertEqual(result, "Action B")


class TestFetchDataFromApi(unittest.TestCase):
    @patch("mockup_exercises.requests.get")
    def test_fetch_data_from_api(self, mock_get):
        # Arrange
        fake_response = MagicMock()
        fake_response.json.return_value = {"id": 1, "name": "Erick"}

        mock_get.return_value = fake_response

        url = "https://fake-api.com/data"

        # Act
        result = fetch_data_from_api(url)

        # Assert
        self.assertEqual(result, {"id": 1, "name": "Erick"})
        mock_get.assert_called_once_with(url, timeout=10)
        fake_response.json.assert_called_once()


class TestReadDataFromFile(unittest.TestCase):
    @patch("mockup_exercises.open")
    def test_read_data_success(self, mock_open):
        mock_file = MagicMock()
        mock_file.read.return_value = "Hola mundo"

        mock_open.return_value.__enter__.return_value = mock_file

        filename = "fake.txt"

        result = read_data_from_file(filename)

        self.assertEqual(result, "Hola mundo")
        mock_open.assert_called_once_with(filename, encoding="utf-8")
        mock_file.read.assert_called_once()

    @patch("mockup_exercises.open")
    def test_read_data_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError

        with self.assertRaises(FileNotFoundError):
            read_data_from_file("missing.txt")

        mock_open.assert_called_once_with("missing.txt", encoding="utf-8")


class TestExecuteCommand(unittest.TestCase):
    @patch("mockup_exercises.subprocess.run")
    def test_execute_command_success(self, mock_run):
        # Arrange
        fake_result = MagicMock()
        fake_result.stdout = "Hello World\n"

        mock_run.return_value = fake_result

        command = ["echo", "Hello World"]

        # Act
        result = execute_command(command)

        # Assert
        self.assertEqual(result, "Hello World\n")
        mock_run.assert_called_once_with(
            command, capture_output=True, check=False, text=True
        )

    @patch("mockup_exercises.subprocess.run")
    def test_execute_command_raises_exception(self, mock_run):
        # Arrange
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="fake_cmd"
        )

        # Act & Assert
        with self.assertRaises(subprocess.CalledProcessError):
            execute_command("fake_cmd")
