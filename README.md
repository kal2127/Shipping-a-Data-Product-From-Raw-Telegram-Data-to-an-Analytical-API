Shipping a Data Product: From Raw Telegram Data to an Analytical API

This project is part of 10 Academy – Artificial Intelligence Mastery (Week 8 Challenge).
It focuses on building the foundation of a modern ELT data platform by extracting raw Telegram data and transforming it into a clean, analytical data warehouse using dbt and dimensional modeling.

📌 Project Overview

Ethiopian medical and pharmaceutical businesses actively use Telegram to promote products.
However, the data is unstructured and difficult to analyze.

This project builds the core data pipeline that:

Scrapes raw Telegram messages and images

Stores them in a structured data lake

Loads raw data into PostgreSQL

Transforms messy data into a trusted star-schema warehouse using dbt

🎯 Business Questions (Foundation)

The pipeline prepares data to answer:

Which medical products are mentioned most frequently?

Which Telegram channels are most active?

How does engagement (views, forwards) vary by channel?

How does posting activity change over time?

🏗️ Architecture (Tasks 1–2)
Telegram Channels
│
▼
Telegram Scraper (Telethon)
│
▼
Raw Data Lake (JSON + Images)
│
▼
PostgreSQL (Raw Schema)
│
▼
dbt Transformations
(Staging → Star Schema)

📂 Project Structure
medical-telegram-warehouse/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env # Secrets (not committed)
├── README.md
├── data/
│ └── raw/
│ ├── telegram_messages/
│ │ └── YYYY-MM-DD/
│ │ └── channel_name.json
│ └── images/
│ └── channel_name/
│ └── message_id.jpg
├── medical_warehouse/ # dbt project
│ ├── dbt_project.yml
│ ├── profiles.yml
│ ├── models/
│ │ ├── staging/
│ │ └── marts/
│ └── tests/
├── src/
│ ├── scraper.py
│ └── load_to_postgres.py
└── tests/

🔍 Data Sources

Public Telegram channels related to Ethiopian medical businesses:

CheMed – Medical products

Lobelia Cosmetics – Cosmetics and health products

Tikvah Pharma – Pharmaceuticals

Additional channels from https://et.tgstat.com/medicine

⚙️ Technologies Used (Tasks 1–2)
Category Tools
Data Extraction Telethon
Raw Storage JSON Data Lake
Database PostgreSQL
Transformation dbt
Data Modeling Star Schema (Kimball)
Containerization Docker
🧪 Task 1: Data Scraping & Collection (Extract & Load)
Objective

Extract messages and images from public Telegram channels and store them in a raw data lake while preserving the original data structure.

Features

Extracts:

Message ID

Channel name

Timestamp

Message text

Views and forwards

Media availability

Downloads images when available

Stores raw data as partitioned JSON files

Implements logging for traceability

Raw Data Lake Structure
data/raw/telegram_messages/YYYY-MM-DD/channel_name.json
data/raw/images/channel_name/message_id.jpg

Output

Raw JSON files

Downloaded images

Logs of scraping activity

🏗️ Task 2: Data Modeling & Transformation (Transform)
Objective

Transform raw Telegram data into a clean, reliable analytical data warehouse using dbt and dimensional modeling.

Steps Implemented

1. Load Raw Data to PostgreSQL

JSON files are read from the data lake

Data is loaded into a raw schema

Table created: raw.telegram_messages

2. Staging Layer (dbt)

Staging models:

Cast correct data types

Standardize column names

Remove invalid or empty records

Add derived fields such as:

message_length

has_image

Example:

models/staging/stg_telegram_messages.sql

3. Star Schema Design

Dimension Tables

dim_channels

dim_dates

Fact Table

fct_messages

This design supports efficient time-series and channel-based analysis.

4. Data Quality Tests

Primary key uniqueness

Non-null constraints

Referential integrity

Custom tests (e.g., no future-dated messages)

All transformations and tests are executed using:

dbt run
dbt test

📊 Data Warehouse Output

The final warehouse provides:

Clean, trusted analytical tables

Consistent naming and data types

Fully tested datasets ready for APIs and dashboards

🚀 How to Run (Tasks 1–2)
1️⃣ Set Environment Variables

Create a .env file:

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
