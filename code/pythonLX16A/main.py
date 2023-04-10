import string
from pylx16a.lx16a import *
import time
import math

LX16A.initialize("/dev/ttyUSB0")





class motor:
    def __init__(self,porta):
        self.porta = porta
        self.rev = 0
        
    

    def pos(self):
        return str(math.floor(LX16A(self.porta).get_physical_angle()))#arredondar o mais perto, -30 30 90 150 210 270
    def mover(self,vel1):
        LX16A(self.porta).motor_mode(vel1)

servo1 = motor(1)
servo2 = motor(2)

while True:
   
    
    servo1.mover(150)
    
    servo2.mover(150)
    print(servo1.pos()+"\\"+servo2.pos())
    # servo1.motor_mode()
    # servo.move(180)

    #print(servo1.get_physical_angle())
    # if servo1.get_physical_angle() == 255:
    #     setor = 5
    #print(setor)

        # print(True,servo2.get_motor_speed)
    #if servo2.get_physical_angle() < 2000:
     #   if state == True:
      #      state = False
    #if setor == 0:
    # angulo1 = math.floor(servo1.get_physical_angle())  
    # angulo2 = math.floor(servo2.get_physical_angle())  
    # angulo3 = math.floor(servo3.get_physical_angle())  
    # angulo4 = math.floor(servo4.get_physical_angle())  
    #elif setor == 1:
    #    angulo = (servo1.get_physical_angle()/255*60)+60
    #elif setor == 2:
    #    angulo = (servo1.get_physical_angle()/255*60)+120
    #elif setor == 3:
    #    angulo = (servo1.get_physical_angle()/255*60)+180
        
    #elif setor == 4:
    #    angulo = (servo1.get_physical_angle()/255*60)+240
    #elif setor == 5:
    #    angulo = (servo1.get_physical_angle()/255*60)+300
    
    # print(str(angulo1) + " \\ " + str(angulo2) + " \\ " + str(angulo3) + " \\ " + str(angulo4) + " \\ )
    # servo1.motor_mode(0) 
    # servo2.motor_mode(0) 
    # servo3.motor_mode(0) 
    # servo4.motor_mode(-1000) 
    