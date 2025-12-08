import cv2

from mediapipe_version.m_camera import find_and_open, camera, end_camera, camera_mediapipe
from mediapipe_version.m_servo import move_servo, convert_angle, return_center, servo1, servo2
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

    DEAD_ZONE = 30


    try:
        print("Start Tracking... Press 'q' to quit.")
        while True:

            found, (diff_x, diff_y) = camera_mediapipe(cap, debug)
            

            if not found:
                continue

            if abs(diff_x) < DEAD_ZONE: diff_x = 0
            if abs(diff_y) < DEAD_ZONE: diff_y = 0


            pan_step = diff_x * PAN_GAIN
            tilt_step = diff_y * TILT_GAIN

            current_pan += pan_step
            current_tilt -= tilt_step

            current_pan = max(-90, min(90, current_pan))
            current_tilt = max(-90, min(90, current_tilt))

            move_servo(servo1, current_pan)
            move_servo(servo2, current_tilt)

            # debug
            # print(f"Diff: {diff_x}, {diff_y} -> Angle: {current_pan:.1f}, {current_tilt:.1f}")

    except KeyboardInterrupt:
        pass


    return_center(servo1)
    return_center(servo2)
    end_camera(cap)
    




if __name__ == "__main__":
    main()