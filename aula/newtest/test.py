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
   

    
    # servo1.servo_mode()
    # servo.move(180)

    #print(servo1.get_physical_angle())
    setor = servo1.get_physical_angle1()
    if servo1.get_physical_angle1() == 255:
        setor = 5
    #print(setor)

        # print(True,servo2.get_motor_speed)
    #if servo2.get_physical_angle() < 2000:
     #   if state == True:
      #      state = False
    servo1.motor_mode(100)
    if setor == 0:
        angulo = servo1.get_physical_angle()/255*60    
    elif setor == 1:
        angulo = (servo1.get_physical_angle()/255*60)+60
    elif setor == 2:
        angulo = (servo1.get_physical_angle()/255*60)+120
    elif setor == 3:
        angulo = (servo1.get_physical_angle()/255*60)+180
        
    elif setor == 4:
        angulo = (servo1.get_physical_angle()/255*60)+240
        for a in range(5):
            anguloanterior = angulo
            angulo = ((servo1.get_physical_angle()/255*60)+240+anguloanterior)/2
    elif setor == 5:
        angulo = (servo1.get_physical_angle()/255*60)+300
        
        anguloanterior = angulo
        angulo = ((servo1.get_physical_angle()/255*60)+300+anguloanterior)/2
    
    print(angulo)
    if angulo >= 240:
        servo1.motor_mode(100)
    else:
        servo1.motor_mode(200)