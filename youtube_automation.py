#!/usr/bin/env python3
import os
import json
from datetime import datetime
from PIL import Image, ImageDraw
import subprocess
import sys

CONCEPTS = [
    {"id": 1, "title": "เช้านี้ที่ออฟฟิศ", "english": "Morning at the Office", "genre": "Lo-fi", "mood": "Relaxing", "tempo": 75, "description": "เพลง Lo-fi สำหรับคนทำงาน", "target": "คนทำงาน", "color": "#FFD700"},
    {"id": 2, "title": "ฝันดีนะเพื่อน", "english": "Goodnight, My Friend", "genre": "Lo-fi", "mood": "Relaxing", "tempo": 75, "description": "เพลง Lo-fi ที่อบอุ่นสำหรับมิตรภาพ", "target": "มิตรภาพ", "color": "#FF69B4"},
    {"id": 3, "title": "เพื่อนคู่ใจยามอ่านหนังสือ", "english": "Study Buddy", "genre": "Chill", "mood": "Relaxing", "tempo": 75, "description": "เพลง Chill สำหรับนักศึกษา", "target": "นักศึกษา", "color": "#87CEEB"},
    {"id": 4, "title": "เดินไปตามทาง", "english": "Walking Through The City", "genre": "Chill", "mood": "Relaxing", "tempo": 85, "description": "เพลง Chill สำหรับเดินเล่น", "target": "คนเดินเล่น", "color": "#FF8C00"}
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def get_todays_concept():
    day = datetime.now().day
    return CONCEPTS[day % len(CONCEPTS)]

def create_placeholder_image(concept):
    log(f"🎨 Creating image...")
    try:
        width, height = 1024, 576
        img = Image.new('RGB', (width, height), color=concept['color'])
        draw = ImageDraw.Draw(img)
        try:
            title_text = concept['title']
            english_text = concept['english']
            info_text = f"{concept['genre']} • {concept['mood']}"
            draw.text((width//2, height//3), title_text, fill=(255,255,255), anchor="mm")
            draw.text((width//2, height//2), english_text, fill=(255,255,255), anchor="mm")
            draw.text((width//2, (height*2)//3), info_text, fill=(255,255,255), anchor="mm")
        except:
            pass
        os.makedirs("output", exist_ok=True)
        image_file = f"output/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(image_file)
        log(f"✅ Image created: {image_file}")
        return image_file
    except Exception as e:
        log(f"❌ Image error: {e}")
        return None

def create_music_file():
    log("🎵 Creating music...")
    os.makedirs("output", exist_ok=True)
    music_file = f"output/music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    try:
        cmd = ["ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "600", "-q:a", "9", "-acodec", "libmp3lame", "-y", music_file]
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        log(f"✅ Music created: {music_file}")
        return music_file
    except Exception as e:
        log(f"❌ Music error: {e}")
        return None

def create_video(image_file, music_file):
    log(f"🎬 Creating video...")
    if not image_file or not music_file:
        log("❌ Missing files")
        return None
    os.makedirs("output", exist_ok=True)
    video_file = f"output/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    try:
        cmd = ["ffmpeg", "-loop", "1", "-i", image_file, "-i", music_file, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", "-y", video_file]
        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        log(f"✅ Video created: {video_file}")
        return video_file
    except Exception as e:
        log(f"❌ Video error: {e}")
        return None

def generate_caption(concept):
    caption = f"""{concept['title']} | {concept['english']}

{concept['description']}

🎵 Genre: {concept['genre']}
🎯 Perfect for: {concept['target']}
⏱️ Duration: 10 minutes
📊 Tempo: {concept['tempo']} BPM

{'✨ Best for studying, working, and relaxation' if concept['genre'] == 'Lo-fi' else '✨ Chill vibes for everyday life'}

━━━━━━━━━━━━━━━━━━
📌 Subscribe for more music!
🎧 Turn on notifications
🔗 Enjoy and relax
━━━━━━━━━━━━━━━━━━

#{concept['title'].replace(' ', '')} #lofimusic #chillbeats #studymusic #relaxingmusic #backgroundmusic #{concept['target'].replace(' ', '')}"""
    return caption

def save_metadata(video_file, concept, caption):
    log(f"💾 Saving metadata...")
    try:
        metadata = {"title": concept['title'], "description": caption, "tags": ["lofi", "chillbeats", "studymusic"], "categoryId": "10", "privacyStatus": "public", "video_file": video_file, "created_at": datetime.now().isoformat()}
        with open("output/youtube_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        log(f"✅ Metadata saved")
        return True
    except Exception as e:
        log(f"❌ Metadata error: {e}")
        return False

def main():
    log("🚀 Starting AI Music Automation")
    log(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    concept = get_todays_concept()
    log(f"🎵 Concept: {concept['title']}")
    image_file = create_placeholder_image(concept)
    if not image_file:
        log("❌ Failed to create image")
        return False
    music_file = create_music_file()
    if not music_file:
        log("❌ Failed to create music")
        return False
    video_file = create_video(image_file, music_file)
    if not video_file:
        log("❌ Failed to create video")
        return False
    caption = generate_caption(concept)
    if not save_metadata(video_file, concept, caption):
        log("⚠️ Failed to save metadata")
    log("✨ Automation complete!")
    log(f"📁 Files: output/")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ Fatal error: {e}")
        sys.exit(1)
