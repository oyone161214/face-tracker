from os import environ
environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

from gpiozero import Servo
import time
import warnings
import cv2

warnings.filterwarnings("ignore")

# Specify which camera to use (0 = default, built-in, or first detected USB camera)
CAM_ID = 0

# Path to the pre-trained model file for face recognition (adjust for your environment)
CASCADE_FILE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"


servo1 = Servo(18, min_pulse_width=0.6/1000, max_pulse_width=2.3/1000)
servo2 = Servo(12, min_pulse_width=0.6/1000, max_pulse_width=2.3/1000)

"""test data"""
move_bulk1 = [90, -90, 0]
move_bulk2 = [90, -90, 0]

"""
 Assumption: We will receive the coordinates (x, y) of the object's center point from the image recognition program.
 Resolution: The camera resolution is 640x480.
 If the x-coordinate is 320 (horizontal center), rotate right by 45 degrees.
 If the y-coordinate is 240 (vertical center), rotate up by 45 degrees.
"""
move_servo1 = [320, -320, 320, -320, 0]
move_servo2 = [240, -240, 240, -240, 0]
# move_servo1 = [320, 240, 160, 80, 0, -80, -160, -240, -320]
# move_servo2 = [320, -240, 160, -80, 0, 80, -160, 240, -320]

coordinate_groop_example = [(320,240), (-320,-240), (320,240), (-320,-240)]

def move_servo(servo_type, angle, hold_time=0.25):
    if not -90 <= angle <= 90:
        raise ValueError("Angle must be between -90 and 90")

    servo_type.value = angle / 90.0
    time.sleep(hold_time)
    servo_type.value = None

def convert_angle(servo_type,coordinate):
    if servo_type == servo1:    
        angle = coordinate // 7.11
        return max(-90, min(90, angle))
    elif servo_type == servo2:
        angle = coordinate // 5.33
        return max(0, min(90, angle))


def return_center(servo_type, hold_time=0.25):
    servo_type.value = 0.0
    time.sleep(hold_time)
    servo_type.value = None


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

"""test movement"""
# for i in move_bulk1:
#     move_servo(servo1, i)

# for i in move_bulk2:
#     move_servo(servo2, i)

"""test movement from coordinate"""
# for x in move_servo1:
#     angle1 = convert_angle(servo1,x)
#     move_servo(servo1, angle1)

# for y in move_servo2:
#     angle2 = convert_angle(servo2,y)
#     move_servo(servo2, angle2)


""" test movement from coordinate groop"""
for coord in coordinate_groop_example:
    angle1 = convert_angle(servo1,coord[0])
    angle2 = convert_angle(servo2, coord[1])
    move_servo(servo1, angle1)
    move_servo(servo2, angle2)

return_center(servo1)
return_center(servo2)
