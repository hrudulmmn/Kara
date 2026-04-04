# Kara – Gesture-Based PDF Viewer with AI Summarization

**Hands-free PDF reading with gesture control + real-time Groq AI summarization**

Built for distraction-free study sessions and accessibility.

## 🎯 Key Results
- Reduced false gesture triggers by **~70%**
- Maintained **~60 FPS** with multi-threaded processing
- Swipe navigation + pinch-to-zoom
- Real-time AI summarization via Groq

## ✨ Features
- Gesture navigation (swipe, pinch, point)
- Instant AI page summarization
- Smooth PyQt6 desktop UI
- Fully multi-threaded (zero lag)

## 🛠️ Tech Stack
- Python, OpenCV + MediaPipe, PyMuPDF, Groq API, PyQt6

## 📹 Demo Video 
**Watch the full demo** → [Kara Demo Video (Release)](https://github.com/hrudulmmn/Kara/releases/download/Demo_vid/Kara.demo.1.mp4)

## 📂 Project Structure
```
Kara/
├── main.py
├── gesture.py
├── render.py
├── summarise.py
├── Ui.py
├── Kara demo.mp4
└── Design.qss
```

## 🚀 Quick Start
```bash
git clone https://github.com/hrudulmmn/Kara.git
cd Kara
pip install -r requirements.txt
python main.py