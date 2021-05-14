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
    t_start = time.time()
    currtime = time.time() 
    dat_arr = []
    while(currtime - t_start < 10000):
        currtime = time.time()
        cmd = 20 * np.sin(float(currtime - t_start) * 16)
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
    t_start = time.time()
    currtime = time.time()
    dat_arr = [[0, 0, 0, 0, 0]]
    time.sleep(.01)
    while(currtime - t_start < 10):
        currtime = time.time()
        dt = ((currtime - t_start) - dat_arr[-1][0])
        #reading1 = mybot.read_servo_angle(1)
        reading0 = mybot.read_servo_angle(0)
        pitchnew = mybot.read_pitch()
        if(pitchnew is not None):
            if(len(dat_arr) == 1):
                pitchrate_der = 0
            else:
                pitchrate_der = (pitchnew - pitch)  / dt
            pitch = pitchnew + 0
            pitchrate = mybot.read_pitch_rate()
            state = np.array([reading0, pitch, pitchrate])
            if(abs(pitchrate_der) < 100):
                try:
                    #cmd = algorithms.pd_control(state)
                    cmd = algorithms.pid_control(state, dt)
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
balancetest()
mybot.shutdown()
