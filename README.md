# 🖐️ Hand Finger Counter Using MediaPipe

A real-time Python application that uses **MediaPipe** and **OpenCV** to detect hands from a webcam feed, count the number of raised fingers, and display the result live.

---

## 💡 Features

- Real-time hand detection using MediaPipe  
- Finger counting for both left and right hands  
- Displays:
  - Individual hand count (Left/Right)
  - Total fingers raised  
- Supports single or dual hand input  
- Annotated live video feed  

---

## 📂 Output

- Live webcam feed with:
  - Finger count near each detected hand
  - Total finger count at the top-left corner  

---

## 🛠️ Requirements

- Python 3.x  
- OpenCV  
- MediaPipe  

Install dependencies using:

```bash
pip install opencv-python mediapipe
```

---

## ▶️ How to Run

- Ensure your webcam is connected
- Run the Python script:
```bash
python #HAND_FINGER_COUNTER.py
```
- Press ESC key to exit

---

## 🔍 Logic Used

- Uses MediaPipe’s 21 hand landmarks
- Thumb logic differs for left and right hands (based on x-coordinate)
- Other fingers checked using y-coordinates of tip vs lower joint
- Counts are updated live per frame

---
