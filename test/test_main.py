import unittest
from consts.FileProcessing import MAX_INPUT_TAR_FILE_SIZE_BYTES
from main import process_tar_file
import argparse

class TestMain(unittest.TestCase):
    # Exits app with an error message if the input TAR file size exceeds 400MB
    def test_input_tar_file_size_exceeds_400mb(self):
        from unittest.mock import patch

        with patch('os.path.getsize', return_value=MAX_INPUT_TAR_FILE_SIZE_BYTES + 1):
            with self.assertRaises(SystemExit) as cm:
                process_tar_file('dummy_input.tar.gz', 'dummy_output')
        
            self.assertEqual(cm.exception.code, 'Input TAR file size exceeds max allowed size of 400MB.')

    # Check for the correct exit message on empty TAR file
    def test_empty_tar_file(self):
        from unittest.mock import patch

        with patch('sys.exit') as mock_sys_exit:
            with patch('os.path.exists', side_effect=[True, True]):
                with patch('os.path.getsize', return_value=100):
                    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(input='dummy_input.tar.gz', output='invalid_output')):
                        with patch('tarfile.open') as mock_tarfile_open:
                            mock_tarfile_open.return_value.__enter__.return_value.getmembers.return_value = []
                            mock_tarfile_open.return_value.__enter__.return_value.__iter__.return_value = iter([])
                            process_tar_file('dummy_input.tar.gz', 'invalid_output')
                            mock_sys_exit.assert_called_once_with('Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')

    # Handles the case where ps.txt file is not found in the TAR archive
    def test_ps_txt_file_not_found_in_tar(self):
        from unittest.mock import patch, MagicMock

        # Mock the tarfile and its contents
        mock_tarfile = MagicMock()
        mock_tarfile.__enter__.return_value = mock_tarfile
        mock_tarfile.getnames.return_value = ['powerlog.PLSQL']
        mock_tarfile.extractfile.return_value = None

        with patch('tarfile.open', return_value=mock_tarfile):
            with patch('os.path.getsize', return_value=100):
                with patch('services.DBLogService.DBLogService.process_sqlite_db_file', return_value='{"db_log_events": []}'):
                    with patch('services.DBLogService.DBLogService.write_db_results_to_file'):
                        with self.assertRaises(SystemExit) as cm:
                            process_tar_file('dummy_input.tar.gz', 'dummy_output')

                        self.assertEqual(str(cm.exception), 'Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')

    # Test ps.txt file extraction error
    def test_ps_txt_file_extraction_failure(self):
        from unittest.mock import patch, MagicMock

        # Mock the tarfile and its contents
        mock_tarfile = MagicMock()
        mock_tarfile.__enter__.return_value = mock_tarfile
        mock_tarfile.getnames.return_value = ['powerlog.PLSQL']
        mock_tarfile.extractfile.return_value = None

        with patch('tarfile.open', return_value=mock_tarfile):
            with patch('os.path.getsize', return_value=100):
                with patch('services.DBLogService.DBLogService.process_sqlite_db_file', return_value='{"db_log_events": []}'):
                    with patch('services.DBLogService.DBLogService.write_db_results_to_file'):
                        with self.assertRaises(SystemExit) as cm:
                            process_tar_file('dummy_input.tar.gz', 'dummy_output')

                        self.assertEqual(str(cm.exception), 'Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')


    # Powerlog PLSQL file is not found in the TAR archive - exit with the correct message
    def test_powerlog_plsql_file_not_found_in_tar(self):
        from unittest import mock
        with mock.patch('os.path.getsize', return_value=1000):
            with mock.patch('tarfile.open') as mock_tar_open:
                mock_tar_open.return_value.__enter__.return_value.extractfile.return_value = None
                with self.assertRaises(SystemExit) as cm:
                    process_tar_file('dummy_input.tar.gz', 'dummy_output')
                self.assertEqual(cm.exception.code, 'Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')

    # Handles exceptions during the processing of ps.txt file
    def test_handles_exceptions_during_processing_ps_txt_file(self):
        from unittest.mock import patch, mock_open
        from unittest.mock import MagicMock

        # Mock the tarfile and its contents
        mock_tarfile = MagicMock()
        mock_tarfile.__enter__.return_value = mock_tarfile
        mock_tarfile.getnames.return_value = ['ps.txt']
        mock_tarfile.extractfile.return_value = mock_open(read_data=b'header\nrow1\nrow2').return_value

        with patch('tarfile.open', return_value=mock_tarfile):
            with patch('os.path.getsize', return_value=100):
                with patch('services.TxtLogService.process_txt_file', side_effect=Exception('Error processing txt file')):
                    with patch('services.TxtLogService.write_txt_results_to_file'):
                        with patch('services.DBLogService.DBLogService.process_sqlite_db_file'):
                            with patch('services.DBLogService.DBLogService.write_db_results_to_file'):
                                with self.assertRaises(SystemExit) as cm:
                                    process_tar_file('dummy_input.tar.gz', 'dummy_output')

                                self.assertEqual(str(cm.exception), 'Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')

    # Powerlog PLSQL file extraction error
    def test_powerlog_plsql_file_extraction_failure(self):
        from unittest.mock import patch, MagicMock

        mock_tarfile = MagicMock()
        mock_tarfile.__enter__.return_value = mock_tarfile
        mock_tarfile.getnames.return_value = ['ps.txt']
        mock_tarfile.extractfile.return_value = None

        with patch('tarfile.open', return_value=mock_tarfile):
            with patch('os.path.getsize', return_value=100):
                with patch('services.TxtLogService.process_txt_file', return_value='{"txt_log_events": []}'):
                    with patch('services.TxtLogService.write_txt_results_to_file') as mock_write_txt:
                        with patch('services.DBLogService.DBLogService.process_sqlite_db_file') as mock_process_sqlite_db:
                            with patch('services.DBLogService.DBLogService.write_db_results_to_file') as mock_write_db:
                                with self.assertRaises(SystemExit) as cm:
                                    process_tar_file('dummy_input.tar.gz', 'dummy_output')
                                self.assertEqual(cm.exception.code, 'Finished parsing log files from TAR. Successful results saved to JSON files in specified directory.')
                                mock_write_txt.assert_not_called()
                                mock_process_sqlite_db.assert_not_called()
                                mock_write_db.assert_not_called()

    # Handling of exceptions during the processing of the powerlog PLSQL file
    def test_handles_exceptions_during_processing_powerlog_plsql_file(self):
        from unittest.mock import patch, mock_open, MagicMock

        # Mock the tarfile and its contents
        mock_tarfile = MagicMock()
        mock_tarfile.__enter__.return_value = mock_tarfile
        mock_tarfile.getnames.return_value = ['ps.txt', 'powerlog.PLSQL']
        mock_tarfile.extractfile.side_effect = [
            mock_open(read_data=b'header\nrow1\nrow2').return_value,
            mock_open(read_data=b'sqlite_db_bytes').return_value
        ]

        with patch('tarfile.open', return_value=mock_tarfile):
            with patch('os.path.getsize', return_value=100):
                with patch('services.TxtLogService.process_txt_file', return_value='{"txt_log_events": []}'):
                    with patch('services.TxtLogService.write_txt_results_to_file') as mock_write_txt:
                        with self.assertRaises(SystemExit) as cm:
                            with patch('services.DBLogService.DBLogService.process_sqlite_db_file', side_effect=Exception('Error processing SQLite DB file')):
                                with patch('services.DBLogService.DBLogService.write_db_results_to_file') as mock_write_db:
                                    process_tar_file('dummy_input.tar.gz', 'dummy_output')

        # Assert that the write functions were not called due to exception
        mock_write_txt.assert_not_called()
        mock_write_db.assert_not_called()