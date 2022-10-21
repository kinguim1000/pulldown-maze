from turtle import left
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

#qual é o valor base?

#Girar uma volta para esquerda
    # if distf() <= 0.04167736680014455: 
    #    motor(0, 0)


#Color sensor
colorSensor = robot.getDevice("colour_sensor") # Step 2: Retrieve the sensor, named "colour_sensor", from the robot. Note that the sensor name may differ between robots)
colorSensor.enable(timeStep) # Step 3: Enable the sensor, using the timestep as the update rate
#colorUpdate
def color ():
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
    return (x*y)/(2*(x+y)*0.2588190451)
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
#print("preloop")
vel = 50
kpR = 0.5 #prop da rotação
kp = 1.5 #constante de prop
ki = 0 #constante de integral
kd = 0 #constante de derivada
I = 0 #integral
pe = 0 #anterior (previous error)
setpoint = 0.04 #ponto que queremos
while robot.step(timeStep) != -1:
    #e = distf()-setpoint #error
    #P = e 
    #I = e+I
    #D = e - pe
    #pid = P*kp + I*ki + D*kd 
    #vel = (100/((1/(100*pid*pid))+1))*sign(pid)
    #pe = e
    #motor(vel,vel)
    #print(e)
    motor(-50,50)
    media = (abs(leftEncoder.getValue()) + abs(rightEncoder.getValue()))/2
    # print(media)
   # off = abs(abs(leftEncoder.getValue()) - media) #< ou > - media = diferença dos enc
   # print(off)
   # motor(vel + off * kpR * sign(rightEncoder.getValue()) , vel + off * kpR * sign(leftEncoder.getValue()))
    #motor(vel + 0.4082 * sign(rightEncoder.getValue()) , vel + 0.4082 * sign(leftEncoder.getValue()))
    
    if (leftEncoder.getValue() >= 2.41152 and rightEncoder.getValue() <= -2.00332) or (rightEncoder.getValue() >= 2.41152 and leftEncoder.getValue() <= -2.00332):
        motor(0,0)
    if whatColor() == "black":
        print("igor")
    
    #print(str(leftEncoder.getValue()) + "     " + str(rightEncoder.getValue()))
    #print(distf())
    #print("entrou no loop")
    #O = gps.getValues()[2]
    #image = colorSensor.getImage()
    
   # if s1.getValue() < 0.1:
    #    speed2 = max_velocity/2

    #if s4.getValue() < 0.1:
    #    speed1 = max_velocity/2

    #if s2.getValue() < 0.1:
    #    speed1 = max_velocity
    #    speed2 = -max_velocity

    #x = gps.getValues()[0] # Step 4: Use the getValues() function to get the sensor readings
    #y = gps.getValues()[1] # Note that the gps returns a list of 3 values for x, y, z, position
    #z = gps.getValues()[2]
    #Px = abs(Px) - abs(x)
    #Py = abs(Py) - abs(y)
    #Pz = abs(Pz) - abs(z)
    #while rightEncoder.getValue() < 0.20096:
    #    motor(1,1)
    #motor(0,0)
    #break
    #print("GGGGG")
    #o = gps.getValues()[2]
    #while abs(O)+0.3 > abs(z):
    #    z = gps.getValues()[2]
    #    motor(1,1)
    #    print("fffffff")
    #print(rightEncoder.getValue())
    #break
    #print("x: " + str(Px) + " y: " + str(Py) + " z: " + str(Pz))
    #print ("esquerda: " + str(s1.getValue())  + " frente: " + str(distf()) + " direita: " + str(s4.getValue()))
    #print("esquerda: " + str(leftEncoder.getValue()) + " direita: " + str(rightEncoder.getValue()))
    #print("r: " + str(r) + " g: " + str(g) + " b: " + str(b))
    

    #if leftEncoder.getValue() > 5.0:    #anda um ladrilho e para
        #motor(0,0)

    #if r > 200  and g > 200 and b < 200 and b > 100:
