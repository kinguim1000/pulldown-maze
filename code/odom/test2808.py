from pylx16a.lx16a import *
import time
import math
import string
LX16A.initialize("/dev/ttyUSB0")




class PID:
    def __init__(self,P,I,D):
        self.kp = P
        self.ki = I
        self.kd = D
        self.prev = 0
        self.anterior = 0;
    def atualizar(self,erro):
        self.prev += erro
        self.anterior = erro
    def out (self,erro):
        self.atualizar(erro)
        return self.kp*erro + self.ki*self.prev + self.kd*(erro - self.anterior)

def sign(a):
    if a < 0:
        return -1
    if a == 0:
        return 0
    return 1
def abs(a):
    if a < 0:
        return -a
    return a
def mapa(input):
    return (800/(1+(20/(abs(input)+0.00001))))*sign(input)





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
        return math.floor(LX16A(self.porta).get_physical_angle())+48#arredondar o mais perto -> transforma -48 em 0, -48 -30 0  0 30 60  90 150 210 270f
    def move(self,vel1):
        LX16A(self.porta).motor_mode(vel1)
motor1 = motor(1)
motor2 = motor(4)
motor3 = motor(2)
motor4 = motor(3)
# posicao = [motor1.pos(),motor2.pos(),motor3.pos(),motor4.pos()]#pra n dar problema de escopo
# def #atualizar():
#     posicao = [motor1.pos(),motor2.pos(),motor3.pos(),motor4.pos()]
def posicao(num):
    if num == 0:
        return motor1.pos()
    if num == 1: 
        return motor2.pos()
    if num == 2:
        return motor3.pos()
    if num == 3:
        return motor4.pos()
def encoder():
    #atualizar()
    
    if(posicao(3) > 60 and posicao(3) < 260): #usar outro motor pra pegar pos
        print([posicao(3),3])
        return [posicao(3),3]
    elif(posicao(2)> 60 and posicao(2) < 260):
        print([posicao(2),2])
        return [posicao(2),2]
    elif(posicao(1)> 60 and posicao(1) < 260):
        print([posicao(1),1])
        return [posicao(1),1]
    else:
        print([posicao(0),0])
        return [posicao(0),0]

def turnLeft(vel):
    idMotor = encoder()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente 
    start = encoder()[0]
    print("entrou")
    print(idMotor)
    print(start)
    #atualizar()
    if(posicao(idMotor) > 120):#garantir( sendo que acima ja tem 4 verificações de qual usar ( tem que ver se para tras tbm vale os valores))
        while(posicao(idMotor) > start-115): #não sei se é maior ou menor que
            #atualizar()
            print("situaçao maior q 100")
            print(posicao(idMotor))
            irEsquerda(vel)
    else:
        resto = 115 - start 
        print(resto)
        while(posicao(idMotor) > 1) and (posicao(idMotor) < 200):
            print("situaçao menor q 1")
            print(posicao(idMotor))

            #atualizar()
            irEsquerda(vel)
        idMotor = encoder()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente 
        start = encoder()[0]
        
        while(posicao(idMotor) > start - resto ):
            print("situaçao terminando o giro")
            print(posicao(idMotor))

            #atualizar()
            irEsquerda(vel)

def turnRight(vel):
    idMotor = encoder()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
    start = encoder()[0]#teoria escolhe ja o melhor motor para fazer essa decisão

    #atualizar()
    if(posicao(idMotor) < 183):
        while(posicao(idMotor) < start+115): #não sei se é maior ou menor que
            #atualizar()
            print('situaçao menor q 228')
            print(posicao(idMotor))
            irDireita(vel)
    else:
        
        resto = 115 - (300 - posicao(idMotor))   #maior q 228
        
        while(posicao(idMotor) > 200 and posicao(idMotor) < 300):#estar entre 228 e 318
            #atualizar()
            
            print('situacao maior q 200')
            print(posicao(idMotor))
            irDireita(vel)
        idMotor = encoder()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
        start = encoder()[0]
        while(posicao(idMotor) < start + resto ):
            #atualizar()
            print("situacaoterminando giro")
            print(posicao(idMotor))
            irDireita(vel)
        

def frente(vel):
    cont = 0
    lookup = {0:4,1:5,2:0,3:1,4:2,5:3}#meia rotação
    #,motor2.se
    # tor(),motor3.setor(),motor4.setor()
    valorInicial = [motor1.setor()]
    print(valorInicial)
    #and motor2.setor() == valorInicial(2) and motor3.setor() == valorInicial[3] and motor4.setor() == valorInicial[4]
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
    #atualizar()
    if(posicao(3)< 20 or posicao(3) > 181): #usar outro motor pra pegar pos
        return [posicao(3),3]
    elif(posicao(2)< 20 or posicao(2) > 181):
        return [posicao(2),2]
    elif(posicao(1)< 135 or posicao(3) > 300):
        return [posicao(1),1]
    else:
        return [posicao(0),0]
