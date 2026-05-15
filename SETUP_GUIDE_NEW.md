# 🚀 GitHub Actions Automation Setup Guide

## 📋 **ความเป็นมา**

```
Automate YouTube music upload ทุกวัน 20:00 (Thailand time)
ใช้ DALL-E สร้างภาพ + FFmpeg สร้าง video
ทั้งหมด ฟรี 100% (เกือบ)
```

---

## ✅ **3 ไฟล์ใหม่:**

```
1. youtube_automation.py    ← Python script
2. automation.yml          ← GitHub Actions workflow
3. Setup Guide (นี่!)
```

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Upload Files to GitHub**

```
GitHub Repo → youtube_automation (ที่เธอสร้าง)

Upload:
1. youtube_automation.py (ราก)
2. automation.yml → ใน .github/workflows/ folder

Structure:
ai-music-youtube/
├── youtube_automation.py
├── .github/
│   └── workflows/
│       └── automation.yml
└── output/ (created automatically)
```

---

### **Step 2: ตั้ง API Keys (Secrets)**

ไปที่ GitHub Repo:

```
Settings → Secrets and variables → Actions
```

**สร้าง 1 Secret:**

```
Name: OPENAI_API_KEY
Value: sk-... (API key จาก OpenAI)

Click "Add secret"
```

---

### **Step 3: Test Run**

```
Actions → Workflows → "Daily AI Music Automation"
Click "Run workflow" (ปุ่มเขียว)
```

---

### **Step 4: รอ 5-10 นาที**

```
Workflow จะรัน:
1. Install ffmpeg
2. Generate DALL-E image
3. Create music file
4. Create video
5. Save metadata
6. Upload artifacts
```

---

## 📊 **ผลลัพธ์ที่คาด**

```
✅ Status: Completed
✅ Artifacts folder:
   ├── image_20260515_HHMMSS.png (DALL-E)
   ├── music_20260515_HHMMSS.mp3 (FFmpeg)
   ├── video_20260515_HHMMSS.mp4 (Final)
   └── youtube_metadata.json (Caption)
```

---

## ⏰ **Schedule**

**Default: ทุกวัน 20:00 (8 PM) Bangkok time**

ถ้าต้องเปลี่ยนเวลา แก้ไฟล์ `automation.yml`:

```yaml
# Line 7:
- cron: '0 13 * * *'

# Format: minute hour day month weekday
# Examples:
# - cron: '0 6 * * *'   = 6:00 AM ทุกวัน
# - cron: '0 12 * * *'  = 12:00 PM ทุกวัน
# - cron: '0 20 * * *'  = 8:00 PM ทุกวัน
# - cron: '0 13 * * 1'  = 8:00 PM ทุกวันจันทร์
```

---

## 🔧 **Troubleshoot**

### **Problem: "OPENAI_API_KEY not set"**

```
Solution:
1. Check Secrets มี OPENAI_API_KEY ไหม
2. Taper name ต้องตรงกัน (case sensitive)
3. Re-create secret
```

### **Problem: "DALL-E error: 400"**

```
Solution:
1. ใช้ dalle-2 แทน dalle-3 (script จะลอง dalle-2 อยู่แล้ว)
2. Check OpenAI billing
3. Wait 5-10 นาที แล้ว run ใหม่
```

### **Problem: "ffmpeg not found"**

```
Workflow จะ install ffmpeg อัตโนมัติ
ถ้าไม่ได้ อาจ network issue
```

### **Problem: Workflow ไม่ run

```
Solution:
1. Check "Actions" ใน GitHub
2. ตรวจสอบ schedule เวลา
3. Manual trigger: "Run workflow"
```

---

## 💰 **Cost**

```
GitHub Actions: ฟรี (2000 min/month)
FFmpeg: ฟรี
DALL-E: ~$0.08/image = ~$2.4/month
OpenAI: ~$2-3/month

รวม: ~$2-3/month (ถูกที่สุด!)
```

---

## 📁 **Concepts (4 เพลง)**

Workflow จะสลับเพลงทุกวัน:

```
วันที่ 1, 5, 9, ... → เช้านี้ที่ออฟฟิศ
วันที่ 2, 6, 10, ... → ฝันดีนะเพื่อน
วันที่ 3, 7, 11, ... → เพื่อนคู่ใจยามอ่านหนังสือ
วันที่ 4, 8, 12, ... → เดินไปตามทาง
```

---

## ✨ **เสร็จแล้ว!**

```
✅ Automation ตั้งค่าเสร็จ
✅ ทำงานทุกวัน 20:00
✅ ไฟล์บันทึกใน Artifacts
✅ Download & ดู ได้ทุกวัน
```

---

## 🎯 **Next Steps**

```
1. Upload 2 files ไป GitHub
2. ตั้ง OPENAI_API_KEY secret
3. Test run workflow
4. ดูผล ใน Artifacts
5. Download files
```

---

Good luck! 🚀
