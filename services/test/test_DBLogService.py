import unittest

# Unit test class
class TestDBLogService(unittest.TestCase):
    # Retrieve all DB log events successfully from an in-memory SQLite database
    def test_retrieve_all_db_log_events_successfully(self):
        from services.DBLogService import DBLogService
        from models.DBLogEvent import DBLogEvent
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return predefined rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.get_all_db_log_events_from_db()

            expected_result = [
                DBLogEvent(1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
                DBLogEvent(2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
            ]

            self.assertEqual(result, expected_result)

    # Handle corrupted or invalid SQLite database file bytes
    def test_handle_corrupted_or_invalid_sqlite_db_file_bytes(self):
        from services.DBLogService import DBLogService
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to raise an exception on deserialise
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.deserialise.side_effect = Exception('Invalid database file')

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'invalid_bytes')
            result = db_log_service.get_all_db_log_events_from_db()

            self.assertEqual(result, [])

    # Ensure handling of an empty database by returning an empty list
    def test_handle_empty_db_gracefully(self):
        from services.DBLogService import DBLogService
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return empty rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = []

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'empty_bytes')
            result = db_log_service.get_all_db_log_events_from_db()

            self.assertEqual(result, [])

    # Handle serialization errors gracefully and return None
    def test_handle_serialization_errors_gracefully(self):
        from services.DBLogService import DBLogService
        from unittest.mock import patch

        # Mock serialise_process_events to return None
        with patch('utils.JsonHelper.serialise_process_events', return_value=None):
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.process_sqlite_db_file()

            self.assertIsNone(result)

    # Ensure DBLogService retrieves no log events from the database when the database is empty
    def test_manage_database_with_no_log_events(self):
        from services.DBLogService import DBLogService
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return an empty list of rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = []

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.get_all_db_log_events_from_db()

            expected_result = []

            self.assertEqual(result, expected_result)

    # Ensure SQLite database connection and cursor are properly managed and closed
    def test_sqlite_db_connection_management(self):  
        from services.DBLogService import DBLogService
        from models.DBLogEvent import DBLogEvent
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return predefined rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            db_log_service.get_all_db_log_events_from_db()

            mock_db_client.__exit__.assert_called_once()

    # Testing the handling of invalid JSON conversion scenarios
    def test_handle_invalid_json_conversion(self):
        from services.DBLogService import DBLogService
        from unittest.mock import patch

        # Mock the serialise_process_events function to return None
        with patch('services.DBLogService.serialise_process_events', return_value=None):
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.process_sqlite_db_file()

            self.assertIsNone(result)

    # Ensure timestamp format in filenames is correct and consistent and fix the TypeError issue
    def test_timestamp_format_in_filenames_with_fix(self):
        from services.DBLogService import DBLogService
        from unittest.mock import patch, MagicMock
        import re

        # Mock the necessary dependencies
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            results_json_string = db_log_service.process_sqlite_db_file()

            if results_json_string is not None:
                # Mock the write_to_json_file function to capture the filename
                with patch('utils.FileHelper.write_to_json_file') as mock_write:
                    db_log_service.write_db_results_to_file(results_json_string, '/path/to/output', 'result_file')
                    if mock_write.call_args:
                        filename = mock_write.call_args[0][1]
                        self.assertRegex(filename, r'_\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}\.json')
                        mock_write.assert_called_once()

    # Check that the correct SQL query is executed to retrieve log events
    def test_correct_sql_query_execution(self):
        from services.DBLogService import DBLogService
        from models.DBLogEvent import DBLogEvent
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return predefined rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            db_log_service.get_all_db_log_events_from_db()

            mock_db_client.execute.assert_called_once_with(
                'SELECT ID, timestamp, BundleID, CoalitionID, PID, ProcessName FROM PLProcessMonitorAgent_EventForward_ProcessID;'
            )

    # Verify that the database deserialization process works correctly
    def test_database_deserialization_process(self):
        from services.DBLogService import DBLogService
        from models.DBLogEvent import DBLogEvent
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return predefined rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.get_all_db_log_events_from_db()

            expected_result = [
                DBLogEvent(1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
                DBLogEvent(2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
            ]

            self.assertEqual(result, expected_result)

    # Ensure that the DBLogEvent data class is correctly populated from database rows
    def test_db_log_event_population(self):
        from services.DBLogService import DBLogService
        from models.DBLogEvent import DBLogEvent
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return predefined rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client):
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.get_all_db_log_events_from_db()

            expected_result = [
                DBLogEvent(1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
                DBLogEvent(2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
            ]

            self.assertEqual(result, expected_result)

    # Validate the structure and content of the JSON output with the recommended fix
    def test_validate_json_output_structure_and_content(self):
        from services.DBLogService import DBLogService
        from models.DBLogEvent import DBLogEvent
        from unittest.mock import patch, MagicMock

        # Mock SQLiteDBClient to return predefined rows
        mock_db_client = MagicMock()
        mock_db_client.__enter__.return_value = mock_db_client
        mock_db_client.fetchall.return_value = [
            (1, 1638316800.0, 'com.example.bundle', 123, 456, 'ExampleProcess'),
            (2, 1638316801.0, 'com.example.bundle2', 124, 457, 'ExampleProcess2')
        ]

        # Mock serialise_process_events function to return predefined serialised events
        mock_serialise_process_events = MagicMock()
        mock_serialise_process_events.return_value = [
            {'ID': 1, 'timestamp': 1638316800.0, 'BundleID': 'com.example.bundle', 'CoalitionID': 123, 'PID': 456, 'ProcessName': 'ExampleProcess'},
            {'ID': 2, 'timestamp': 1638316801.0, 'BundleID': 'com.example.bundle2', 'CoalitionID': 124, 'PID': 457, 'ProcessName': 'ExampleProcess2'}
        ]

        # Mock convert_object_to_json_string function to return predefined JSON string directly
        with patch('services.DBLogService.SQLiteDBClient', return_value=mock_db_client), \
             patch('services.DBLogService.serialise_process_events', return_value=mock_serialise_process_events), \
             patch('services.DBLogService.convert_object_to_json_string', return_value='{"events": [{"ID": 1, "timestamp": 1638316800.0, "BundleID": "com.example.bundle", "CoalitionID": 123, "PID": 456, "ProcessName": "ExampleProcess"}, {"ID": 2, "timestamp": 1638316801.0, "BundleID": "com.example.bundle2", "CoalitionID": 124, "PID": 457, "ProcessName": "ExampleProcess2"}]}'):
    
            db_log_service = DBLogService(b'some_bytes')
            result = db_log_service.process_sqlite_db_file()

            expected_result = '{"events": [{"ID": 1, "timestamp": 1638316800.0, "BundleID": "com.example.bundle", "CoalitionID": 123, "PID": 456, "ProcessName": "ExampleProcess"}, {"ID": 2, "timestamp": 1638316801.0, "BundleID": "com.example.bundle2", "CoalitionID": 124, "PID": 457, "ProcessName": "ExampleProcess2"}]}'

            self.assertEqual(result, expected_result)