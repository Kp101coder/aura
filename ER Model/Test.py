import mediapipe as mp
import cv2
import time

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)
printed = False
print("Opening camera 1")
try:
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('Raw Webcam Feed', frame)
        if not printed:
            print("Opened Camera 1")
            printed = True
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
except Exception as e:
    print(e)
    print("Error opening camera 1")

cap.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
print("Opening camera 2")
# Initiate holistic model
try:
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            # print(results.face_landmarks)
            
            # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
            
            # Recolor image back to BGR for rendering
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
            
            # Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            # Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                            
            cv2.imshow('Raw Webcam Feed', image)
            if printed:
                print("Opened camera 2")
                printed = False
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
except Exception as e:
    print(e)
    print("Error opening camera 2")
cap.release()
cv2.destroyAllWindows()

mp_holistic.POSE_CONNECTIONS

mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)

mp_drawing.draw_landmarks #??

cap = cv2.VideoCapture(0)
print("Opening camera 3")
try:
    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.6, min_tracking_confidence=0.6) as holistic:
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            # print(results.face_landmarks)
            
            # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
            
            # Recolor image back to BGR for rendering
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # 1. Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                    mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                    mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                    )
            
            # 2. Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                    )

            # 3. Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                    )

            # 4. Pose Detections
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                #                     mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                #                    mp_drawingq.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                #                   )
                            
            cv2.imshow('Raw Webcam Feed', image)
            if not printed:
                print("Opened Camera 3")
                printed = True
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
except Exception as e:
    print(e)
    print("Error opening camera 3")

cap.release()
cv2.destroyAllWindows()