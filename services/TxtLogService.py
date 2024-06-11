from typing import IO, List, Optional

from consts.LogTextFile import NUMBER_OF_COLUMNS_IN_TXT_PROCESS_LOG_TXT_FILE, PROCESS_LOG_TXT_FILE_DELIMITER_REGEX
from models.TxtLogEvent import TxtLogEvent
from utils.FileHelper import write_to_json_file
from utils.JsonHelper import convert_object_to_json_string, serialise_process_log_items
from utils.TimeHelper import get_current_timestamp_utc
from utils.TxtConverter import convert_txt_row_to_txt_log_event


def process_txt_file(txt_file: IO[bytes]) -> Optional[str]:
    try:
        # skip first line in txt file (header row)
        next(txt_file)
        
        # read file to convert to bytes
        txt_file_bytes: bytes = txt_file.read()

        # decode txt file bytes to string
        txt_file_bytes_decoded: str = txt_file_bytes.decode('utf-8')

        # split txt file into lines -> treat each new line as a separate row
        txt_file_lines: List[str] = txt_file_bytes_decoded.splitlines()

        txt_log_events: List[TxtLogEvent] = []

        for txt_file_row in txt_file_lines:        
            txt_log_event: TxtLogEvent | None = convert_txt_row_to_txt_log_event(
                txt_file_row, 
                NUMBER_OF_COLUMNS_IN_TXT_PROCESS_LOG_TXT_FILE, 
                PROCESS_LOG_TXT_FILE_DELIMITER_REGEX
            )
            
            if txt_log_event:
                txt_log_events.append(txt_log_event)
        
        # Make JSON-serialisable array of the TxtLogEvent dataclass array
        txt_log_events_serialisable: List[dict[str, TxtLogEvent]] | None = (
            serialise_process_log_items(txt_log_events)
        )

        # Convert serialised txt log events list to JSON
        txt_log_events_json = convert_object_to_json_string(txt_log_events_serialisable, 2)

        return txt_log_events_json
    except Exception as process_txt_file_error:
        print('Error processing text file: ', process_txt_file_error)
        return None

def write_txt_results_to_file(results_json_string: str, result_output_path: str, file_name: str):
    # Build result file name (append current timestamp to make unique)
    resulting_json_file_name: str = (
        result_output_path + '/' + file_name + 
        '_' + get_current_timestamp_utc() + '.json'
    )
    
    try:
        # Write JSON file to disk
        write_to_json_file(results_json_string, resulting_json_file_name)

        print('Successfully wrote txt log file results to JSON file')
    except Exception as file_write_excpetion:
        print(
            'TxtLogService - Error writing results file: ', 
            file_write_excpetion
        )