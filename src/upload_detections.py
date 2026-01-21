import pandas as pd
from sqlalchemy import create_engine

# 1. Database Connection (Use the same details as your profiles.yml)
# Format: postgresql://username:password@localhost:5432/dbname
# Since you have no password, leave it empty after the colon
engine = create_engine('postgresql://postgres:@localhost:5432/medical_db')

# 2. Load the CSV we made with YOLO
csv_path = 'data/detection_results.csv'
df = pd.DataFrame()

try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded {len(df)} rows from CSV.")
except Exception as e:
    print(f"Error reading CSV: {e}")

# 3. Push to PostgreSQL
if not df.empty:
    try:
        # We put it in the 'raw' schema so dbt can 'source' it
        df.to_sql('image_detections', engine, schema='raw', if_exists='replace', index=False)
        print("Success! Data loaded to raw.image_detections table.")
    except Exception as e:
        print(f"Error uploading to Postgres: {e}")