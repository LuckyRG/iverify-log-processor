from typing import Any, List, Optional, Self

from models.DBLogEvent import DBLogEvent
from clients.SQLiteDBClient import SQLiteDBClient
from consts.SQLiteDB import QUERY_ALL_DATA_FROM_PROCESS_EVENT_TABLE
from utils.FileHelper import write_to_json_file
from utils.JsonHelper import convert_object_to_json_string, serialise_process_events
from utils.TimeHelper import get_current_timestamp_utc


class DBLogService:
    def __init__(self, sqlite_db_file_bytes: bytes):
        self._sqlite_db = sqlite_db_file_bytes

    @property
    def sqlite_db(self: Self):
        return self._sqlite_db

    def get_all_db_log_events_from_db(self: Self) -> List[DBLogEvent]:    
        db_log_event_rows: List[Any] = []
        db_log_events: List[DBLogEvent] = []

        try:
            # Define new SQLite DB Client
            # Client automatcially handles connection and cursor lifecycle when using "with" block
            with SQLiteDBClient(':memory:') as db_client:        
                db_client.deserialise(self.sqlite_db)

                db_client.execute(QUERY_ALL_DATA_FROM_PROCESS_EVENT_TABLE)

                db_log_event_rows = db_client.fetchall()

            for db_log_event_row in db_log_event_rows:
                # Map result rows to DBLogEvent data class
                process_event: DBLogEvent = DBLogEvent(*db_log_event_row)

                db_log_events.append(process_event)
        except Exception as retrieve_process_events_from_db_error:
            print(
                'DBLogService - Error retrieving process events from DB: ', 
                retrieve_process_events_from_db_error
            )
        
        return db_log_events
    
    
    def process_sqlite_db_file(self: Self) -> Optional[str]:
        # Retrieve all db log events from SQLite DB Table
        db_log_events: List[DBLogEvent] = []
        db_log_events = self.get_all_db_log_events_from_db()

        if db_log_events:
            # Serialise log event list to make it JSON-friendly
            db_log_events_serialisable: List[dict[str, DBLogEvent]] | None = (
                serialise_process_events(db_log_events)
            )

            if db_log_events_serialisable:
                # Convert serialised process events list to JSON
                db_log_events_json: str | None = convert_object_to_json_string(db_log_events_serialisable, 2)

                return db_log_events_json
        else:
            print('Could not retrieve process events from DB table, or none present')
            return None


    def write_db_results_to_file(self: Self, results_json_string: str, result_output_path: str, file_name: str):
        # Build result file name (append current timestamp to make unique)
        resulting_json_file_name: str = (
            result_output_path + '/' + file_name + 
            '_' + get_current_timestamp_utc() + '.json'
        )
        
        try:
            # Write JSON file to disk
            write_to_json_file(results_json_string, resulting_json_file_name)

            print('Successfully wrote SQLite DB log file results to JSON file')
        except Exception as file_write_excpetion:
            print(
                'DBLogService - Error writing results file: ', 
                file_write_excpetion
            )
