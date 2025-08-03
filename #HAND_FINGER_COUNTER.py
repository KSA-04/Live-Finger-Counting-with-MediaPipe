import cv2
import mediapipe as mp

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Finger tip indices
# These indices correspond to the landmarks provided by MediaPipe for hand tracking.
# 4: Thumb tip
# 8: Index finger tip
# 12: Middle finger tip
# 16: Ring finger tip
# 20: Pinky finger tip
finger_tips = [4, 8, 12, 16, 20]

# Open webcam
# UPDATED: Added cv2.CAP_DSHOW for better compatibility on Windows systems
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if camera opened successfully
if not cap.isOpened():
    print("❌ Camera not accessible. Please check if it's connected and not in use by another application.")
    exit()

def count_fingers(hand_landmarks, hand_label):
    """
    Counts the number of open fingers for a given hand.

    Args:
        hand_landmarks: A MediaPipe HandLandmarks object containing the coordinates of the hand joints.
        hand_label: A string ('Left' or 'Right') indicating which hand it is.

    Returns:
        An integer representing the count of open fingers.
    """
    count = 0
    landmarks = hand_landmarks.landmark

    # Thumb logic:
    # For the thumb, we compare the x-coordinate of the tip (4) with the x-coordinate of the joint just below it (3).
    # The orientation depends on whether it's a right or left hand.
    # This logic assumes a relatively upright hand posture.
    if hand_label == "Right":
        # For the right hand, if the thumb tip's x is less than its base's x, it's typically open.
        if landmarks[4].x < landmarks[3].x:
            count += 1
    else:  # Left hand
        # For the left hand, if the thumb tip's x is greater than its base's x, it's typically open.
        if landmarks[4].x > landmarks[3].x:
            count += 1

    # Index to pinky fingers logic:
    # For these fingers, we compare the y-coordinate of the tip with the y-coordinate of the joint two positions below it.
    # If the tip's y-coordinate is 'higher' (smaller value, as y-axis origin is top-left) than the joint below, the finger is considered open.
    for tip in finger_tips[1:]: # Start from index 1 (index finger) to skip the thumb
        if landmarks[tip].y < landmarks[tip - 2].y:
            count += 1

    return count

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame from webcam. Exiting.")
        break

    # Flip the frame horizontally for a mirror view, which is more intuitive for webcam interactions.
    frame = cv2.flip(frame, 1)
    # Convert the BGR (OpenCV default) frame to RGB, which MediaPipe expects.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the RGB frame to detect hand landmarks.
    result = hands.process(rgb_frame)

    left_fingers = 0
    right_fingers = 0

    # Check if any hands were detected and if handedness (left/right) information is available.
    if result.multi_hand_landmarks and result.multi_handedness:
        # Iterate through each detected hand and its corresponding handedness information.
        for hand_landmarks, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
            # Get the label ('Left' or 'Right') for the current hand.
            hand_label = hand_info.classification[0].label
            
            # Count the open fingers for the current hand.
            finger_count = count_fingers(hand_landmarks, hand_label)

            # Assign the finger count to the appropriate hand variable.
            if hand_label == 'Left':
                left_fingers = finger_count
            elif hand_label == 'Right':
                right_fingers = finger_count

            # Draw the hand landmarks and connections on the original BGR frame for visualization.
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display the individual hand count next to the hand.
            # Get the coordinates of the wrist (landmark 0) to place the text.
            coords = tuple([int(hand_landmarks.landmark[0].x * frame.shape[1]),
                            int(hand_landmarks.landmark[0].y * frame.shape[0])])
            cv2.putText(frame, f'{hand_label}: {finger_count}', coords,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2) # Blue color for individual counts

    # Display the total finger count at the top-left of the frame.
    total = left_fingers + right_fingers
    cv2.putText(frame, f'Total Fingers: {total}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3) # Green color for total count

    # Show the processed frame in a window.
    cv2.imshow("Hand Finger Counter", frame)

    # Wait for a key press (1ms delay).
    key = cv2.waitKey(1)
    # If the ESC key (ASCII 27) is pressed, break the loop.
    if key == 27:
        print("🚪 ESC pressed. Exiting.")
        break

# Release the webcam resource.
cap.release()
# Destroy all OpenCV windows.
cv2.destroyAllWindows()