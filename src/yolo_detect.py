import os
import pandas as pd
from ultralytics import YOLO

# 1. Load the model
model = YOLO('yolov8n.pt')

# 2. Path to your main photos folder
base_image_folder = 'data/raw/images' 
results_list = []

print("Starting deep search for images...")

# 3. os.walk goes into every subfolder automatically
for root, dirs, files in os.walk(base_image_folder):
    for filename in files:
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # Get the full path so the AI can find the file
            img_path = os.path.join(root, filename)
            
            print(f"Analyzing: {img_path}")
            results = model(img_path)
            
            has_person = False
            has_product = False
            max_conf = 0
            detected_names = []

            for r in results:
                for box in r.boxes:
                    label = model.names[int(box.cls)]
                    conf = float(box.conf)
                    detected_names.append(label)
                    if conf > max_conf: max_conf = conf
                    if label == 'person': has_person = True
                    if label in ['bottle', 'cup', 'vase', 'bowl']: has_product = True

            if has_person and has_product: cat = 'promotional'
            elif has_product: cat = 'product_display'
            elif has_person: cat = 'lifestyle'
            else: cat = 'other'

            # We use the filename (message_id) to join with our database later
            results_list.append({
                'message_id': filename.split('.')[0], 
                'detected_class': ", ".join(set(detected_names)),
                'confidence_score': max_conf,
                'image_category': cat
            })

# 4. Save results
if results_list:
    df = pd.DataFrame(results_list)
    df.to_csv('data/detection_results.csv', index=False)
    print(f"Success! Analyzed {len(results_list)} images.")
else:
    print("Zero images found. Double check that data/photos contains subfolders with images.")