🖐️ LIVE FINGER COUNTING WITH MEDIAPIPE

This is a real-time Python application that uses MediaPipe and OpenCV to detect hands from a webcam feed, count the number of raised fingers for each hand, and display the results live with annotations.

💡 FEATURES:
Real-time hand detection using MediaPipe
Accurate finger counting for both left and right hands
Total fingers displayed live on screen
Individual finger count shown near each hand
Works with one or two hands simultaneously
Smooth and responsive visualization

📂 OUTPUT:
The number of fingers detected is displayed:
  Near each hand (Left / Right)
  As a total count at the top-left corner of the window

🛠️ REQUIREMENTS:
Python 3.x
OpenCV
MediaPipe

Install the dependencies using:
```bash
pip install opencv-python mediapipe
```
▶️ HOW TO RUN:
>Ensure your webcam is connected and not being used by another application.
>Run the script:
```bash
python #HAND_FINGER_COUNTER.py
```
>Press ESC to exit the application.

🧠 LOGIC:
The application uses MediaPipe’s hand landmarks.
Thumb direction is determined based on hand side (Left/Right).
Other fingers are checked by comparing tip and lower joint positions.
