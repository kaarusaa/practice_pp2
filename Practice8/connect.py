import psycopg2
from config import DB_CONFIG

def get_connection():
    """Connect to the PostgreSQL database server using DB_CONFIG."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # print("Connected to PostgreSQL server.")
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print("Connection error:", error)
        return None