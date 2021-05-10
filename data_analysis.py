import numpy as np
import pandas
import matplotlib.pyplot as plt

with open("data\\servotstsi2c50kbaud.csv") as f:
    servo_pd = pandas.read_csv(f)
    f.close()

print(servo_pd.head())
plt.title("Y vs U for SG995 Left Hip")
#plt.scatter(servo_pd["Time"], servo_pd["Lefthip"], color = "tab:red", label="Y_Left")
#plt.scatter(servo_pd["Time"], servo_pd["Righthip"], color = "tab:green", label="Y_Right")
plt.scatter(servo_pd["Time"], servo_pd["Pitch"], color = "tab:orange", label="Pitch")

#plt.scatter(servo_pd["Time"], servo_pd["Command"], color = "tab:blue", label="U")
plt.ylabel("Servo angle Y (degrees)")
plt.xlabel("Time (ms)")

plt.legend()
plt.show()