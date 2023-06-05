from pylx16a.lx16a import *
import string
import math
LX16A.initialize("/dev/ttyUSB0")
def round(x):
    y = x - int(x) 
    if(y <= 0.5):
        return int(x)
    elif(y > 0.5):
        return int(x) + 1
def min(a,b,c,d):
    return [a,b,c,d].sort()[0]
pi = 104348/33215
class motor:
    def __init__(self,porta):
        self.porta = porta
        self.rev = 0
    def pos(self):
        return math.floor(LX16A(self.porta).get_physical_angle())#arredondar o mais perto, -48 -30 0  0 30 60  90 150 210 270
    def move(self,vel1):
        LX16A(self.porta).motor_mode(vel1)
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
motor1 = motor(1)
motor2 = motor(2)
motor3 = motor(3)
motor4 = motor(4)

    
class SensoresJuntos:
    def __init__(self, frenteesquerda, frentedireita, trasesqueda, trasdireita, errorval ,offset):
        self.motorFE = frenteesquerda
        self.motorFD = frentedireita
        self.motorTE = trasesqueda
        self.motorTD = trasdireita
        self.offset = offset
        self.errorval = errorval

    def inicializar(self):
        while(self.motorFE.pos() > -45 or self.motorFE.pos() < -40):
            self.motorFE.move(500)
        self.motorFE.move(0)
        while(self.motorTE.pos() > 0):  
            self.motorTE.move(500)
        while(self.motorTE.pos() < self.motorFE.pos() + self.offset or self.motorTE.pos() > self.motorFE.pos() + self.offset + 5):
            self.motorTE.move(500)
        self.motorTE.move(0)

        while(self.motorFD.pos() > -45 or self.motorFD.pos() < -40):
            self.motorFD.move(500)
        self.motorFD.move(0)
        while(self.motorTD.pos() > 0):  
            self.motorTD.move(500)
        while(self.motorTD.pos() < self.motorFD.pos() + self.offset or self.motorTD.pos() > self.motorFD.pos() + self.offset + 5):
            self.motorTD.move(500)
        self.motorTD.move(0)

    def Ler(self,lado): #lado = 0 é esquerda, lado = 1 é direita 
        if(lado == 0): 
            if(self.motorTE.pos() > self.errorval):
                return self.motorFE.pos() + self.offset
            else:
                return self.motorTE.pos()
        elif(lado == 1): 
            if(self.motorTD.pos() > self.errorval):
                return self.motorFD.pos() + self.offset
            else:
                return self.motorTD.pos()
        return
a = SensoresJuntos(motor1,motor2,motor4,motor3,270, 90)
a.inicializar()
def AndarDist(velocidade,distancia):
    rotations = distancia/(7*pi)
    init = a.Ler(0)
    while(a.Ler(0) > (init + rotations)%360 + 5 or a.Ler(0) < (init + rotations)%360 - 5):
        motor1.move(-velocidade)
        motor2.move(velocidade)
        motor3.move(velocidade)
        motor4.move(-velocidade)
    motor1.move(0)
    motor2.move(0)
    motor3.move(0)
    motor4.move(0)
AndarDist(500,5)
