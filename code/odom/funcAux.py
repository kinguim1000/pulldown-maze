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