import psycopg2
from key_vault import get_database_credentials


def get_database_connection():
    try:
        host, database, user, password, *_ = get_database_credentials()
        return psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password, 
            sslmode="require"
        )
    except Exception as e:
        print(e)

