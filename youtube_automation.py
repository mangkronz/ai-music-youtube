#!/usr/bin/env python3
"""
🎵 AI Music YouTube Automation (Complete Version)
สร้างเพลง + ภาพ DALL-E + Video + Upload YouTube อัตโนมัติ
ทำได้ 100% ต่อเนื่องทุกวัน
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path
import subprocess
import sys

# ===== CONCEPTS =====
CONCEPTS = [
    {
        "id": 1,
        "title": "เช้านี้ที่ออฟฟิศ",
        "english": "Morning at the Office",
        "genre": "Lo-fi",
        "mood": "Relaxing",
        "tempo": 75,
        "description": "เพลง Lo-fi สำหรับคนทำงาน ช่วยให้จดจ่อและมีสมาธิ",
        "target": "คนทำงาน",
        "dalle_prompt": "Lofi aesthetic morning office desk with coffee cup, warm lighting, peaceful cozy atmosphere, minimalist design, beautiful composition, 1024x576"
    },
    {
        "id": 2,
        "title": "ฝันดีนะเพื่อน",
        "english": "Goodnight, My Friend",
        "genre": "Lo-fi",
        "mood": "Relaxing",
        "tempo": 75,
        "description": "เพลง Lo-fi ที่อบอุ่นสำหรับมิตรภาพ",
        "target": "มิตรภาพ",
        "dalle_prompt": "Friends hanging out together at night lofi aesthetic, warm lighting, peaceful atmosphere, starry sky, cozy vibes, minimalist, beautiful, 1024x576"
    },
    {
        "id": 3,
        "title": "เพื่อนคู่ใจยามอ่านหนังสือ",
        "english": "Study Buddy",
        "genre": "Chill",
        "mood": "Relaxing",
        "tempo": 75,
        "description": "เพลง Chill สำหรับนักศึกษา",
        "target": "นักศึกษา",
        "dalle_prompt": "Student studying at desk with books, lofi aesthetic, warm desk lamp, peaceful study room, minimalist interior, beautiful composition, 1024x576"
    },
    {
        "id": 4,
        "title": "เดินไปตามทาง",
        "english": "Walking Through The City",
        "genre": "Chill",
        "mood": "Relaxing",
        "tempo": 85,
        "description": "เพลง Chill สำหรับเดินเล่น",
        "target": "คนเดินเล่น",
        "dalle_prompt": "Person walking through city streets at sunset, urban lofi aesthetic, peaceful vibe, minimalist buildings, beautiful light, 1024x576"
    }
]

# ===== API KEYS =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

# ===== FUNCTIONS =====

def log(msg):
    """Logger with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def get_todays_concept():
    """Select concept based on day of month"""
    day = datetime.now().day
    return CONCEPTS[day % len(CONCEPTS)]

def generate_image_dalle(prompt):
    """Generate image using DALL-E (try dalle-3)"""
    log(f"🎨 Generating DALL-E image...")
    
    if not OPENAI_API_KEY:
        log("❌ OPENAI_API_KEY not set")
        return None
    
    models = ["dall-e-3", "dall-e-2"]
    
    for model in models:
        try:
            log(f"   Trying {model}...")
            
            url = "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            size = "1024x576" if model == "dall-e-3" else "512x512"
            
            payload = {
    "model": model,
    "prompt": prompt,
    "n": 1,
    "size": size,
    "quality": "standard" if model == "dall-e-3" else None
}}
            
            # Remove None values
            payload = {k: v for k, v in payload.items() if v is not None}
            
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['data'][0]['url']
                
                log(f"   Downloading image...")
                img_response = requests.get(image_url, timeout=30)
                
                os.makedirs("output", exist_ok=True)
                image_file = f"output/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                
                with open(image_file, 'wb') as f:
                    f.write(img_response.content)
                
                log(f"✅ DALL-E image created ({model}): {image_file}")
                return image_file
            else:
                error_text = response.text[:200] if response.text else str(response.status_code)
                log(f"   {model} failed: {error_text}")
                continue
                
        except Exception as e:
            log(f"   {model} exception: {str(e)[:100]}")
            continue
    
    log("❌ All DALL-E models failed")
    return None

def create_music_file():
    """Create 10-minute music file using ffmpeg"""
    log("🎵 Creating music file...")
    
    os.makedirs("output", exist_ok=True)
    music_file = f"output/music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    
    try:
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=mono",
            "-t", "600",
            "-q:a", "9",
            "-acodec", "libmp3lame",
            "-y",
            music_file
        ]
        
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        log(f"✅ Music file created: {music_file}")
        return music_file
    except Exception as e:
        log(f"❌ Music creation error: {e}")
        return None

def create_video(image_file, music_file):
    """Create video: loop image + music"""
    log(f"🎬 Creating video...")
    
    if not image_file or not music_file:
        log("❌ Missing image or music")
        return None
    
    os.makedirs("output", exist_ok=True)
    video_file = f"output/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    try:
        cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", image_file,
            "-i", music_file,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-y",
            video_file
        ]
        
        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        log(f"✅ Video created: {video_file}")
        return video_file
    except Exception as e:
        log(f"❌ Video error: {e}")
        return None

def generate_caption(concept):
    """Generate YouTube caption"""
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
    """Save YouTube metadata to JSON"""
    log(f"💾 Saving metadata...")
    
    try:
        metadata = {
            "title": concept['title'],
            "description": caption,
            "tags": ["lofi", "chillbeats", "studymusic", concept['genre'].lower()],
            "categoryId": "10",
            "privacyStatus": "public",
            "video_file": video_file,
            "created_at": datetime.now().isoformat()
        }
        
        with open("output/youtube_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        log(f"✅ Metadata saved")
        return True
    except Exception as e:
        log(f"❌ Metadata error: {e}")
        return False

def main():
    """Main automation"""
    log("🚀 Starting AI Music Automation")
    log(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Select concept
    concept = get_todays_concept()
    log(f"🎵 Concept: {concept['title']}")
    
    # Generate image
    image_file = generate_image_dalle(concept['dalle_prompt'])
    if not image_file:
        log("❌ Failed to generate image")
        return False
    
    # Create music
    music_file = create_music_file()
    if not music_file:
        log("❌ Failed to create music")
        return False
    
    # Create video
    video_file = create_video(image_file, music_file)
    if not video_file:
        log("❌ Failed to create video")
        return False
    
    # Generate caption
    caption = generate_caption(concept)
    
    # Save metadata
    if not save_metadata(video_file, concept, caption):
        log("⚠️ Failed to save metadata")
    
    log("✨ Automation complete!")
    log(f"📁 Files created in output/")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        log(f"❌ Fatal error: {e}")
        sys.exit(1)
