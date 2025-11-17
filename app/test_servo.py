from servo import move_servo, convert_angle, return_center, servo1, servo2

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