import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')

try:
    connection = psycopg2.connect(database_url)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")