import re
from typing import List, Optional
from models.TxtLogEvent import TxtLogEvent

def convert_txt_row_to_txt_log_event(txt_row: str, num_of_columns: int, delimiter_regex: str) -> Optional[TxtLogEvent]:
    if not txt_row:
      print('TxtConverter - convert_txt_row_to_txt_log_event - ', 
            'Cannot parse row - empty string given')
      return None
    else:
        # Strip leading and trailing whitespaces from row string, if any
        txt_row_stripped: str = txt_row.strip()

        # The last column ("COMMAND") may have multiple instances of the delimiter in it (i.e. multiple whitespaces), 
        # Limit the max number of splits to avoid splitting this column value
        max_number_of_splits: int = num_of_columns - 1

        # Split row string by specified delimiter, the specified amount of times
        row_parts: List[str] = re.split(delimiter_regex, txt_row_stripped, max_number_of_splits)

        mapped_txt_log_event: TxtLogEvent | None = map_row_parts_to_txt_log_event(txt_row, row_parts, num_of_columns)

        return mapped_txt_log_event

        
def map_row_parts_to_txt_log_event(row_string:str, row_parts: List[str], num_of_columns: int) -> Optional[TxtLogEvent]:
    try:
        # Ensure we have the correct number of parts (columns), raise an error otherwise (caught below)
        if len(row_parts) != num_of_columns:
            error_message: str = (
                'Row does not have expected number of Columns (expected: ' + 
                str(num_of_columns) + ', recieved: ' + str(len(row_parts))
            )
            raise Exception(error_message)
            
        # Map column values to correct data types (initially, all values will be strings from txt file row)
        # Assuming the order of columns in the text file is correct for all rows
        user_value = row_parts[0]            
        uid_value = int(row_parts[1])  
        prsna_value = row_parts[2]
        pid_value = int(row_parts[3])
        ppid_value = int(row_parts[4])  
        f_value = row_parts[5] if row_parts[5] else None
        cpu_value = float(row_parts[6]) if row_parts[6] else None  
        mem_value = float(row_parts[7]) if row_parts[7] else None  
        pri_value = int(row_parts[8]) if row_parts[8] else None
        ni_value = int(row_parts[9]) if row_parts[9] else None  
        vsz_value = int(row_parts[10]) if row_parts[10] else None   
        rss_value = int(row_parts[11]) if row_parts[11] else None  
        wchan_value = row_parts[12] if row_parts[12] else None   
        tt_value = row_parts[13] if row_parts[13] else None   
        stat_value = row_parts[14] if row_parts[14] else None  
        started_value = row_parts[15] if row_parts[15] else None    
        time_value = row_parts[16] if row_parts[16] else None 
        command_value = row_parts[17] if row_parts[17] else None

        # Create new TxtLogEvent from mapped data values
        process_log_item_from_row: TxtLogEvent = TxtLogEvent(
            user_value,
            uid_value,
            prsna_value,
            pid_value,
            ppid_value,
            f_value,
            cpu_value,
            mem_value,
            pri_value,
            ni_value,
            vsz_value,
            rss_value,
            wchan_value,
            tt_value,
            stat_value,
            started_value,
            time_value,
            command_value
        )

        return process_log_item_from_row
    except Exception as convert_row_to_process_log_item_error:
        print('TxtConverter - map_row_parts_to_process_item - ',
              'Error parsing row: ', row_string, ' - Error: ', convert_row_to_process_log_item_error)
        return None