import numpy as np
import sys
sys.path.append('../')
from volestipy import *
from src.inner_ball import slow_inner_ball, fast_inner_ball

if __name__ == "__main__":

    m = 2
    n = 5

    A = np.zeros((2*n, n), dtype=np.float)
    A[0:n] = np.eye(n)
    A[n:] -=  np.eye(n,n, dtype=np.float)
    print("\n This is the A matrix: \n")
    print(A)

    b = np.ones(2*n, dtype=np.float)
    print("\n This is the vector b: \n")
    print(b)

    max_ball = slow_inner_ball(A,b)
    print("The center point of max ball is:")
    print(max_ball[0])
    print("The radius of max ball equals to:")
    print(max_ball[1])