import psycopg2
from psycopg2 import DatabaseError
from .config import config


def connect():
    """Connect to the PostgreSQL database and return the connection."""
    try:
        return psycopg2.connect(**config())
    except (Exception, DatabaseError) as error:
        print("DB connection error:", error)
        return None