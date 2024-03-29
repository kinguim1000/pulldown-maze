
from pylx16a.lx16a import *
import string
import time
import math
LX16A.initialize("/dev/ttyUSB0")
from imusensor.MPU9250 import MPU9250
from imusensor.filters import madgwick
import smbus
def sign(c):
    if(c < 0):
        return -1
    return 1
def sqrt(n):
    x = n
    for i in range(10):
        x = (x*x+n)/(2*x)
    return x
class motor:
    def __init__(self,porta):
        self.porta = porta
        self.rev = 0
    def pos(self):
        return str(math.floor(LX16A(self.porta).get_physical_angle()))#arredondar o mais perto, -48 -30 0  0 30 60  90 150 210 270
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
        
class IMU: 
    def __init__(self,endereco):
        self.imu = MPU9250.MPU9250(smbus.SMBus(1), endereco)
        self.imu.begin()
        self.imu.loadCalibDataFromFile("/home/pi/calib_real4.json")
        self.sensorfusion = madgwick.Madgwick(0.5)
        self.currTime = time.time()
        self.newTime = time.time()
    def __Atualizar(self):
        self.imu.readSensor()
        self.imu.computeOrientation()
        self.newTime = time.time()
        self.dt = self.newTime - self.currTime
        self.currTime = self.newTime
        #self.sensorfusion.computeAndUpdateRollPitchYaw(self.imu.AccelVals[0], self.imu.AccelVals[1], self.imu.AccelVals[2], self.imu.GyroVals[0], self.imu.GyroVals[1], self.imu.GyroVals[2], self.imu.MagVals[0], self.imu.MagVals[1], self.imu.MagVals[2], self.dt)
        self.sensorfusion.updateRollPitchYaw(self.imu.AccelVals[0], self.imu.AccelVals[1], self.imu.AccelVals[2], self.imu.GyroVals[0], self.imu.GyroVals[1], self.imu.GyroVals[2], self.imu.MagVals[0], self.imu.MagVals[1], self.imu.MagVals[2], self.dt)
        return
    def yaw(self): 
        self.__Atualizar()
        return self.sensorfusion.yaw + 180
        
    def pitch(self):
        self.__Atualizar()
        return self.sensorfusion.pitch
    def Aceleracao(self):
        self.__Atualizar()
        return self.imu.AccelVals    
class SD:
    def __init__(self,buffersize):
        self.buffersize = buffersize
        self.buffer = []
        self.recente = 0

    def Avg(self):
        avg = 0
        size = len(self.buffer)
        for i in range(size):
            avg += self.buffer[i]
        if size != 0:
            return avg/size
        else:
            return 0

    def Desvio(self):
        variancia = 0
        media = self.Avg()
        size = len(self.buffer)
        for i in range(size):
            temp = self.buffer[i] - media 
            variancia += temp*temp
        variancia = variancia/size
        return sqrt(variancia)

    def Atualizar(self,valor):
        if(len(self.buffer) < self.buffersize):
            self.buffer.append(valor)
        else:
            self.buffer[self.recente] = valor
            self.recente = (self.recente + 1) % self.buffersize
        return

    def Flush(self):
        self.buffer = []
        self.recente = 0
        return

class FuncAprox:
    def __init__(self):
        self.buffer = []

    def Atualizar(self,valor):
        self.buffer.append(valor)
        return

    def Funcao(self):
        size = len(self.buffer)
        x = [i + 1 for i in range(size)]
        y = self.buffer
        avg = 0
        for i in range(size):
            avg += y[i]
        avg = avg/size
        Sxy = 0
        for i in range(size):
            Sxy += (x[i] - (size+1)/2) * (y[i] - avg)
        Sxx = 1/12 * size * (-1+ (size*size))
        try:
            a = Sxy/Sxx
        except ZeroDivisionError:
            return [1, 0]
        if a == 0:
            return [1, 0]
        return [a, avg - ((a) * (size+1)/2)]
    
    def Flush(self):
        self.buffer = []
        return



