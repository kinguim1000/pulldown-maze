from pylx16a.lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0")

try:
    servo1 = LX16A(1)
    #servo2 = LX16A(3)
    #servo1.disable_torque
    #servo2.disable_torque

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

t = 0
state = True
while True:
   
    #servo1.motor_mode(-1000)

    
    # servo1.servo_mode()
    # servo.move(180)
    
    print(servo1.get_physical_angle())
    # print(servo1.get_commanded_angle())
        # print(True,servo2.get_motor_speed)
    #if servo2.get_physical_angle() < 2000:
     #   if state == True:
      #      state = False
    servo1.motor_mode(0)
        #    time.sleep(0.4)
        #else:

            #state = True
            #servo2.motor_mode(-200)
            #time.sleep(0.4)
#    if state:
 #       servo2.motor_mode(-200)
  #  else:
   #     servo2.motor_mode(200)