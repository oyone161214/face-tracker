from os import environ
environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

from gpiozero import Servo
import time
import warnings

warnings.filterwarnings("ignore")

servo1 = Servo(18, min_pulse_width=0.6/1000, max_pulse_width=2.3/1000)
servo2 = Servo(12, min_pulse_width=0.6/1000, max_pulse_width=2.3/1000)

def move_servo(servo_type, angle, hold_time=0.2):
    if not -90 <= angle <= 90:
        angle = max(-90, min(90, angle))

    servo_type.value = angle / 90.0

    # time.sleep(hold_time)
    # servo_type.value = None

def convert_angle(servo_type,coordinate):
    if servo_type == servo1:    
        angle = coordinate // 9.142
        return max(-90, min(90, angle))
    elif servo_type == servo2:
        angle = coordinate // 6.857
        return max(-90, min(90, angle))

def return_center(servo_type, hold_time=0.2):
    servo_type.value = 0.0
    time.sleep(hold_time)
    servo_type.value = None