import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

# 1. Setup Logging - This keeps track of what the scraper is doing
logging.basicConfig(
    filename='logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. Load Secret Keys
load_dotenv()
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# List of channels 
channels = [
    '@CheMed123', 
    '@lobelia4cosmetics', 
    '@tikvahpharma',
    '@EPHARM_Medical',
    '@Doctor_Addis',
    '@Tena_Ethiopia'
]

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        logging.info("Connected to Telegram successfully.")
        
        for channel in channels:
            logging.info(f"Starting to scrape {channel}")
            
            # Use today's date for the folder name (Partitioning)
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            # Path for JSON and Photos as requested
            json_dir = f'data/raw/telegram_messages/{date_str}'
            img_dir = f'data/raw/images/{channel.replace("@", "")}'
            
            os.makedirs(json_dir, exist_ok=True)
            os.makedirs(img_dir, exist_ok=True)

            messages_data = []

            try:
                async for message in client.iter_messages(channel, limit=100):
                    media_path = None
                    # 3. Download Images into the organized folder
                    if message.photo:
                        media_path = f"{img_dir}/{message.id}.jpg"
                        await client.download_media(message.photo, media_path)

                    # 4. Prepare data structure
                    msg_info = {
                        "message_id": message.id,
                        "channel_name": channel,
                        "message_date": str(message.date),
                        "message_text": message.text,
                        "views": message.views,
                        "forwards": message.forwards,
                        "image_path": media_path
                    }
                    messages_data.append(msg_info)

                # 5. Save as a JSON file in the partitioned directory
                json_file_path = f"{json_dir}/{channel.replace('@', '')}.json"
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(messages_data, f, indent=4, ensure_ascii=False)
                
                logging.info(f"Successfully saved data for {channel}")

            except Exception as e:
                logging.error(f"Error scraping {channel}: {e}")

        print("Task 1 Complete! Check your 'data' and 'logs' folders.")

import asyncio
asyncio.run(main())