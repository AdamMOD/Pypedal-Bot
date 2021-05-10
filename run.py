import time
import bot
import pandas

import adafruit_ads1x15.ads1115 as ADS
import adafruit_motor.servo
import busio
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from board import SCL, SDA

mybot = bot.Bot()

mybot.zero_servos()
time.sleep(1)

t_start = round(time.time() * 1000)
currtime = round(time.time() * 1000)

#print(t_start)

dat_arr = []

while(currtime - t_start < 1000):
    currtime = round(time.time() * 1000)
    cmd = 20 * np.sin(float(currtime - t_start) * 2 / 1000)
    mybot.command_servo_angle(1, cmd)
    mybot.command_servo_angle(0, cmd)
    reading1 = mybot.read_servo_angle(1)
    reading0 = mybot.read_servo_angle(0)
    dat_arr.append([currtime - t_start, cmd, reading0, reading1])


mybot.shutdown()

#print(dat_arr)
cols = ["Time", "Command", "Righthip", "Lefthip"]
df = pandas.DataFrame(dat_arr, columns = cols)
df.to_csv(r"data\servotsts.csv")
