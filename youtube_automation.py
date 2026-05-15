#!/usr/bin/env python3
import os
import json
import requests
import time
from datetime import datetime
from PIL import Image, ImageDraw
import subprocess
import sys

CONCEPTS = [
    {"id": 1, "title": "เช้านี้ที่ออฟฟิศ", "english": "Morning at the Office", "genre": "Lo-fi", "mood": "Relaxing", "tempo": 75, "description": "เพลง Lo-fi สำหรับคนทำงาน", "target": "คนทำงาน", "color": "#FFD700", "prompt": "lofi hip hop beat, calm, relaxing, office background, 10 minutes"},
    {"id": 2, "title": "ฝันดีนะเพื่อน", "english": "Goodnight, My Friend", "genre": "Lo-fi", "mood": "Relaxing", "tempo": 75, "description": "เพลง Lo-fi ที่อบอุ่นสำหรับมิตรภาพ", "target": "มิตรภาพ", "color": "#FF69B4", "prompt": "lofi chill beat, night vibes, relaxing, cozy, 10 minutes"},
    {"id": 3, "title": "เพื่อนคู่ใจยามอ่านหนังสือ", "english": "Study Buddy", "genre": "Chill", "mood": "Relaxing", "tempo": 75, "description": "เพลง Chill สำหรับนักศึกษา", "target": "นักศึกษา", "color": "#87CEEB", "prompt": "study music, chill beats, focus, relaxing, 10 minutes"},
    {"id": 4, "title": "เดินไปตามทาง", "english": "Walking Through The City", "genre": "Chill", "mood": "Relaxing", "tempo": 85, "description": "เพลง Chill สำหรับเดินเล่น", "target": "คนเดินเล่น", "color": "#FF8C00", "prompt": "chill urban beat, city vibes, relaxing, walk music, 10 minutes"}
]

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

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
            draw.text((width//2, height//3), concept['title'], fill=(255,255,255), anchor="mm")
            draw.text((width//2, height//2), concept['english'], fill=(255,255,255), anchor="mm")
            draw.text((width//2, (height*2)//3), f"{concept['genre']} • {concept['mood']}", fill=(255,255,255), anchor="mm")
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

def generate_music_replicate(prompt):
    log(f"🎵 Generating music with Replicate...")
    
    if not REPLICATE_API_TOKEN:
        log("⚠️ REPLICATE_API_TOKEN not set")
        return None
    
    try:
        # Use Stable Audio model from Replicate
        url = "https://api.replicate.com/v1/predictions"
        headers = {"Authorization": f"Token {REPLICATE_API_TOKEN}"}
        
        data = {
            "version": "8cf61d529ac03c4b9d628ff412f050e5",  # Stable Audio
            "input": {
                "prompt": prompt,
                "duration": 600  # 10 minutes
            }
        }
        
        log("   Sending request to Replicate...")
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code not in [200, 201]:
            log(f"⚠️ Replicate error: {response.status_code}")
            return None
        
        prediction = response.json()
        prediction_id = prediction.get('id')
        log(f"   Prediction ID: {prediction_id}")
        
        # Poll for completion
        max_retries = 60
        for i in range(max_retries):
            log(f"   Checking status... ({i+1}/{max_retries})")
            
            status_response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=headers,
                timeout=30
            )
            
            if status_response.status_code != 200:
                log(f"⚠️ Status check failed: {status_response.status_code}")
                return None
            
            status = status_response.json()
            
            if status['status'] == 'succeeded':
                output_url = status.get('output')
                if output_url:
                    log(f"✅ Music generated: {output_url}")
                    
                    # Download music
                    music_response = requests.get(output_url, timeout=60)
                    os.makedirs("output", exist_ok=True)
                    music_file = f"output/music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                    
                    with open(music_file, 'wb') as f:
                        f.write(music_response.content)
                    
                    log(f"✅ Music downloaded: {music_file}")
                    return music_file
                else:
                    log("⚠️ No output URL")
                    return None
            
            elif status['status'] == 'failed':
                log(f"❌ Music generation failed: {status.get('error')}")
                return None
            
            # Wait before next check
            time.sleep(5)
        
        log("❌ Music generation timeout")
        return None
        
    except Exception as e:
        log(f"❌ Replicate error: {e}")
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
    log("🚀 Starting AI Music Automation with Replicate")
    log(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    concept = get_todays_concept()
    log(f"🎵 Concept: {concept['title']}")
    
    # Create image
    image_file = create_placeholder_image(concept)
    if not image_file:
        log("❌ Failed to create image")
        return False
    
    # Generate music
    music_file = generate_music_replicate(concept['prompt'])
    if not music_file:
        log("❌ Failed to generate music")
        return False
    
    # Create video
    video_file = create_video(image_file, music_file)
    if not video_file:
        log("❌ Failed to create video")
        return False
    
    # Save metadata
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
