from pylx16a.lx16a import *
import time
import math
# import pygame

LX16A.initialize("/dev/ttyUSB0")


# pygame.init()
# display = pygame.display.set_mode((300, 300))

class motor:
    def __init__(self,porta):
        self.porta = porta
        self.rev = 0
        # self.area = setor()#vira um millis de posição
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
servo1 = motor(1)
servo2 = motor(2)
servo3 = motor(3)
servo4 = motor(4)
class movimento:
    def __init__(self):
        self = self

    def mover(self,func,vel):
        self.func = func
        self.vel = vel
        if self.func == 0:
            servo1.move(0)
            servo2.move(0)
            servo3.move(0)
            servo4.move(0)
        elif self.func == 1:
            servo1.move(self.vel)
            servo2.move(-self.vel)
            servo3.move(-self.vel)
            servo4.move(self.vel)
        elif self.func == 2:
            servo1.move(-self.vel)
            servo2.move(self.vel)
            servo3.move(self.vel)
            servo4.move(-self.vel)
        elif self.func == 3:
            servo1.move(-self.vel)
            servo2.move(-self.vel)
            servo3.move(-self.vel)
            servo4.move(-self.vel)
        elif self.func == 4:
            servo1.move(self.vel)
            servo2.move(self.vel)
            servo3.move(self.vel)
            servo4.move(self.vel)


    
movimento = movimento()

# valorantigo = servo1.setor() 
# contador = 0
while True:
    







    # for event in pygame.event.get():   
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_a:
    #             movimento.mover(3, 600)

    #         if event.key == pygame.K_w:
    movimento.mover(1, 0)
    #         if event.key == pygame.K_d:
    #             movimento.mover(4, 600)
    #         if event.key == pygame.K_s:
