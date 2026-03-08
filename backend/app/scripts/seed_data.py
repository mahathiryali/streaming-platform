import requests
import os
from app.database import SessionLocal
from app.models import Content
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def seed_videos():
    db = SessionLocal()

    url = "https://api.pexels.com/videos/search?query=nature&per_page=10"
    headers = {"Authorization": PEXELS_API_KEY}
    
    response = requests.get(url, headers=headers)
    data = response.json()

    for video in data["videos"]:
        video_url = video["video_files"][0]["link"]
        thumbnail = video["image"]

        exists = db.query(Content).filter(Content.title == f"Nature {video['id']}").first()

        if not exists:
            new_video = Content(
                title=f"Nature Clip {video['id']}",
                description="A beautiful nature scene from Pexels.",
                video_url=video_url,
                thumbnail_url=thumbnail,
                duration_seconds=video['duration']
            )
            db.add(new_video)
    
    db.commit()
    db.close()
    print("Seeded Videos")

if __name__ == "__main__":
    seed_videos()