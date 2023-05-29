from pylx16a.lx16a import *
import time
import math
import string
LX16A.initialize("/dev/ttyUSB0")

class motor:
    def __init__(self,porta):
        self.porta = porta
        self.rev = 0
    def setor(self):
        valor = math.floor(LX16A(self.porta).get_physical_angle())
        if(valor >= -48 and valor < 0):
            return(0)
        elif(valor >= 0 and valor < 60):
            return(1)
        elif(valor >= 60 and valor < 120):
            return(2)
        elif(valor >= 120 and valor < 180):
            return(3)
        elif(valor >= 180 and valor < 240):
            return(4)
        else:
            return(5)
    def pos(self):
        return str(math.floor(LX16A(self.porta).get_physical_angle()))#arredondar o mais perto, -48 -30 0  0 30 60  90 150 210 270
    def move(self,vel1):
        LX16A(self.porta).motor_mode(vel1)
motor1 = motor(1)
motor2 = motor(2)
motor3 = motor(3)
motor4 = motor(4)
def VirarDireita(vel):
    motor1.move(vel)
    motor2.move(vel)
    motor3.move(-vel)
    motor4.move(-vel)
    init = [motor1.setor(),motor2.setor(),motor3.setor(),motor4.setor()]
    flag = [0,0,0,0]
    while flag[0] == 0 or flag[1] == 0 or flag[2] == 0 or flag[3] == 0:
        if(init[0] != motor1.setor()):
            flag[0] = 1
        if(init[1] != motor2.setor()):
            flag[1] = 1
        if(init[2] != motor3.setor()):
            flag[2] = 1
        if(init[3] != motor4.setor()):
            flag[3] = 1
    while flag[0] == 1 or flag[1] == 1 or flag[2] == 1 or flag[3] == 1:
        if(init[0] == motor1.setor()):
            flag[0] = 0
        if(init[1] == motor2.setor()):
            flag[1] = 0
        if(init[2] == motor3.setor()):
            flag[2] = 0
        if(init[3] == motor4.setor()):
            flag[3] = 0
    motor1.move(0)
    motor2.move(0)
    motor3.move(0)
    motor4.move(0)
VirarDireita(100)