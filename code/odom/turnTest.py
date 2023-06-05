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
motor2 = motor(4)
motor3 = motor(2)
motor4 = motor(3)
def VirarDireita(vel):
    cont = 0
    lookup = {0:4,1:5,2:0,3:1,4:2,5:3}
    #,motor2.se
    # tor(),motor3.setor(),motor4.setor()
    valorInicial = [motor1.setor()]
    print(valorInicial)
    #and motor2.setor() == valorInicial[2] and motor3.setor() == valorInicial[3] and motor4.setor() == valorInicial[4]
    while(motor1.setor() == valorInicial[0] or cont < 1 ):
        motor1.move(vel)
        motor2.move(vel)
        motor3.move(vel)
        motor4.move(vel)
        if motor1.setor() != valorInicial[0]:
            cont += 1
            print(cont) 
            print(motor1.setor())

    while (motor1 != lookup[valorInicial[0]]):  
        print(motor1.setor())
        if(motor1.setor() == lookup[valorInicial[0]] ):
            motor1.move(0)
            motor2.move(0)
            motor3.move(0)
            motor4.move(0)
            break
        
        # and motor2.setor() != valorInicial[2] and motor3.setor() != valorInicial[3] and motor4.setor() != valorInicial[4]
    
VirarDireita(500)
