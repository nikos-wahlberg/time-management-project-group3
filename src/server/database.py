# server/database.py
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from key_vault import get_database_credentials

class DatabasePool:
    def __init__(self):
        self._pool = None

    def initialize(self):
        """Initializes the connection pool once when the app starts."""

        creds = get_database_credentials()
        host = creds["host"]
        db_name = creds["database"]
        user = creds["user"]
        password = creds["password"]
        port = creds["port"]

        self._pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=5,
            host=host,
            database=db_name,
            user=user,
            password=password,
            port=port,
            sslmode="require"
        )

    @contextmanager
    def get_cursor(self):
        """
        Yields a cursor from a pooled connection.
        Automatically commits on success and rolls back on failure.
        """
        if self._pool is None:
            self.initialize()
            
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                yield cur
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self._pool.putconn(conn)

db = DatabasePool()