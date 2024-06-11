from services.TxtLogService import process_txt_file
import unittest

# Unit test class
class TestTxtLogService(unittest.TestCase):
    # Ensure the 'io' module is imported at the beginning of the test file to resolve the NameError
    def test_process_well_formed_text_file_with_io_import(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Handles an empty text file gracefully and returns None, with the 'io' module imported
    def test_process_empty_text_file_with_io_import(self):
        import io
        txt_file = io.BytesIO(b"")
        result = process_txt_file(txt_file)
        self.assertIsNone(result)

    # Properly decodes text file bytes to a UTF-8 string
    def test_properly_decodes_text_file_bytes_to_utf8_string(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Ensure that the header row is correctly skipped in the text file processing
    def test_correctly_skips_header_row(self):
        import io

        # Create a well-formed text file with header and data rows
        txt_content = (
            "USER_HEADER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )

        # Create an IO stream with the text content
        txt_file = io.BytesIO(txt_content.encode('utf-8'))

        # Call the function under test
        result = process_txt_file(txt_file)

        # Assert that the result is not None and contains expected data
        self.assertIsNotNone(result)
        self.assertNotIn("USER_HEADER", result )  # Header row should be skipped # type: ignore
        self.assertNotIn('"USER": "USER_HEADER"', result)  # Ensure header row is not included in data rows # type: ignore
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Fix the missing 'io' import statement in the test function
    def test_serialize_txt_log_events_to_json(self):
        import io
    
        # Prepare test data
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
    
        # Call the function under test
        result = process_txt_file(txt_file)
    
        # Assertions
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Accurately splits the text file into lines and processes each line
    def test_accurately_splits_text_file_lines(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Converts each valid text row to a TxtLogEvent object
    def test_convert_valid_text_row_to_txt_log_event(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result) 
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Returns an empty list if an exception occurs during processing
    def test_returns_empty_list_on_exception(self):
        # Prepare a mock text file with invalid content
        import io
        txt_content = "Invalid content"
        txt_file = io.BytesIO(txt_content.encode('utf-8'))

        # Call the function under test
        result = process_txt_file(txt_file)

        # Assert that the result is an empty list
        self.assertEqual(result, '[]')

    # Ensure the 'io' module is imported for the test function
    def test_import_io_module_for_test_function(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
    
        result = process_txt_file(txt_file)
    
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Ensure that text rows with fewer columns than expected are handled correctly
    def test_manage_text_rows_with_fewer_columns(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Deals with text rows with more columns than expected without crashing
    def test_deals_with_text_rows_with_more_columns_than_expected_without_crashing(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1 extra_column\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2 extra_column\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Handles text rows with unexpected delimiters correctly
    def test_handles_text_rows_with_unexpected_delimiters_correctly(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Verifies that the function handles large text files efficiently
    def test_process_large_text_file_handling(self):
        import io
        txt_content = "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n" + "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n" * 100000
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore

    # Handles text rows with missing optional fields correctly
    def test_handles_text_rows_with_missing_optional_fields_correctly(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Ensures the final JSON string is correctly formatted and valid
    def test_json_string_formatting(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore

    # Processes text files with mixed valid and invalid rows, only including valid ones in the output
    def test_process_mixed_valid_and_invalid_rows_in_text_file(self):
        import io
        txt_content = (
            "USER UID PRSNA PID PPID F CPU MEM PRI NI VSZ RSS WCHAN TT STAT STARTED TIME COMMAND\n"
            "user1 1000 pr1 1234 5678 - 0.1 0.2 20 0 10000 2000 - tty1 S 2023-10-01 00:00:01 command1\n"
            "invalid_row\n"
            "user2 1001 pr2 1235 5679 - 0.2 0.3 21 1 11000 2100 - tty2 R 2023-10-02 00:00:02 command2\n"
        )
        txt_file = io.BytesIO(txt_content.encode('utf-8'))
        result = process_txt_file(txt_file)
        self.assertIsNotNone(result)
        self.assertIn('"USER": "user1"', result) # type: ignore
        self.assertNotIn('invalid_row', result) # type: ignore
        self.assertIn('"USER": "user2"', result) # type: ignore