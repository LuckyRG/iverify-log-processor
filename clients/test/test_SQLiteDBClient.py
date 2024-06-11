import unittest
from clients.SQLiteDBClient import SQLiteDBClient
import sqlite3

# Unit test class
class TestSQLiteDBClient(unittest.TestCase):
    # Initialize SQLiteDBClient with a valid database name
    def test_initialize_with_valid_db_name(self):
        db_name = ":memory:"  # Using an in-memory database for testing
        client = SQLiteDBClient(db_name)
        self.assertIsNotNone(client.connection)
        self.assertIsNotNone(client.cursor)
        client.close()

    # Initialize SQLiteDBClient with an invalid database name
    def test_initialize_with_invalid_db_name(self):
        invalid_db_name = "/invalid/path/to/db.sqlite"
        with self.assertRaises(sqlite3.OperationalError):
            SQLiteDBClient(invalid_db_name)

    # Execute a valid SQL query and fetch results
    def test_execute_valid_sql_query(self):
        db_name = ":memory:"
        client = SQLiteDBClient(db_name)
        client.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        client.execute("INSERT INTO test_table (name) VALUES (?)", ("John",))
        client.commit()
        client.execute("SELECT * FROM test_table")
        results = client.fetchall()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "John")
        client.close()

    # Commit changes to the database
    def test_commit_changes_to_db(self):
        db_name = ":memory:"
        client = SQLiteDBClient(db_name)
        client.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        client.execute("INSERT INTO test_table (name) VALUES (?)", ("Jane",))
        client.commit()
        client.execute("SELECT * FROM test_table")
        results = client.fetchall()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Jane")
        client.close()

    # Close the connection and cursor properly
    def test_close_connection_and_cursor(self):
        db_name = ":memory:"
        client = SQLiteDBClient(db_name)
        client.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            client.execute("SELECT * FROM test_table")

    # Use SQLiteDBClient within a context manager
    def test_use_sqlite_db_client_within_context_manager(self):
        db_name = ":memory:"  # Using an in-memory database for testing
        with SQLiteDBClient(db_name) as client:
            self.assertIsNotNone(client.connection)
            self.assertIsNotNone(client.cursor)

    # Execute an invalid SQL query
    def test_execute_invalid_sql_query(self):
        with self.assertRaises(sqlite3.OperationalError):
            with SQLiteDBClient(":memory:") as client:
                client.execute("SELECT * FROM non_existing_table")
                client.fetchall()

    # Handle exceptions during database operations
    def test_handle_exceptions_during_db_operations(self):
        with self.assertRaises(Exception):
            with SQLiteDBClient(":memory:") as client:
                client.execute("SELECT * FROM non_existing_table")

    # Close the connection without committing changes
    def test_close_connection_without_commit(self):
        db_name = ":memory:"  # Using an in-memory database for testing
        client = SQLiteDBClient(db_name)
        client.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        client.execute("INSERT INTO test_table (name) VALUES ('test')")
        client.close(commit=False)
        with self.assertRaises(sqlite3.ProgrammingError):
            client.execute("SELECT * FROM test_table")

    # Test the properties connection and cursor for correct instances
    def test_properties_connection_and_cursor(self):
        db_name = ":memory:"  # Using an in-memory database for testing
        client = SQLiteDBClient(db_name)
        self.assertIsInstance(client.connection, sqlite3.Connection)
        self.assertIsInstance(client.cursor, sqlite3.Cursor)
        client.close()

    # Verify the commit method actually commits changes
    def test_commit_method_commits_changes(self):
        db_name = ":memory:"  # Using an in-memory database for testing
        client = SQLiteDBClient(db_name)
        client.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        client.execute("INSERT INTO test_table (name) VALUES (?)", ("Alice",))
        client.commit()
        client.execute("SELECT * FROM test_table")
        result = client.fetchall()
        self.assertEqual(len(result), 1)
        client.close()

    # Execute SQL queries with and without parameters
    def test_execute_sql_queries(self):
        db_name = ":memory:"  # Using an in-memory database for testing
        client = SQLiteDBClient(db_name)
    
        # Test executing SQL query without parameters
        client.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        client.execute("INSERT INTO test_table (name) VALUES ('Alice')")
        client.execute("INSERT INTO test_table (name) VALUES ('Bob')")
        client.execute("SELECT * FROM test_table")
        result = client.fetchall()
        self.assertEqual(len(result), 2)
    
        # Test executing SQL query with parameters
        client.execute("SELECT * FROM test_table WHERE name=?", ('Alice',))
        result = client.fetchall()
        self.assertEqual(len(result), 1)
    
        client.close()