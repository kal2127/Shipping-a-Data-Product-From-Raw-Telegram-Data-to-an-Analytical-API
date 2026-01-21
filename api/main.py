from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
from . import schemas
from typing import List

app = FastAPI(title="Medical Data Warehouse API")

@app.get("/")
def home():
    return {"message": "Welcome to the Medical Warehouse API!"}

# Endpoint 1: Top Products
@app.get("/api/reports/top-products", response_model=List[schemas.ProductStats])
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    query = text("SELECT term, mention_count FROM marts.mart_medical_trends LIMIT :limit")
    result = db.execute(query, {"limit": limit})
    return [{"term": r[0], "mention_count": r[1]} for r in result]

# Endpoint 2: Channel Activity
@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT date_key, COUNT(*) as post_count 
        FROM staging.fct_messages m
        JOIN staging.dim_channels c ON m.channel_key = c.channel_key
        WHERE c.channel_title = :name
        GROUP BY date_key ORDER BY date_key DESC
    """)
    result = db.execute(query, {"name": channel_name})
    return [{"date": str(r[0]), "post_count": r[1]} for r in result]

# Endpoint 3: Message Search
@app.get("/api/search/messages", response_model=List[schemas.MessageResult])
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    sql = text("""
        SELECT message_id, channel_key, message_text, view_count 
        FROM staging.fct_messages 
        WHERE message_text ILIKE :search LIMIT :limit
    """)
    result = db.execute(sql, {"search": f"%{query}%", "limit": limit})
    return [{"message_id": str(r[0]), "channel_title": r[1], "text": r[2], "view_count": r[3]} for r in result]

# Endpoint 4: Visual Content Stats
@app.get("/api/reports/visual-content", response_model=List[schemas.VisualStats])
def get_visual_stats(db: Session = Depends(get_db)):
    query = text("""
        SELECT image_category, COUNT(*) as total_count, AVG(view_count) as avg_views
        FROM staging.fct_image_detections
        GROUP BY image_category
    """)
    result = db.execute(query)
    return [{"image_category": r[0], "total_count": r[1], "avg_views": float(r[2])} for r in result]