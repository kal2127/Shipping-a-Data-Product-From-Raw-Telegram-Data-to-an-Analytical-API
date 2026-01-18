import os
import json
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

# 1. Load database credentials from your .env
load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'medical_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'your_password')

def load_data():
    # 2. Connect to PostgreSQL
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()

    # 3. Create the 'raw' schema and table
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            message_id BIGINT,
            channel_name TEXT,
            message_date TIMESTAMP,
            message_text TEXT,
            views INTEGER,
            forwards INTEGER,
            image_path TEXT
        );
    """)
    conn.commit()

    # 4. Find all JSON files in your data lake
    base_path = 'data/raw/telegram_messages'
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 5. Insert data into the table
                    for msg in data:
                        cur.execute("""
                            INSERT INTO raw.telegram_messages 
                            (message_id, channel_name, message_date, message_text, views, forwards, image_path)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                            msg['message_id'], msg['channel_name'], msg['message_date'],
                            msg['message_text'], msg['views'], msg['forwards'], msg['image_path']
                        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Success! Raw data loaded to PostgreSQL.")

if __name__ == "__main__":
    load_data()