import numpy as np

zero_pitch = 0.0
I_term = 0
I_gain = 1

def pd_control(state):
    """State is in form righthip angle, pitch, pitch rate"""
    err = np.array([0, zero_pitch, 0]) - state
    K = np.array([.1, 1.5, 0])
    return np.dot(err, K)


def pid_control(state, dt):
    """State is in form righthip angle, pitch, pitch rate"""
    state = raw_read_to_incline(state)
    err = np.array([zero_pitch, 0]) - state
    I_term = I_term + dt * err[1]
    K = np.array([1, 0, 0])
    return np.dot(err, K) + I_gain * I_term


def raw_read_to_incline(state):
    return np.array([state[0]+state[1], state[2]])