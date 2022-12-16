import math
inserirnumero = 100
def Corrigir(): #Sao pra ser os sensores do lado, os que estao a 45⁰ um do outro:)
    D0 = Sensor_1
    D1 = Sensor_2 #Eu sei que n sao esses os nomes, to só vendo como ia ficar pra ver se é coerente
    for i in range(inserirnumero):
        motor(-50,50)
    motor(0,0)
    D2 = Sensor_1
    D3 = Sensor_2
    sin45 = math.sqrt(2)/2
    if (D0 - sin45 * D1) < (D2 - sin45 * D3):
        Vel = 50
    else:
        Vel = -50
    Erro = 1
    while robot.step(timeStep) != -1 and Erro > 0.0001:
        Erro = (Sensor_1 / Sensor_2) - sin45
        PID_só_Que_Pra_Girar(Vel,-Vel,Erro)
#Eu acho que é isso.......
#Faz sentido?

#math.sqrt(x)
