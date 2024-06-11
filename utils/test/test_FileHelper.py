import unittest
from unittest.mock import mock_open, patch

from utils.FileHelper import find_file_path, write_to_json_file

# Unit test class
class TestFileHelper(unittest.TestCase):
    def test_find_file_path_found(self):
        pathList = ['/path/to/file1.txt', '/another/path/file2.log', '/yet/another/path/file3.txt']
        fileNameRegExp = r'file2\.log'
        
        result = find_file_path(pathList, fileNameRegExp)
        
        self.assertEqual(result, '/another/path/file2.log')
    
    def test_find_file_path_not_found(self):
        pathList = ['/path/to/file1.txt', '/another/path/file2.log', '/yet/another/path/file3.txt']
        fileNameRegExp = r'file4\.log'
        
        result = find_file_path(pathList, fileNameRegExp)
        
        self.assertIsNone(result)
    
    def test_find_file_path_case_insensitive(self):
        pathList = ['/path/to/FiLe1.txt', '/another/path/file2.log', '/yet/another/path/file3.txt']
        fileNameRegExp = r'file1\.txt'
        
        result = find_file_path(pathList, fileNameRegExp)
        
        self.assertEqual(result, '/path/to/FiLe1.txt')

class TestWriteToJsonFile(unittest.TestCase):
    def test_write_to_json_file(self):
        json_string = '{"key": "value"}'
        file_name = 'test.json'
        
        with patch('builtins.open', new_callable=mock_open) as mock_open_instance:
            write_to_json_file(json_string, file_name)
            
            mock_open_instance.assert_called_once_with(file_name, 'w')
            mock_open_instance().write.assert_called_once_with(json_string)
            mock_open_instance().close.assert_called_once()

if __name__ == '__main__':
    unittest.main()