def frente2(vel):
    idMotor = aux()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
    start = aux()[0]
    #atualizar()
    lookup = {0:False, 1:False, 2:True, 3:True}
    print(idMotor)
    if(start< 115 or start > 181):
        print("entrou1")
        if lookup[idMotor]:
            a = start - 108
            if a < 0:
                print("4")
                a += 360
            print("3")
            while posicao(idMotor) > a: #-> se a for menor q 360 ele vai ser entre -48 e -180 então entra certo
                ##atualizar()
                print("entrou2")
                irFrente(vel)
        else:
            print("entrou5")
            print(start)
            print(posicao(idMotor))
            if(start > 108):
                while posicao(idMotor) > 180:
                    irFrente(vel)
            while posicao(idMotor) < (start + 180)%360: #se passar de 360 volta pro range normal
                ##atualizar()
                irFrente(vel)
    else:
        if lookup[idMotor]:
            resto = 180 - (360 - start)  
            while(posicao(idMotor) <200):
                ##atualizar()
                irFrente(vel)
            idMotor = aux()[1]#isso aqui tem que ##atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
            start = aux()[0]
            ##atualizar()
            while posicao(idMotor) < start + resto:
                ##atualizar()
                irFrente(vel)
        else:
            resto = 180 - start  
            while(posicao(idMotor) >0):
                ##atualizar()
                irFrente(vel)
            idMotor = aux()[1]#isso aqui tem que ##atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
            start = aux()[0]
            ##atualizar()
            while(posicao(idMotor) > start - resto):
                ##atualizar()
                irFrente(vel)
        #ou menor n sei depende se aumenta ou diminui
        # and motor2.setor() != valorInicial(2) and motor3.setor() != valorInicial[3] and motor4.setor() != valorInicial[4]
def frente3(vel):
    idMotor = aux()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
    start = aux()[0]
    print("entrou")
    print(idMotor) 
    print(start)  
    lookup = {0: True, 1: True, 2: False, 3:False}
    #atualizar()
    if(idMotor == 0 or idMotor == 1):
        if(posicao(idMotor) > 135):#garantir( sendo que acima ja tem 4 verificações de qual usar ( tem que ver se para tras tbm vale os valores))
            while(posicao(idMotor) > start-130): #não sei se é maior ou menor que
                #atualizar()
                print("situaçao maior q 100")
                print(posicao(idMotor))
                irFrente(vel)
        else:
            resto = 130 - start 
            print(resto)
            while(posicao(idMotor) > 1) and (posicao(idMotor) < 200):
                print("situaçao menor q 1")
                print(posicao(idMotor))

            #atualizar()   
                irFrente(vel)
            idMotor = aux()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente 
            start = aux()[0]
        
            while(posicao(idMotor) > start - resto ):
                print("situaçao terminando o giro")
                print(posicao(idMotor))

            #atualizar()   
                irFrente(vel)

    else:
        if(posicao(idMotor) < 170):
            while(posicao(idMotor) < start+130): #não sei se é maior ou menor que
                #atualizar()
                print('situaçao menor q 228')
                print(posicao(idMotor))
                irFrente(vel)
        else:

            resto = 130 - (300 - posicao(idMotor))   #maior q 228

            while(posicao(idMotor) > 170 and posicao(idMotor) < 300):#estar entre 228 e 318
            #atualizar()

                print('situacao maior q 200')
                print(posicao(idMotor))
                irFrente(vel)
            idMotor = aux()[1]#isso aqui tem que #atualizar a parte de cima pra ser os motores que vão pra frente(ou não caso for igual)
            start = aux()[0]
            print(start)
            print(resto)
            while(posicao(idMotor) < start + resto ):
            #atualizar()
                print("situacao terminando giroaaaaa")
                print(posicao(idMotor))
                irFrente(vel)
def abs(a):
    if a < 0:
        return -a
    return a

def err(motor,input):
    
    return  
def frente4(angulo):
    a = PID(0.5,0,5) 
    initial = encoder()
    k = {0:1,1:1,2:0,3:0}
    a.atualizar(posicao(initial[1])-initial[0])
    def d():
        return 360*k[initial[1]] - ((k[initial[1]]*2)-1)*((initial[0]-posicao(initial[1])+360+ angulo)%360)
    while(abs(posicao(initial[1])-initial[0])<5):
        irFrente(600)
    print(d())
    while(d() > 40):
        irFrente(int(mapa(a.out(d()))))
        print(d(),posicao(initial[1]))
    parar()
    print(d())

def tras(vel):
    a = PID(2,0,0) 
    initial = encoder()
    a.atualizar(posicao(initial[1])-initial[0])
    while(abs(posicao(initial[1])-initial[0])<10):
        irTras(vel)
    while(abs(posicao(initial[1])-initial[0])>5):
        irTras(int(mapa(a.out(abs(posicao(initial[1])-initial[0])))))
    parar()

def irFrente(vel):
    motor1.move(-vel)
    motor2.move(-vel)
    motor3.move(vel)
    motor4.move(vel)
def irTras(vel):
    motor1.move(vel)
    motor2.move(vel)
    motor3.move(-vel)
    motor4.move(-vel)
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
#turnRight(200)
#turnRight(200) #20,5 aproximadamente a rotação 3,4 cm pra frente. tanto de começo como pra fim
#turnLeft(200)
#turnLeft(200)
while(True):
    frente4(0)
    frente4(110)
    turnLeft(600)



#######lembrar de refazer o frente -> troca de lado ====