class Robo: #Classe que vai segurar... Tudo... em teoria vai ajudar na organização e como bonus tira a necessidade de whiles desnecessarios
    def __init__(self,portaFE,portaFD,portaTE,portaTD):
        self._motores = [motor(portaFE),motor(portaFD),motor(portaTE),motor(portaTD)]
        self._imu = IMU(0x68)
        self._sd = SD(100)
        self._funcao = FuncAprox()
        self._erro = [0,0,0,0]
        self._intencao = [0 ,0]
        self._acumulador = 0
        self._vel = 150
        self._roda = 18
        self._pi = 104348/33215
        self._offset = 90 #offset de uma roda para outra, aqui para tentar consertar a p****** que acontece com os encoders
        self._lookup = {
            0:"Fazer nada",
            1:"Virar Direita",
            2:"Virar Esquerda",
            3:"Seguir Reto",
            4:"Boot"
            #toda vez que quiser adicionar uma ação continua nova, colocar aqui para ficar facil de saber o que diabos faz
        }
        for i in range(1000):
           self._imu.yaw()

    def __KillMotors(self):
        self._motores[0].move(0)
        self._motores[1].move(0)
        self._motores[2].move(0)
        self._motores[3].move(0)
        return

    def __Boot(self): #descobre os erros dos motores e em teoria tenta concertar eles :D
        vel = self._vel
        intencao = self._intencao[1]
        if intencao == 0 or intencao == 1 or intencao == 2 or intencao == 3:
            self._motores[intencao].move(vel)
            if(self._motores[intencao].pos() > 5 and self._motores[intencao].pos() < 10):
                self.__KillMotors()
                self.__MudarIntencao(4,intencao + 1)
                return
            self._funcao.Atualizar(self._motores[intencao].pos())
            if(self._motores[intencao].pos() > 200 and self._erro[intencao] == 0 and self._motores[intencao].pos()/self.funcao.Funcao()[0] > self._sd.Avg() + 2*self._sd.Desvio()):
                self._erro[intencao] = self._motores[intencao].pos()
            self._sd.Atualizar(self._motores[intencao].pos()/self._funcao.Funcao()[0])
        elif intencao == 4 or intencao == 5:
            self._motores[intencao-4].move(vel/2)
            if(self._motores[intencao-4].pos() + 0.5 > (self.motores[intencao-2].pos() + self._offset)%360 or self._motores[intencao-4].pos() - 0.5 < (self.motores[intencao-2].pos() + self._offset)%360):
                self.__KillMotors()
                self.__MudarIntencao(4,intencao + 1)
                return
        else:
            self.__MudarIntencao(0,0)
            return

    def __LerMotores(self,lado):
        if lado == 0: #lado esquerdo
            if(self._motores[0].pos() >= self._erro[0]):
                return self._motores[2].pos() + self._offset
            return self._motores[0].pos()
        elif lado == 1: #lado direito
            if(self._motores[1].pos() >= self._erro[1]):
                return self._motores[3].pos() + self._offset
            return self._motores[1].pos()
        else:
            print("Lado Inválido")
            return 0

    def __MudarIntencao(self,intencao,valor):
        if intencao ==  0:
            self._acumulador = 0
        elif intencao == 1 or intencao == 2: 
            self._acumulador = self._imu.yaw()
        elif intencao == 3:
            self._acumulador = [self.__LerMotores(0),-1,1]
        elif intencao == 4:
            self._acumulador = 0
            self._sd.Flush()
            self._funcao.Flush()
        else:
            print("Intenção inválida")
            return
        self._intencao = [intencao,valor]
        return

    def __VirarDireita(self): 
        vel = self._vel
        self._sd.Atualizar(self._imu.yaw())
        if(sign(self._acumulador - self._intencao[1])*self._sd.Avg() > ((self._acumulador - self._intencao[1] + 360)%360)*sign(self._acumulador - self._intencao[1])):
            self._motores[0].move(vel)
            self._motores[1].move(vel)
            self._motores[2].move(vel)
            self._motores[3].move(vel)
        else:
            self.__KillMotors()
            self.__MudarIntencao(0,0)
        return

    def __VirarEsquerda(self):
        vel = self._vel
        if(self._imu.yaw() < (self._acumulador + self._intencao[1])%360):
            self._motores[0].move(-vel)
            self._motores[1].move(-vel)
            self._motores[2].move(-vel)
            self._motores[3].move(-vel)
        else:
            self.__KillMotors()
            self.__MudarIntencao(0,0)
        return
    
    def __SeguirReto(self):
        vel = self._vel
        if(self._acumulador[1] == -1):
            self._acumulador[1] = int(self._intencao[1]/(self._pi * self._roda))
            self._intencao[1] = self._intencao[1] - (self._acumulador[1]*self._pi * self._roda)

        if(self._acumulador[1] > 0):
            self._motores[0].move(vel)
            self._motores[1].move(-vel)
            self._motores[2].move(vel)
            self._motores[3].move(-vel)

        elif(self.__LerMotores(0) > self._acumulador[0] + self._intencao[1] - 1 or self.__LerMotores(0) < self._acumulador[0] + self._intencao[1] + 1):
            self.__KillMotors
            self.__MudarIntencao(0,0)
            return

        if(self._acumulador[2] == 1):
            if(self.__LerMotores(0) > self._acumulador[0] + 1 or self.__LerMotores(0) < self._acumulador[0] - 1):
                self._acumulador[2] = 0
                return
        elif(self._acumulador[2] == 0):
            if(self.__LerMotores(0) < self._acumulador[0] + 1 or self.__LerMotores(0) > self._acumulador[0] + 1):
                self._acumulador[2] = 1
                self._acumulador[1] = self._acumulador[1]-1
                return
        return

    def PrintIntencao(self):
        string = self._lookup[self._intencao[0]] + " "
        if self._intencao[0] ==  1 or self._intencao[0] == 2:
            string = string + str(self._intencao[1])+"⁰"
        elif self._intencao[0] == 3:
            if(self._acumulador[1] >= 1):
                string = string +str(self._acumulador[1])+" rotações completas e "
            string = string +str(self._intencao[1])+" cm"
        print(string + str(self._sd.Avg()))
        return

    def Virar(self,lado,angulo):
        if(self._intencao[0] == 1 or self._intencao[0] == 2): 
            return
        if(angulo < 0 or angulo > 360):
            print("Angulo Inválido")
            return
        if(lado == 0): # Virar para a Direita
            self.__MudarIntencao(1,angulo)
        elif(lado == 1): # Virar para a Esquerda
            self.__MudarIntencao(2,angulo)
        else:
            print("Lado inválido")
        return

    def Andar(self,distancia):
        if(self._intencao[0] == 3):
            return
        if(distancia < 0):
            print("Distancia inválida")
            return
        self.__MudarIntencao(3,distancia)
        return

    def Main(self):
        if self._intencao[0] ==  0:
            pass
        elif self._intencao[0] ==  1:
            self.__VirarDireita()
        elif self._intencao[0] == 2:
            self.__VirarEsquerda()
        elif self._intencao[0] == 3:
            self.__SeguirReto()
        elif self._intencao[0] == 4:
            self.__Boot()
        else:
            print("Estado interno inválido")
            self.__MudarIntencao(0,0)
        self.PrintIntencao()
        #inserir codigo de fazer a matriz
        #inserir maze solving
        #etc...
        #basicamente qualquer coisa que dá pra rodar no fundo enquanto o role todo tá acontecendo
        #também colocar aqui as coisas de mudar de intenção, com o sistema de prioridade e tals
        #A idéia disso tudo é não ter nenhum while dentro do código, e também organizar tudo, e assim fica bem organizado
        return

PulldownMaze = Robo(2,1,4,3)
PulldownMaze.Virar(0,90)
#Imu = IMU(0x68)
#sd = SD(100)
while(True):
    PulldownMaze.Main()
    #print(Imu.yaw())
    #isso é o mais proximo de "if going_to_crash: Dont()" que vamos chegar, eu acho 
