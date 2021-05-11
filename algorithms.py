import numpy as np

zero_pitch = 0.0

def pd_control(state):
    """State is in form righthip angle, pitch, pitch rate"""
    err = np.array([0, zero_pitch, 0]) - state
    K = np.array([0, 1, 0])
    return np.dot(err, K)