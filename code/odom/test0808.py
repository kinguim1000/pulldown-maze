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
        # if(valor >= -48 and valor < 0):
        #     return(0)
        # elif(valor >= 0 and valor < 60):
        #     return(1)
        # elif(valor >= 60 and valor < 120):
        #     return(2)
        # elif(valor >= 120 and valor < 180):
        #     return(3)
        # elif(valor >= 180 and valor < 240):
        #     return(4)
        # else:
        #     return(5)
    def pos(self):
        return math.floor(LX16A(self.porta).get_physical_angle()+48)#arredondar o mais perto -> transforma -48 em 0, -48 -30 0  0 30 60  90 150 210 270f
    def move(self,vel1):
        LX16A(self.porta).motor_mode(vel1)
motor1 = motor(1)
motor2 = motor(4)
motor3 = motor(2)
motor4 = motor(3)
matrix = [motor1.pos(),motor2.pos(),motor3.pos(),motor4.pos()]#pra n dar problema de escopo
def atualizar():
    matrix = [motor1.pos(),motor2.pos(),motor3.pos(),motor4.pos()]
def encoder():
    atualizar()
    
    if(matrix[3] > 45 and matrix[3] < 273): #usar outro motor pra pegar pos
        print([matrix[3],3])
        return [matrix[3],3]
    elif(matrix[2]> 45 and matrix[2] < 273):
        print([matrix[2],2])
        return [matrix[2],2]
    elif(matrix[1]> 45 and matrix[1] < 273):
        print([matrix[1],1])
        return [matrix[1],1]
    else:
        print([matrix[0],0])
        return [matrix[0],0]

def turnRight(vel):
    idMotor = encoder()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente 
    start = encoder()[0];

    atualizar()
    if(matrix[idMotor] > 90):#garantir( sendo que acima ja tem 4 verificações de qual usar ( tem que ver se para tras tbm vale os valores))
        while(matrix[idMotor] > start-90): #não sei se é maior ou menor que
            atualizar()
            irDireita(vel)
    else:
        resto = matrix[idMotor] % 360
        
        while(matrix[idMotor] > 1):
            atualizar()
            irDireita(vel)
        idMotor = encoder()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente 
        start = encoder()[0];
        
        while(matrix[idMotor] > start - resto ):
            atualizar()
            irDireita(vel)

def turnLeft(vel):
    idMotor = encoder()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
    start = encoder()[0];#teoria escolhe ja o melhor motor para fazer essa decisão

    atualizar()
    if(matrix[idMotor] < 228):
        while(matrix[idMotor] < start+90): #não sei se é maior ou menor que
            atualizar()
            irEsquerda(vel)
    else:
        
        resto = matrix[idMotor]%360-48
        
        while(matrix[idMotor] < 200):#estar entre 228 e 318
            atualizar()
            irEsquerda(vel)
        idMotor = encoder()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
        start = encoder()[0];
        while(matrix[idMotor] < start + resto ):
            atualizar()
            irEsquerda(vel)
        

def frente(vel):
    cont = 0
    lookup = {0:4,1:5,2:0,3:1,4:2,5:3}#meia rotação
    #,motor2.se
    # tor(),motor3.setor(),motor4.setor()
    valorInicial = [motor1.setor()]
    print(valorInicial)
    #and motor2.setor() == valorInicial[2] and motor3.setor() == valorInicial[3] and motor4.setor() == valorInicial[4]
    while(motor1.setor() == valorInicial[0] or cont != 1 ):
        motor1.move(vel)
        motor2.move(-vel)
        motor3.move(-vel)
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


def aux():
    atualizar()
    if(matrix[3]< 138 or matrix[3] > 181): #usar outro motor pra pegar pos
        return [matrix[3],3]
    elif(matrix[2]< 138 or matrix[2] > 181):
        return [matrix[2],2]
    elif(matrix[1]< 138 or matrix[1] > 181):
        return [matrix[1],1]
    else:
        return [matrix[0],0]
def frente2(vel):
    idMotor = aux()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
    start = aux()[0];
    atualizar()
    lookup = {0:1, 1:0, 2:0, 3:1}
    if(start< 138 or start > 181):
        if lookup[idMotor]:
            a = start - 180
            if a < 0:
                a += 360
            while matrix[idMotor] > a: #-> se a for menor q 360 ele vai ser entre -48 e -180 então entra certo
                atualizar()
                irFrente(vel)
        else:
            while matrix[idMotor] < (start + 180)%360:#se passar de 360 volta pro range normal
                atualizar()
                irFrente(vel)
    else:
        if lookup[idMotor]:
            resto = 180 - (360 - start)  
            while(matrix[idMotor] <200):
                atualizar()
                irFrente(vel)
            idMotor = aux()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
            start = aux()[0];
            atualizar()
            while matrix[idMotor] < start + resto:
                atualizar()
                irFrente(vel)
        else:
            resto = 180 - start  
            while(matrix[idMotor] >0):
                atualizar()
                irFrente(vel)
            idMotor = aux()[1];#isso aqui tem que atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
            start = aux()[0];
            atualizar()
            while(matrix[idMotor] > start - resto):
                atualizar()
                irFrente(vel)
        #ou menor n sei depende se aumenta ou diminui
        # and motor2.setor() != valorInicial[2] and motor3.setor() != valorInicial[3] and motor4.setor() != valorInicial[4]
def irFrente(vel):
    motor1.move(vel)
    motor2.move(-vel)
    motor3.move(-vel)
    motor4.move(vel)
def irEsquerda(vel):
    motor1.move(-vel)
    motor2.move(-vel)
    motor3.move(-vel)
    motor4.move(-vel)
def irDireita(vel):
    motor1.move(vel)
    motor2.move(vel)
    motor3.move(vel)
    motor4.move(vel)
def parar():
    motor1.move(0)
    motor2.move(0)
    motor3.move(0)
    motor4.move(0)

turnLeft(500) #20,5 aproximadamente a rotação 3,4 cm pra frente. tanto de começo como pra fim
parar();


