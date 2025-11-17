import cv2
from app.servo import move_servo, convert_angle, return_center

# Specify which camera to use (0 = default, built-in, or first detected USB camera)
CAM_ID = 0

# Path to the pre-trained model file for face recognition (adjust for your environment)
CASCADE_FILE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"



def face_track():
    for i in range(5):
        # Explore available cameras by changing the camera ID
        # Capture video from the selected camera
        cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
            
        if not cap.isOpened():
            print(f"Camera {i} opened")
            CAM_ID = i
            break

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)    
    # Load the Haar Cascade classifier
    cascade = cv2.CascadeClassifier(CASCADE_FILE)
    
    print("Starting face recognition... (Press 'q' to quit)")

    while True:
        # Read one frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame.")
            break

        # Convert the frame to grayscale to speed up processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the result in a window
        cv2.imshow('Face Recognition', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Face recognition ended.")

if __name__ == '__main__':
    face_track()