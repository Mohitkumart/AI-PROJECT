
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connections import get_mssql_connection


def test_connection():
    try:
        conn = get_mssql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 * FROM sys.tables")  # Basic test query
        rows = cursor.fetchall()
        print("✅ MSSQL connection successful. Sample data:")
        for row in rows:
            print(row)
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", str(e))

if __name__ == "__main__":
    test_connection()
