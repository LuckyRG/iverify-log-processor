import unittest
from unittest.mock import patch

from consts.LogTextFile import NUMBER_OF_COLUMNS_IN_TXT_PROCESS_LOG_TXT_FILE, PROCESS_LOG_TXT_FILE_DELIMITER_REGEX
from models.TxtLogEvent import TxtLogEvent
from utils.TxtConverter import convert_txt_row_to_txt_log_event, map_row_parts_to_txt_log_event

# Unit test class
class TestTxtConverter(unittest.TestCase):
    def test_convert_txt_row_to_txt_log_event_success(self):
        with (
            # Place any mocks that are required for this test in here
            patch('utils.TxtConverter.map_row_parts_to_txt_log_event') as mock_map_row_parts_to_txt_log_event,
        ):
            test_txt_row_string = "test_user                 1   PRSNA_1 1     1  1   1.0  1.0   1  1        1      1 1        1  1s    9:00PM   0:00.00 test_command"
            test_num_of_columns = NUMBER_OF_COLUMNS_IN_TXT_PROCESS_LOG_TXT_FILE
            test_delimeter_regex = PROCESS_LOG_TXT_FILE_DELIMITER_REGEX

            test_txt_log_event: TxtLogEvent | None = TxtLogEvent(
                "test_user",         
                1,
                "PRSNA_1",
                1,
                1,      
                "1", 
                1.0,  
                1.0 , 
                1,
                1,    
                1,     
                1,  
                "1",   
                "1",  
                "1s" ,
                "9:00PM",
                "0:00.00",
                "test_command"
            )
            
            mock_map_row_parts_to_txt_log_event.return_value = test_txt_log_event

            result: TxtLogEvent | None = convert_txt_row_to_txt_log_event(
                test_txt_row_string, 
                test_num_of_columns,
                test_delimeter_regex
            )

            self.assertEqual(result, test_txt_log_event)


    def test_convert_txt_row_to_txt_log_event_fail(self):
        with (
            # Place any mocks that are required for this test in here
            patch('utils.TxtConverter.map_row_parts_to_txt_log_event') as mock_map_row_parts_to_txt_log_event,
        ): 
            test_txt_row_string = "invalid log row string"
            test_num_of_columns = NUMBER_OF_COLUMNS_IN_TXT_PROCESS_LOG_TXT_FILE
            test_delimeter_regex = PROCESS_LOG_TXT_FILE_DELIMITER_REGEX

            test_txt_log_event: TxtLogEvent | None = None
            
            mock_map_row_parts_to_txt_log_event.return_value = test_txt_log_event

            result: TxtLogEvent | None = convert_txt_row_to_txt_log_event(
                test_txt_row_string, 
                test_num_of_columns,
                test_delimeter_regex
            )

            self.assertEqual(result, None)


    def test_map_row_parts_to_txt_log_event_success(self):
        test_txt_row_string = "test_user                 1   PRSNA_1 1     1  1   1.0  1.0   1  1        1      1 -        1  1s    9:00PM   0:00.00 test_command"
        test_txt_row_parts = ['test_user', '1', 'PRSNA_1', '1', '1', '1', '1.0', '1.0', '1', '1', '1', '1', '1', '1', '1s', '9:00PM', '0:00.00', 'test_command']
        test_num_of_columns = NUMBER_OF_COLUMNS_IN_TXT_PROCESS_LOG_TXT_FILE

        test_expected_result: TxtLogEvent = TxtLogEvent(
            "test_user",         
            1,
            "PRSNA_1",
            1,
            1,      
            "1", 
            1.0,  
            1.0 , 
            1,
            1,    
            1,     
            1,  
            "1",   
            "1",  
            "1s" ,
            "9:00PM",
            "0:00.00",
            "test_command"
        )
        
        result: TxtLogEvent | None = map_row_parts_to_txt_log_event(
            test_txt_row_string, 
            test_txt_row_parts,
            test_num_of_columns
        )

        self.assertEqual(result, test_expected_result)

    def test_map_row_parts_to_txt_log_event_fail(self):
        test_txt_row_string = "test_user                 1   PRSNA_1 1     1  1   1.0  1.0   1  1        1      1 -        1  1s    9:00PM   0:00.00 test_command"
        test_txt_row_parts = ['test_user', '1', 'PRSNA_1', '1', '1', '1', '1.0', '1.0', '1', '1', '1', '1', '1', '1', '1s', '9:00PM', '0:00.00', 'test_command']
        test_incorrect_num_of_columns = 12
        
        result: TxtLogEvent | None = map_row_parts_to_txt_log_event(
            test_txt_row_string, 
            test_txt_row_parts,
            test_incorrect_num_of_columns
        )

        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
