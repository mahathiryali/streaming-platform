from google import genai
from google.genai import types
from PIL import Image
import cv2
import requests
import tempfile
from app.database import SessionLocal
from app import models
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")

client = genai.Client(api_key=GENAI_API_KEY)
DATA_FILE = "app/data/processed_videos.json"

def fix_metadata():
    db = SessionLocal()
    videos = db.query(models.Content).all()

    processed_data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            processed_data = json.load(f)
    
    for video in videos:
        if str(video.id) in processed_data:
            print(f"Skipping ID {video.id} - already processed.")
            continue
        print(f"Downloading {video.title} for analysis...")
        
        try:
            r = requests.get(video.video_url, stream=True)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        tmp.write(chunk)
                tmp_path = tmp.name

            cap = cv2.VideoCapture(tmp_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, 2000) # 2 seconds in
            success, frame = cap.read()
            
            if success:
                
                color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(color_converted)
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        "Provide a specific 3-word title and a 1-sentence description. Format: Title: [Title] | Description: [Description]",
                        pil_img
                    ]
                )
                
                raw_text = response.text
                parts = raw_text.split("|")
                title = parts[0].replace("Title:", "").strip()
                description = parts[1].replace("Description:", "").strip()

                processed_data[str(video.id)] = {
                "title": title,
                "description": description,
                "url": video.video_url
            }
                
                print(f"Success! New Title: {video.title}")
                with open(DATA_FILE, "w") as f:
                    json.dump(processed_data, f, indent=4)

                print("Waiting 12 seconds to respect API rate limits...")
                time.sleep(12)
            else:
                print(f"OpenCV failed to read frame from {video.id}")

            cap.release()
            os.remove(tmp_path)

        except Exception as e:
            if "429" in str(e):
                print("Rate limit hit! Sleeping for 60 seconds...")
                time.sleep(60)
            else:
                print(f"Error: {e}")

    db.commit()
    db.close()

if __name__ == "__main__":
    print("Starting metadata update...")
    fix_metadata()
    print("Done!")
