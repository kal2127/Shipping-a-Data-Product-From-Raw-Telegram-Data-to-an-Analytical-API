Medical Telegram Data Warehouse & Analytical API

Shipping a Data Product: From Raw Telegram Data to an Analytical API
10 Academy – Artificial Intelligence Mastery | Week 8 Challenge

📌 Project Overview

Telegram is a major platform used by Ethiopian medical and pharmaceutical businesses to advertise products, share prices, and engage customers. However, this data is unstructured, noisy, and difficult to analyze at scale.

This project builds a modern, end-to-end ELT data platform that transforms raw Telegram messages and images into a trusted analytical data product. The platform enables structured analysis of medical trends, engagement metrics, price-related mentions, and visual marketing behavior.

🎯 Business Objectives & Key Questions

The platform is designed to answer the following business questions:

What are the top 10 most frequently mentioned medical products or drugs across channels?

How do product availability and price-related mentions vary across different channels?

Which Telegram channels rely more on visual content (images vs text)?

Do posts with images or promotional visuals receive higher engagement?

What are the daily and weekly posting trends for medical topics?

🏗️ End-to-End Architecture
Telegram Channels
        │
        ▼
Telethon Scraper (Python)
        │
        ▼
Raw Data Lake (JSON + Images)
        │
        ▼
PostgreSQL (Raw Schema)
        │
        ▼
dbt Transformations
(Staging → Star Schema Marts)
        │
        ▼
YOLOv8 Image Enrichment
        │
        ▼
Analytical API (FastAPI)
        │
        ▼
Dagster Orchestration


This layered design follows modern ELT best practices, ensuring scalability, traceability, and reliability.

📂 Project Structure
medical-telegram-warehouse/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env                      # Secrets (not committed)
├── README.md
├── data/
│   └── raw/
│       ├── telegram_messages/
│       │   └── YYYY-MM-DD/
│       │       └── channel_name.json
│       └── images/
│           └── channel_name/
│               └── message_id.jpg
├── medical_warehouse/        # dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
├── src/
│   ├── scraper.py
│   ├── load_to_postgres.py
│   └── yolo_detect.py
├── api/
│   ├── main.py
│   ├── database.py
│   └── schemas.py
├── pipeline.py               # Dagster pipeline
└── tests/

🔍 Data Sources

Public Telegram channels related to Ethiopian medical businesses:

CheMed – Medical products

Lobelia Cosmetics – Cosmetics and health products

Tikvah Pharma – Pharmaceuticals

Additional channels from https://et.tgstat.com/medicine

⚙️ Technologies Used
Category	Tools
Scraping	Telethon
Storage	JSON Data Lake, PostgreSQL
Transformation	dbt
Modeling	Star Schema (Kimball)
Image Enrichment	YOLOv8 (Ultralytics)
API	FastAPI, SQLAlchemy
Orchestration	Dagster
Containers	Docker & Docker Compose
🧪 Task 1: Data Scraping & Collection (Extract & Load)
Objective

Extract messages and images from Telegram and store them in a structured raw data lake.

Implementation

Telethon was used to scrape public Telegram channels

Extracted fields include:

message_id

channel_name

message_date

message_text

views and forwards

media presence

Images are downloaded when available

Raw Data Lake Design
data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
data/raw/images/channel_name/message_id.jpg

Key Design Choice

Raw data is preserved without transformation, ensuring full data lineage and reusability.

🏗️ Task 2: Data Modeling & Transformation (Transform)
Objective

Convert raw Telegram data into a clean, analytical data warehouse using dbt.

ELT Strategy

Raw data is first loaded into PostgreSQL, then transformed inside the warehouse using dbt.

Staging Layer

Cleans and standardizes raw data:

Type casting (timestamps, integers)

Removal of empty messages

Standardized naming

Derived features:

message_length

has_image

Star Schema Design
Star Schema Diagram
               dim_dates
                   │
                   │
dim_channels ─── fct_messages

Fact Table

fct_messages

message_id

channel_key

date_key

message_text

message_length

view_count

forward_count

has_image

Dimension Tables

dim_channels

channel_name

channel_type

total_posts

avg_views

dim_dates

full_date

day_of_week

month

year

is_weekend

This schema supports:

Time-series analysis

Channel comparisons

Price and product trend analysis

Data Quality & Testing

Implemented dbt tests:

Unique and non-null constraints

Referential integrity

Custom test ensuring view counts are never negative

✅ All tests pass successfully.

🖼️ Task 3: Data Enrichment with Object Detection (YOLO)
Objective

Analyze image content to understand visual marketing strategies.

Approach

YOLOv8 nano model used for efficiency

Objects detected (e.g., person, bottle, container)

Images classified as:

promotional (person + product)

product_display

lifestyle

other

Analytical Value

Compare engagement between image categories

Identify channels that rely heavily on visuals

Challenges & Mitigation

Pre-trained models are not medical-specific

Used proxy objects and rule-based classification to extract value

🌐 Task 4: Analytical API (FastAPI)
Objective

Expose warehouse insights through a REST API.

Example Endpoints

Top mentioned products (including price-related terms)

Channel activity trends

Keyword-based message search

Visual content statistics

Design Decisions

Queries run on dbt mart tables

Pydantic used for schema validation

OpenAPI docs available at /docs

🔄 Task 5: Pipeline Orchestration (Dagster)
Objective

Automate and monitor the entire pipeline.

Dagster Pipeline Steps

Scrape Telegram data

Load raw data into PostgreSQL

Run dbt transformations and tests

Execute YOLO image enrichment

Benefits

Automated daily runs

Clear dependency management

Failure monitoring and logging

Dagster UI:

http://localhost:3000

🚀 How to Run the Project
1️⃣ Set Environment Variables
TELEGRAM_API_ID=your_id
TELEGRAM_API_HASH=your_hash
DB_HOST=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=medical_dw

2️⃣ Run with Docker
docker-compose up --build

3️⃣ Run dbt
cd medical_warehouse
dbt run
dbt test

📈 Key Learnings

Designing scalable ELT pipelines

Dimensional modeling for analytics

Data quality enforcement using dbt

Integrating unstructured image data

Building analytical APIs

Orchestrating pipelines with Dagster

🔮 Future Improvements

NLP for multi-language (Amharic) text

Domain-specific object detection models

Real-time ingestion

Authentication for API access

✅ Final Summary

This project delivers a production-ready data platform that transforms raw Telegram data into a reliable analytical product. By combining Telethon scraping, PostgreSQL storage, dbt transformations, YOLO-based enrichment, FastAPI exposure, and Dagster orchestration, the system fully aligns with modern data engineering best practices and the Week 8 challenge requirements.
