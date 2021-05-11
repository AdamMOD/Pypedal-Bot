import adafruit_ads1x15.ads1115
import adafruit_motor.servo
import busio
import numpy as np
import time
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from board import SCL, SDA
import serial
import adafruit_bno055


class Bot:
    def __init__(self):
        self.__i2cbus = busio.I2C(SCL, SDA)
        self.__uart = serial.Serial("/dev/serial0")

        self.imu = adafruit_bno055.BNO055_I2C(self.__i2cbus)



        self.kit = ServoKit(channels=16)
        self.pca = PCA9685(self.__i2cbus)
        self.pca.frequency = 330

        self.pca_servo_channels = np.array([0, 1, 4, 5])
        for channel in self.pca_servo_channels:
            self.kit.servo[channel].acuation_range = 180
            self.kit.servo[channel].set_pulse_width_range(900, 2100)

        self.servo_zero_angles = np.array([80.0, 65.0, 80.0, 70.0])
        self.servo_angle_flips = np.array([1, -1, -1, 1])
        self.servo_map_in_mins = np.array([17664, 9632, 8496, 18368])
        self.servo_map_in_maxs = np.array([8704, 18704, 17616, 9392])
        self.servo_map_out_mins = np.ones(4) * -60
        self.servo_map_out_maxs = np.ones(4) * 60

        self.ads = adafruit_ads1x15.ads1115.ADS1115(self.__i2cbus)
        self.ads.gain = 1
        self.ads.data_rate = 860
        ads_chan0 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P0)
        ads_chan1 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P1)
        ads_chan2 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P2)
        ads_chan3 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P3)
        self.ads_servo_channels = [ads_chan0, ads_chan1, ads_chan2, ads_chan3]

    def __map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def zero_servos(self):
        for servo in range(4):
            self.command_servo_angle(servo, 0)

    def command_servo_angle(self, servo, cmd):
        if(abs(cmd) < 61.):
            self.kit.servo[self.pca_servo_channels[servo]].angle = (
                self.servo_zero_angles[servo] + cmd * self.servo_angle_flips[servo]
            )
        else:
            print("Angle too big!")

    def shutdown(self):
        self.zero_servos()
        time.sleep(1)

    def read_servo_count(self, servo):
        count = self.ads_servo_channels[servo].value
        return count

    def read_servo_angle(self, servo):
        count = self.read_servo_count(servo)
        angle = self.__map(count, self.servo_map_in_mins[servo], self.servo_map_in_maxs[servo], self.servo_map_out_mins[servo], self.servo_map_out_maxs[servo])
        return angle

    def read_pitch(self):
        euler = self.imu.euler
        return euler[1]

    def read_pitch_rate(self):
        anglerate = self.imu.gyro
        return anglerate[1]
