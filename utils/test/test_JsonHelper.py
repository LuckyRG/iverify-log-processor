import unittest
from unittest.mock import patch
import json

from models.DBLogEvent import DBLogEvent
from models.TxtLogEvent import TxtLogEvent
from utils.JsonHelper import convert_object_to_json_string, serialise_process_events, serialise_process_log_items

# Unit test class
class TestJsonHelper(unittest.TestCase):
    def test_serialise_process_events_success(self):
        events = [
            DBLogEvent(ID=1, timestamp=1625563200.0, BundleID="com.example", CoalitionID=42, PID=1234, ProcessName="example_process"),
            DBLogEvent(ID=2, timestamp=None, BundleID=None, CoalitionID=None, PID=None, ProcessName=None)
        ]
        expected_result = [
            {
                'ID': 1,
                'timestamp': 1625563200.0,
                'BundleID': 'com.example',
                'CoalitionID': 42,
                'PID': 1234,
                'ProcessName': 'example_process'
            },
            {
                'ID': 2,
                'timestamp': None,
                'BundleID': None,
                'CoalitionID': None,
                'PID': None,
                'ProcessName': None
            }
        ]
        result = serialise_process_events(events)
        self.assertEqual(result, expected_result)

    def test_serialise_process_events_empty_list(self):
        events = []
        expected_result = []
        result = serialise_process_events(events)
        self.assertEqual(result, expected_result)

    def test_serialise_process_events_error(self):
        with patch('dataclasses.asdict', side_effect=Exception('Test Exception')):
            events = [DBLogEvent(ID=1, timestamp=1625563200.0, BundleID="com.example", CoalitionID=42, PID=1234, ProcessName="example_process")]
            result = serialise_process_events(events)
            self.assertIsNone(result)

    def test_serialise_process_log_items_success(self):
        logs = [
            TxtLogEvent(USER="user1", UID=1001, PRSNA="example", PID=1234, PPID=5678, F=None, CPU=12.5, MEM=45.6, PRI=20, NI=0, VSZ=2048, RSS=1024, WCHAN=None, TT="tt", STAT="R", STARTED="12:00", TIME="0:01", COMMAND="command"),
            TxtLogEvent(USER="user2", UID=1002, PRSNA="example2", PID=1235, PPID=5679, F=None, CPU=None, MEM=None, PRI=None, NI=None, VSZ=None, RSS=None, WCHAN=None, TT=None, STAT=None, STARTED=None, TIME=None, COMMAND=None)
        ]
        expected_result = [
            {
                'USER': 'user1',
                'UID': 1001,
                'PRSNA': 'example',
                'PID': 1234,
                'PPID': 5678,
                'F': None,
                'CPU': 12.5,
                'MEM': 45.6,
                'PRI': 20,
                'NI': 0,
                'VSZ': 2048,
                'RSS': 1024,
                'WCHAN': None,
                'TT': 'tt',
                'STAT': 'R',
                'STARTED': '12:00',
                'TIME': '0:01',
                'COMMAND': 'command'
            },
            {
                'USER': 'user2',
                'UID': 1002,
                'PRSNA': 'example2',
                'PID': 1235,
                'PPID': 5679,
                'F': None,
                'CPU': None,
                'MEM': None,
                'PRI': None,
                'NI': None,
                'VSZ': None,
                'RSS': None,
                'WCHAN': None,
                'TT': None,
                'STAT': None,
                'STARTED': None,
                'TIME': None,
                'COMMAND': None
            }
        ]
        result = serialise_process_log_items(logs)
        self.assertEqual(result, expected_result)

    def test_serialise_process_log_items_empty_list(self):
        logs = []
        expected_result = []
        result = serialise_process_log_items(logs)
        self.assertEqual(result, expected_result)

    def test_serialise_process_log_items_error(self):
        with patch('dataclasses.asdict', side_effect=Exception('Test Exception')):
            logs = [TxtLogEvent(USER="user1", UID=1001, PRSNA="example", PID=1234, PPID=5678, F=None, CPU=12.5, MEM=45.6, PRI=20, NI=0, VSZ=2048, RSS=1024, WCHAN=None, TT="tt", STAT="R", STARTED="12:00", TIME="0:01", COMMAND="command")]
            result = serialise_process_log_items(logs)
            self.assertIsNone(result)

    def test_convert_object_to_json_string_success(self):
        obj = {'key': 'value', 'list': [1, 2, 3]}
        expected_result = json.dumps(obj, indent=4)
        result = convert_object_to_json_string(obj, indent=4)
        self.assertEqual(result, expected_result)

    def test_convert_object_to_json_string_error(self):
        obj = {'key': 'value', 'list': [1, 2, 3]}
        with patch('json.dumps', side_effect=Exception('Test Exception')):
            result = convert_object_to_json_string(obj, indent=4)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()