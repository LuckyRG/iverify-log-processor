import argparse
import sys
import os
import tarfile
from typing import IO, List
from pathlib import Path

from consts.FileProcessing import MAX_INPUT_TAR_FILE_SIZE_BYTES, POWERLOG_PLSQL_FILE_NAME_MATCH_PATTERN, PS_TXT_FILE_NAME_MATCH_PATTERN
from services.DBLogService import DBLogService
from services.TxtLogService import process_txt_file, write_txt_results_to_file
from utils.FileHelper import find_file_path

# Creates and returns the ArgumentParser object
def create_arg_parser():
    parser = argparse.ArgumentParser(description='Extract System Diagnostic Files from Given TAR file')
    parser.add_argument('--input', help='Input file path of your diagnostic TAR file')
    parser.add_argument('--output', help='Output directory path for resulting JSON files')
    return parser


def process_tar_file(input_tar_file_path: str, output_results_path: str):
    input_tar_file_size_bytes: int  = os.path.getsize(input_tar_file_path)

    # Safety check for input tar file size
    # If exceeds 400MB, warn and exit
    if input_tar_file_size_bytes > MAX_INPUT_TAR_FILE_SIZE_BYTES:
        sys.exit('Input TAR file size exceeds max allowed size of 400MB.')

    # Open the tar file, but don't extract it yet
    with tarfile.open(input_tar_file_path) as tar_file_obj:
        filePathList: List[str] = []

        for file in tar_file_obj:
            filePath: str = file.name

            filePathList.append(filePath)

        ps_txt_file_path: str | None = find_file_path(filePathList, PS_TXT_FILE_NAME_MATCH_PATTERN)

        if ps_txt_file_path:
            # Get name of file from path, to use for result file
            ps_text_file_name = Path(ps_txt_file_path).stem
            
            # Extract specific "ps.txt" file from this tar
            ps_txt_file: IO[bytes] | None = tar_file_obj.extractfile(ps_txt_file_path)
            
            if ps_txt_file:
                # Process the ps.txt file
                result_json_string: str | None = process_txt_file(ps_txt_file)

                if result_json_string:
                    write_txt_results_to_file(result_json_string, output_results_path, ps_text_file_name)
            else:
                print('Unable to extract ps.txt file from TAR archive.')
        else:
             print('Unable to find ps.txt file in TAR archive.')
    
        powerlog_plsql_file_path: str | None = find_file_path(filePathList, POWERLOG_PLSQL_FILE_NAME_MATCH_PATTERN)

        if powerlog_plsql_file_path:
            # Get name of file from path, to use for result file
            powerlog_plsql_file_name = Path(powerlog_plsql_file_path).stem
            
            # Extract specific "powerlog plsql" SQLite DB file from this tar
            powerlog_sqlite_db_file: IO[bytes] | None = tar_file_obj.extractfile(powerlog_plsql_file_path)
            
            if powerlog_sqlite_db_file:                
                # Make sure refernece point is set to beginning of DB file
                powerlog_sqlite_db_file.seek(0)

                # Read file to turn into bytes stream
                sqlite_db_file_bytes = powerlog_sqlite_db_file.read()

                # Instantiate new DBLogService with SQLite DB file
                process_event_service = DBLogService(sqlite_db_file_bytes)

                # Process the powerlog plsql (SQLite DB) file
                result_json: str | None = process_event_service.process_sqlite_db_file()

                if result_json:
                    # Write result to disk
                    process_event_service.write_db_results_to_file(result_json, output_results_path, powerlog_plsql_file_name)
            else:
                print('Unable to extract powerlog plsqsl file from TAR archive.')
        else:
            print('Unable to find powerlog plsqsl file in TAR archive.') 

        # Close tar file object
        tar_file_obj.close()

        sys.exit('Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    if not parsed_args.input:
        sys.exit('A valid TAR (.tar.gz) file is required as input')

    if not parsed_args.output:
        sys.exit('A valid output directory is required for resulting JSON files output.\nFor example: results-json')
    
    if os.path.exists(parsed_args.input):
        print('Valid input path')
    else:
        sys.exit('A valid TAR (.tar.gz) file is required as input')
    
    if os.path.exists(parsed_args.output):
       print('Valid output path')
    else:
        sys.exit('A valid output directory is required for resulting JSON files output.\nFor example: results-json')
        
    # remove trailing slashes from provided output directory path, if present
    # eg: json-results/ becomes json-results
    cleaned_output_directory_path = parsed_args.output.rstrip('/')
    
    process_tar_file(parsed_args.input, cleaned_output_directory_path)
