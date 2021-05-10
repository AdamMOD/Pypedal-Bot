import adafruit_ads1x15.ads1115
import adafruit_motor.servo
import busio
import numpy as np
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from board import SCL, SDA


class Bot:
    def __init__(self):
        self.__i2cbus = busio.I @ C(SCL, SDA)

        self.kit = ServoKit(channels=16)
        self.pca = PCA9685(i2c_bus)
        self.pca.frequency = 330

        self.pca_servo_channels = np.array([0, 1, 4, 5])
        for channel in self.pca_servo_channels:
            self.kit.servo[channel].acuation_range = 120
            self.kit.servo[channel].set_pulse_width_range(1000, 2000)

        self.servo_zero_angles = np.array([60.0, 60.0, 60.0, 60.0])
        self.servo_angle_flips = np.array([1, -1, -1, 1])

        self.ads = adafruit_ads1x15.ads1115.ADS1115(i2c_bus)
        self.ads.gain = 1
        ads_chan0 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P0)
        ads_chan1 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P1)
        ads_chan2 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P2)
        ads_chan3 = AnalogIn(self.ads, adafruit_ads1x15.ads1115.P3)
        self.ads_servo_channels = np.array([0, 1, 2, 3])

    def __map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def zero_servos(self):
        for servo in self.pca_servo_channels:
            self.command_servo_angle(servo, 0)

    def command_servo_angle(self, servo, cmd):
        self.kit[self.pca_servo_channels[servo]].angle = (
            servo_zero_angles[servo] + cmd * self.servo_angle_flips[servo]
        )

    def read_servo_angle(self, servo):
        count = self.ads_servo_channels[servo].value
        return count
