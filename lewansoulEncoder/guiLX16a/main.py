import serial
import lewansoul_lx16a

SERIAL_PORT = '/dev/ttyUSB0'

controller = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1),
)

# control servos directly
controller.move(1, 200) # move servo ID=1 to position 100

# or through proxy objects
servo1 = controller.servo(1)

servo1.move(100)

# synchronous move of multiple servos
servo1.move_prepare(300)
controller.move_start()