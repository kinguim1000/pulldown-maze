def PID(lsetpoint, lkp, lki, lkd,e):
    I, P, D, pe = 0
    P = e
    I = e + I
    D = e - pe
    pid = P*lkp + I*lki + D*lkd
    vel = (100/((1/(100*pid*pid))+1))*sign(pid)
    pe = e
    motor(vel,vel)
def front()
    PID(setpoint,kp,kd,ki,distf()-lsetpoint)
def back()
    PID(setpoint,kp,kd,ki,distb()-lsetpoint)