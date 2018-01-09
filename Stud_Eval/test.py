import json
import matlab.engine
import os
import numpy as np

A = matlab.double([[0.59, 0.35, 1.00, 0.66, 0.11, 0.08, 0.84, 0.23, 0.04, 0.24],
                   [0.01, 0.27, 0.14, 0.04, 0.88, 0.16, 0.04, 0.22, 0.81, 0.53],
                   [0.77, 0.69, 0.97, 0.71, 0.17, 0.86, 0.87, 0.42, 0.91, 0.74],
                   [0.73, 0.72, 0.18, 0.16, 0.50, 0.02, 0.32, 0.92, 0.90, 0.25],
                   [0.93, 0.49, 0.08, 0.81, 0.65, 0.93, 0.39, 0.51, 0.97, 0.61]])
#
# T = matlab.double([[0.7, 0.1, 0.1, 1.0, 0.7, 0.2, 0.7, 0.6, 0.4, 0.9],
#                    [1.0, 0.0, 0.9, 0.3, 1.0, 0.3, 0.2, 0.8, 0.0, 0.3],
#                    [0.0, 0.1, 0.0, 0.0, 0.9, 1.0, 0.2, 0.3, 0.1, 0.4],
#                    [0.2, 0.1, 0.0, 1.0, 1.0, 0.3, 0.4, 0.8, 0.7, 0.5],
#                    [0.0, 0.1, 1.0, 1.0, 0.6, 1.0, 0.8, 0.2, 0.8, 0.2]])
#
# C = matlab.double([[0.0, 0.85, 0.15, 0.0, 0.0],
#                    [0.0, 0.0, 0.33, 0.67, 0.0],
#                    [0.0, 0.0, 0.0, 0.69, 0.31],
#                    [0.56, 0.44, 0.0, 0.0, 0.0],
#                    [0.0, 0.0, 0.7, 0.3, 0.0]])
#
# I = matlab.double([[0.0, 0.0, 0.0, 0.0, 1.0],
#                    [0.0, 0.33, 0.67, 0.0, 0.0],
#                    [0.0, 0.0, 0.0, 0.15, 0.85],
#                    [1.0, 0.0, 0.0, 0.0, 0.0],
#                    [0.0, 0.07, 0.93, 0.0, 0.0]])


def run_evaluation(T, C, I, G):
    eng = matlab.engine.start_matlab()
    eng.addpath(os.path.dirname(os.path.abspath(__file__)))

    # A = matlab.double(A)
    T = matlab.double(T)
    C = matlab.double(C)
    I = matlab.double(I)
    G = matlab.double(G)

    return eng.main(A, T, C, I, G)


if __name__ == '__main__':
    # eng = matlab.engine.start_matlab()
    # eng.addpath(os.path.dirname(os.path.abspath(__file__)))
    print(A.transpose())
