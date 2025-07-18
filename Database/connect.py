import mysql.connector
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def ConnectDB():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connect DB success")
        return connection
    
    except mysql.connector.Error as err:
        print(f"Connect DB failed: {err}")
        sys.exit(1)

# Test
if __name__ == "__main__":
    conn = ConnectDB()
    conn.close()