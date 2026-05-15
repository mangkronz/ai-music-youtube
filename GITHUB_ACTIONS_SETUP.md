# 🚀 GitHub Actions Automation Setup (ฟรี 100%!)

## 📋 **ความเป็นมา**

```
Python Script: youtube_automation.py
GitHub Actions: ทำให้รัน automatic ทุกวัน 20:00

ฟรี + ไม่ต้องเสียตัง + ทำได้ทั้งวัน
```

---

## 🎯 **ขั้นตอน Setup (5 นาที)**

### **Step 1: สร้าง GitHub Repository**

```
1. ไปที่ https://github.com/new
2. Repository name: "ai-music-youtube"
3. Public ✓ (ต้องเพื่อให้ Actions เข้าถึงได้)
4. Create repository
```

---

### **Step 2: Clone Repository ลงเครื่อง**

```bash
git clone https://github.com/YOUR_USERNAME/ai-music-youtube.git
cd ai-music-youtube
```

---

### **Step 3: สร้าง Folder & Files**

```bash
# สร้าง folders
mkdir -p .github/workflows
mkdir output

# Copy files:
# - youtube_automation.py (root folder)
# - .github/workflows/automation.yml (ใน .github/workflows/)
```

---

### **Step 4: สร้าง Secrets (API Keys)**

```
ไปที่ GitHub:
1. Settings → Secrets and variables → Actions
2. Create new secret

ต้องสร้าง 3 secrets:
```

#### **Secret 1: OPENAI_API_KEY**
```
ไป https://platform.openai.com/api-keys
Copy API key
Paste ใน GitHub Secrets
```

#### **Secret 2: YOUTUBE_API_KEY**
```
ไป https://console.cloud.google.com
1. Create project: "AI Music YouTube"
2. Enable: YouTube Data API v3
3. Create credential: OAuth 2.0 Desktop app
4. Download JSON
5. Copy API key → GitHub Secrets

หรือใช้ API key ตัวเดียว (ได้)
```

#### **Secret 3: YOUTUBE_CHANNEL_ID**
```
ไปที่ YouTube channel เธอ
ตรง "About" → Copy Channel ID
Paste ใน GitHub Secrets
```

---

### **Step 5: Push Code ขึ้น GitHub**

```bash
# Setup git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Add files
git add .
git commit -m "Initial AI Music Automation setup"
git push origin main
```

---

### **Step 6: Enable Actions**

```
GitHub:
1. Go to Actions tab
2. Enable GitHub Actions
3. Workflow should appear: "Daily AI Music Automation"
```

---

### **Step 7: Test Run**

```
1. Click Workflows → "Daily AI Music Automation"
2. Click "Run workflow" → "Run workflow"
3. Wait for it to complete
4. Check "Artifacts" for output files
```

---

## 🎯 **File Structure**

```
ai-music-youtube/
├── youtube_automation.py          ← Main script
├── .github/
│   └── workflows/
│       └── automation.yml         ← GitHub Actions config
├── output/                        ← Generated files
│   ├── image_*.png
│   ├── music_*.mp3
│   ├── video_*.mp4
│   └── youtube_metadata.json
└── README.md
```

---

## ⏰ **Schedule ตั้งเวลา**

**Default: ทุกวัน 20:00 (Bangkok time)**

```yaml
# ใน automation.yml
cron: '0 13 * * *'
# 13:00 UTC = 20:00 Bangkok (UTC+7)
```

**ถ้าอยากเปลี่ยนเวลา:**

```
Cron format: minute hour day month weekday

Examples:
- '0 6 * * *'   = 6:00 AM ทุกวัน
- '0 12 * * *'  = 12:00 PM ทุกวัน
- '0 20 * * *'  = 8:00 PM ทุกวัน
- '0 13 * * 1'  = 8:00 PM ทุกวันจันทร์
```

---

## 🔧 **Troubleshoot**

### **Problem: "Workflow failed"**
```
Solutions:
1. Check if ffmpeg installed
2. Check if API keys correct
3. View "Logs" ใน Actions
```

### **Problem: "OPENAI_API_KEY not found"**
```
Solutions:
1. Check Secrets ถูกไหม
2. Check Secret name: OPENAI_API_KEY (case sensitive)
3. Re-create secret
```

### **Problem: "ffmpeg not found"**
```
Workflow จะ install ffmpeg อัตโนมัติ
ถ้าไม่ได้ ให้ check logs
```

### **Problem: "YouTube upload failed"**
```
Solutions:
1. Check YOUTUBE_CHANNEL_ID
2. Check quota limits
3. Use OAuth2 properly
```

---

## 💾 **Output Files**

```
GitHub Actions จะสร้าง:
├── image_YYYYMMDD_HHMMSS.png     ← DALL-E image
├── music_YYYYMMDD_HHMMSS.mp3     ← Music file
├── video_YYYYMMDD_HHMMSS.mp4     ← Final video
└── youtube_metadata.json          ← YouTube info

ทั้งหมด save ใน Artifacts
Download ได้จาก GitHub Actions page
```

---

## 📊 **ค่าใช้จ่าย**

```
GitHub: ฟรี
Python: ฟรี
GitHub Actions: 2000 free minutes/month ✅
OpenAI (DALL-E): ~$0.080/image = ~$2.4/month
YouTube: ฟรี

━━━━━━━━━━━━━━━
รวม: ~$2-3/month
```

---

## ✅ **เสร็จแล้ว!**

```
1. Workflow ตั้งค่าเสร็จ
2. Automate ทุกวัน 20:00
3. ดูผล ใน Artifacts
4. Download & Upload YouTube ด้วยมือ (ฟรี)
   หรือ ตั้ง YouTube API OAuth2 (ยุ่งกว่า)
```

---

## 🚀 **Next Steps**

### **ถ้าอยากให้ Upload YouTube เองโดยอัตโนมัติ:**

```
ต้องใช้ YouTube API OAuth2
ยุ่งกว่า แต่ได้ผล 100%

บอกผมถ้าต้องการ! 👉
```

### **ถ้าอยากเพิ่มเติม:**

```
- Slack notification
- Email notification
- Multiple concepts rotation
- Custom music API (Suno)
```

---

## 📞 **Contact**

```
GitHub Issues: ถ้า error
Logs: ที่ Actions → Workflow
Help: Ask me! 👉
```

---

## 💡 **Pro Tips**

```
1. Test ด้วย "Run workflow" ก่อน
2. Check logs ทุกครั้ง
3. Download artifacts เพื่อตรวจสอบ
4. Commit message ให้ชัดเจน
```

---

**Ready?** Let's automate! 🚀
