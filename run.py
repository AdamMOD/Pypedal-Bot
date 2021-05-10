import time
import bot

import adafruit_ads1x15.ads1115 as ADS
import adafruit_motor.servo
import busio
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from board import SCL, SDA

mybot = bot.Bot()

maxcmd = np.array([90.0, 90, 90, 90])
for servo, cmd in enumerate(maxcmd):
    mybot.command_servo_angle(servo, cmd)
time.sleep(1)
for i in range(4):
    print(mybot.read_servo_angle(i))

"""
mincmd = maxcmd * -1
for servo, cmd in enumerate(mincmd):
    mybot.command_servo_angle(servo, cmd)
time.sleep(1)
for i in range(4):
    print(mybot.read_servo_angle(i))

mybot.zero_servos()
"""
"""
t_start = round(time.time() * 1000)
currtime = round(time.time() * 1000)

print(t_start)

dat_arr = []

while(currtime - t_start < 10000):
    currtime = round(time.time() * 1000)
    cmd = 60 + 20 * np.sin(float(currtime - t_start) * 2 / 1000)
    mybot.command_servo_angle(1, cmd)
    reading = mybot.read_servo_angle(1)
    dat_arr.append([currtime - t_start, cmd, reading])


print(dat_arr)
"""
