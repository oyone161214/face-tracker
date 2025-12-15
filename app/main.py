import cv2

from camera import find_and_open, camera, end_camera
from servo import move_servo, convert_angle, return_center, servo1, servo2
# from facial_recognition import face_track

def main():
    
    debug = False

    cap, cascade = find_and_open()
    if cap is None:
        return

    current_pan = 0.0
    current_tilt = 0.0


    PAN_GAIN = 0.05
    TILT_GAIN = 0.05  

    return_center(servo1)
    return_center(servo2)

    DEAD_ZONE = 50

    try:
    # (x,y)received from face_track
        while True:
            response = camera(cap, cascade, debug)

            if response is None:
                continue

            diff_x, diff_y = response

            if abs(diff_x) < DEAD_ZONE: diff_x = 0
            if abs(diff_y) < DEAD_ZONE: diff_y = 0

            # move servos diffelence angle
            diff1 = convert_angle(servo1, diff_x)
            diff2 = convert_angle(servo2, -diff_y)

            if diff1 != 0 or diff2 != 0:
                current_pan += diff1
                current_tilt += diff2
                current_pan = max(-90, min(90, current_pan))
                current_tilt = max(-90, min(0, current_tilt))
            
            
                move_servo(servo1, current_pan)
                move_servo(servo2, current_tilt)
    
    except KeyboardInterrupt:
        pass

    
    return_center(servo1)
    return_center(servo2)
    end_camera(cap)
    


if __name__ == "__main__":
    main()