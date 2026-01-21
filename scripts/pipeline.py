from dagster import op, job, schedule, Config
import subprocess

# --- Define the Operations (Ops) ---

@op
def scrape_telegram_data():
    """Step 1: Scrape data from Telegram"""
    subprocess.run(["python", "src/scraper.py"], check=True)

@op(ins={"start": None}) # Needs scraper to finish first
def load_raw_to_postgres(start):
    """Step 2: Upload raw JSON/CSV to Database"""
    subprocess.run(["python", "src/upload_raw.py"], check=True)

@op(ins={"start": None})
def run_yolo_enrichment(start):
    """Step 3: Run AI Object Detection on images"""
    subprocess.run(["python", "src/yolo_detect.py"], check=True)
    subprocess.run(["python", "src/upload_detections.py"], check=True)

@op(ins={"start_raw": None, "start_ai": None})
def run_dbt_transformations(start_raw, start_ai):
    """Step 4: Run dbt to clean and join everything"""
    subprocess.run(["dbt", "run"], check=True)

# --- Create the Job (The Graph) ---

@job
def medical_warehouse_pipeline():
    # 1. Start Scraper
    scraped = scrape_telegram_data()
    
    # 2. Load Raw and Run AI (These can happen at the same time!)
    raw_loaded = load_raw_to_postgres(scraped)
    ai_loaded = run_yolo_enrichment(scraped)
    
    # 3. Final Step: Run dbt only after BOTH loads are finished
    run_dbt_transformations(start_raw=raw_loaded, start_ai=ai_loaded)
@schedule(cron_schedule="0 0 * * *", job=medical_warehouse_pipeline, execution_timezone="UTC")
def daily_medical_update_schedule():
    return {}