class PID:
    def __init__(self,P,I,D):
        self.kp = P
        self.ki = I
        self.kd = D
        self.prev = 0
        self.anterior = 0;
    def atualizar(self,error):
        self.prev += erro
        self.anterior = erro
    def out (self,erro):
        self.atualizar(error)
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
def mapa(max,input):
    return (max/(1+((max/2)/abs(input))))*sign(input)