import numpy as np
import pandas
import matplotlib.pyplot as plt
import scipy.signal

with open("data\\hip_sysiden\\sina20w16hip.csv") as f:
    servo_pd = pandas.read_csv(f)
    f.close()

print(servo_pd.head())
plt.title("Y vs U for SG995 Left Hip")
plt.scatter(servo_pd["Time"], servo_pd["Reading"], color = "tab:red", label="Y_Left")
plt.plot(servo_pd["Time"], scipy.signal.medfilt(servo_pd["Reading"], 21), color = "tab:green", label="Y_Left Filtered")
#plt.scatter(servo_pd["Time"], servo_pd["Righthip"], color = "tab:green", label="Y_Right")
#plt.scatter(servo_pd["Time"], servo_pd["Pitch"], color = "tab:orange", label="Pitch")
#plt.scatter(servo_pd["Time"], servo_pd["Pitchdot"], color = "tab:purple", label="Pitch_rate")
plt.plot(servo_pd["Time"], servo_pd["Command"], color = "tab:blue", label="U")

plt.ylabel("Angle (deg)")
plt.xlabel("Time (s)")

plt.legend()
plt.show()