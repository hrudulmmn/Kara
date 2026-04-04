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

## 📹 Demo Video (plays directly on GitHub)
<video width="100%" controls>
  <source src="https://github.com/hrudulmmn/Kara/releases/tag/Demo_vid" type="video/mp4">
  Your browser does not support the video tag.
</video>

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