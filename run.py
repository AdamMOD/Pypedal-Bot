import time
import bot
import pandas
import algorithms

import adafruit_ads1x15.ads1115 as ADS
import adafruit_motor.servo
import busio
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from board import SCL, SDA

def measuretest(write=True):
    print("Starting servo move and read test")
    t_start = round(time.time() * 1000)
    currtime = round(time.time() * 1000)
    dat_arr = []
    while(currtime - t_start < 10000):
        currtime = round(time.time() * 1000)
        cmd = 20 * np.sin(float(currtime - t_start) * 2 / 1000)
        mybot.command_servo_angle(1, cmd)
        reading1 = mybot.read_servo_angle(1)
        dat_arr.append([currtime - t_start, cmd,reading1])
    mybot.shutdown()

    if(write):
        cols = ["Time", "Command","Lefthip"]
        df = pandas.DataFrame(dat_arr, columns = cols)
        df.to_csv(r"data/hip_sysiden/servotsts.csv")


def balancetest(write=True):
    print("Starting balance test")
    t_start = round(time.time() * 1000)
    currtime = round(time.time() * 1000)
    dat_arr = []
    while(currtime - t_start < 10000):
        newtime = round(time.time() * 1000)
        #reading1 = mybot.read_servo_angle(1)
        reading0 = mybot.read_servo_angle(0)
        pitchnew = mybot.read_pitch()
        if(pitchnew is not None):
            if(len(dat_arr) == 0):
                pitchrate_der = 0
            else:
                pitchrate_der = 1000 * (pitchnew - pitch)  / (newtime - currtime)
            pitch = pitchnew + 0
            currtime = newtime + 0
            pitchrate = mybot.read_pitch_rate()
            state = np.array([reading0, pitch, pitchrate])
            if(abs(pitchrate_der) < 100):
                try:
                    cmd = algorithms.pd_control(state)
                    mybot.command_servo_angle(1, cmd)
                    mybot.command_servo_angle(0, cmd)
                except:
                    cmd = 0
            else:
                    cmd = 0
        else:
            cmd = 0
        dat_arr.append([currtime - t_start, cmd, reading0, pitch, pitchrate])
    mybot.shutdown()

    if(write):
        cols = ["Time", "Command", "Righthip", "Pitch", "Pitchdot"]
        df = pandas.DataFrame(dat_arr, columns = cols)
        df.to_csv(r"data/runtst.csv")


mybot = bot.Bot()

mybot.zero_servos()
time.sleep(1)
measuretest()
mybot.shutdown()
