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

#Motor
def motor(vel1,vel2):
        wheel1.setVelocity(vel1)
        wheel2.setVelocity(vel2)
def lwf():
    if s1.getValue() > s4.getValue():
        p = rightEncoder.getValue()
        while rightEncoder.getValue() < p+4.4:
            motor(0,2)
    elif s1.getValue() < s4.getValue():
        p = leftEncoder.getValue()
        while leftEncoder.getValue() < p+4.4:
            motor(2,0)
    else:
        p = leftEncoder.getValue()
        while leftEncoder.getValue() < p+5:
            motor(2,2)


#Encoders
leftEncoder = wheel1.getPositionSensor()
rightEncoder = wheel2.getPositionSensor()
leftEncoder.enable(timeStep)
rightEncoder.enable(timeStep)

#Color sensor
colorSensor = robot.getDevice("colour_sensor") # Step 2: Retrieve the sensor, named "colour_sensor", from the robot. Note that the sensor name may differ between robots)
colorSensor.enable(timeStep) # Step 3: Enable the sensor, using the timestep as the update rate


# Enable distance sensors N.B.: This needs to be done for every sensor
s1.enable(timeStep)
s2.enable(timeStep)
s3.enable(timeStep)
s4.enable(timeStep)
def distf():
    x = s2.getValue()
    y = s3.getValue()
    return (xy)/(2(x+y)*0.2588190451)
# Mini visualiser for the distance senors on the console


start = robot.getTime()


#Color
def whatColor():
        r = colorSensor.imageGetRed(image, 1, 0, 0)
        g = colorSensor.imageGetGreen(image, 1, 0, 0)
        b = colorSensor.imageGetBlue(image, 1, 0, 0)
        if r < 100 and g < 100 and b < 100 :
            return "black"
        if r > 200  and g > 200 and b < 200 and b > 100:
            return "yellow"
        if r > 200 and g > 200 and b > 200 and r != 255 and g != 255 and b != 255:
            return "white"
        if r == 255 and g == 255 and b == 255:
            return "checkpoint"






while robot.step(timeStep) != -1:
    image = colorSensor.getImage()

   # if s1.getValue() < 0.1:
    #    speed2 = max_velocity/2

    #if s4.getValue() < 0.1:
    #    speed1 = max_velocity/2

    #if s2.getValue() < 0.1:
    #    speed1 = max_velocity
    #    speed2 = -max_velocity


    lwf()
    print ("esquerda: " + str(s1.getValue())  + " frente: " + str(distf()) + " direita: " + str(s4.getValue()))
    #print("esquerda: " + str(leftEncoder.getValue()) + " direita: " + str(rightEncoder.getValue()))
    #print("r: " + str(r) + " g: " + str(g) + " b: " + str(b))
    r = colorSensor.imageGetRed(image, 1, 0, 0)
    g = colorSensor.imageGetGreen(image, 1, 0, 0)
    b = colorSensor.imageGetBlue(image, 1, 0, 0)

    #if leftEncoder.getValue() > 5.0:    #anda um ladrilho e para
        #motor(0,0)

    #if r > 200  and g > 200 and b < 200 and b > 100: