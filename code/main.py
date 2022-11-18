from controller import Robot
import math
from controller import PositionSensor
timeStep = 32            # Set the time step for the simulation
max_velocity = 6.28      # Set a maximum velocity time constant
# Make robot controller instance
robot = Robot()

# Define the wheels 
wheel1 = robot.getDevice("wheel1 motor")   # Create an object to control the left wheel
wheel2 = robot.getDevice("wheel2 motor") # Create an object to control the right wheel

# Set the wheels to have infinite rotation 
wheel1.setPosition(float("inf"))
wheel2.setPosition(float("inf"))

# Define distance sensors
s1 = robot.getDevice("ps5")
s2 = robot.getDevice("ps7")
s3 = robot.getDevice("ps0")
s4 = robot.getDevice("ps2")
gps = robot.getDevice("gps")

#Motor
def motor(vel1,vel2):
    wheel1.setVelocity(vel1/50)
    wheel2.setVelocity(vel2/50)

#Globais
velg = 50
kpRg = 1 #prop da rotação

kp = 1.5 #constante de prop
ki = 0 #constante de integral
kd = 0 #constante de derivada
I = 0 #integral
pe = 0 #anterior (previous error)
setpoint = 0.04 #ponto que queremos


#Color sensor
colorSensor = robot.getDevice("colour_sensor") # Step 2: Retrieve the sensor, named "colour_sensor", from the robot. Note that the sensor name may differ between robots)
colorSensor.enable(timeStep) # Step 3: Enable the sensor, using the timestep as the update rate
#colorUpdate
def color ():
    
    image = colorSensor.getImage()
    return [colorSensor.imageGetRed(image, 1, 0, 0), colorSensor.imageGetGreen(image, 1, 0, 0), colorSensor.imageGetBlue(image, 1, 0, 0)]



#Encoders
leftEncoder = wheel1.getPositionSensor()
rightEncoder = wheel2.getPositionSensor()
leftEncoder.enable(timeStep)
rightEncoder.enable(timeStep)
gps.enable(timeStep)



# Enable distance sensors N.B.: This needs to be done for every sensor
s1.enable(timeStep)
s2.enable(timeStep)
s3.enable(timeStep)
s4.enable(timeStep)
def distf():
    x = s2.getValue()
    y = s3.getValue()
    return (x*y)/(2*(x+y)*0.25882)
# Mini visualiser for the distance senors on the console


start = robot.getTime()


#Color
def whatColor():
    image = colorSensor.getImage()
    r = colorSensor.imageGetRed(image, 1, 0, 0)
    g = colorSensor.imageGetGreen(image, 1, 0, 0)
    b = colorSensor.imageGetBlue(image, 1, 0, 0)
    colorSens = [r,g,b]

    if colorSens[0] < 100 and colorSens[1] < 100 and colorSens[2] < 100 :
        return "black"
    elif colorSens[0] > 200  and colorSens[1] > 200 and colorSens[2] < 200 and colorSens[2] > 100:
        return "yellow"
    elif colorSens[0] > 200 and colorSens[1] > 200 and colorSens[2] > 200 and colorSens[0] != 255 and colorSens[1] != 255 and colorSens[2] != 255:
        return "white"
    elif colorSens[0] == 255 and colorSens[1] == 255 and colorSens[2] == 255:
        return "checkpoint"

Px = 0
Py = 0
Pz = 0
def sign(q):
    if q>0:
        return 1
    elif q<0: 
        return -1
    else:
        return 0



#while timeStep != 1:
    #print("7")
    #turn(1,2)

def turn(sentido):
    Esquerda = leftEncoder.getValue()
    Direita= rightEncoder.getValue()
    firstLeft = Esquerda
    firstRight = Direita
    kpt = 0.1
    print(sentido)
    if sentido == 0 :
        setEsquerda = 2.41152
        setDireita = -2.00332
        S = 1
        print("direita")
    elif sentido == 1 :
       setEsquerda = -2.00332
       setDireita = 2.41152
       S = -1
       print("esquerda")    
    media = 1
    while (robot.step(timeStep) != -1 and media > 0.2):
        Esquerda = leftEncoder.getValue()
        Direita = rightEncoder.getValue()
        media =  (Direita - firstRight) - setDireita #semi pid so com proporcional - erro
        motor((S*(100/(1+(1/(media*kpt))))), -1* S*(100/(1+(1/(media*kpt))))) # semi pid de verdade
        print(media)
        #print("5")
    #print("6")
    motor(0,0)

    
def front(lsetpoint, lkp, lki, lkd):
    global I, P, D, e, pe
    e = distf()-lsetpoint #error
    P = e 
    I = e+I
    D = e - pe
    pid = P*lkp + I*lki + D*lkd 
    vel = (100/((1/(100*pid*pid))+1))*sign(pid)
    pe = e
    motor(vel,vel)

def inTest():#prototypes
    if whatColor() == "black":
        left = leftEncoder.getValue()
        print(left)
        
        while leftEncoder.getValue() - left >= -3.27188:
            motor(-50,-50)
            

        motor(0,0)


    
#print("preloop")
#print(timeStep)
while robot.step(timeStep) != -1:
    turn(0)
    break
    