import dataclasses
import json
from typing import Any, List, Optional

from models.DBLogEvent import DBLogEvent
from models.TxtLogEvent import TxtLogEvent

def serialise_process_events(process_events: List[DBLogEvent]) -> Optional[List[dict[str, DBLogEvent]]]:
    process_events_serialisable: List[dict[str, DBLogEvent]] = []
    
    try:
        if process_events:
            process_events_serialisable = (
                [dataclasses.asdict(process_event) for process_event in process_events]
            )

        return process_events_serialisable
    except Exception as serialise_process_events_error:
        print('Error serialising process events object: ', serialise_process_events_error)
        return None
    


def serialise_process_log_items(process_log_items: List[TxtLogEvent]) -> Optional[List[dict[str, TxtLogEvent]]]:
    process_log_items_serialisable: List[dict[str, TxtLogEvent]] = []
    
    try:
        if process_log_items:
            process_log_items_serialisable = (
                [dataclasses.asdict(process_log_item) for process_log_item in process_log_items]
            )
        
        return process_log_items_serialisable
    except Exception as serialise_process_log_items_error:
        print('Error serialising process log items object: ', serialise_process_log_items_error)
        return None


def convert_object_to_json_string(object: Any, indent: int) -> Optional[str]:
    try:
        return json.dumps(object, indent=indent)
    except Exception as json_dumps_error:
        print('Error converting object to JSON string: ', json_dumps_error)
        return None