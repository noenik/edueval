# import matplotlib.pyplot as plt
import numpy

ans = []


def trimf(x, vect):
    """
    Triangle membership function
    (Do not use, only for testing purposes)
    :param x:
    :param vect:
    :return:
    """
    a = vect[0]
    b = vect[1]
    c = vect[2]

    k = (x - a) / (b - a)
    l = (c - x) / (c - b)

    return max(min(k, l), 0)


def trapmf(x, vect):
    """
    Trapezoid membership function
    (Do not use, only for testing purposes)
    :param x:
    :param vect:
    :return:
    """
    a = vect[0]
    b = vect[1]
    c = vect[2]
    d = vect[3]

    k = (x - a) / (b - a)
    n = (d - x) / (d - c)

    return max(min(min(k, n), 1), 0)


def halftrapmf(x, vect):
    """
    Half trapezoid membership function
    (Do not use, only for testing purposes)
    :param x:
    :param vect:
    :return:
    """
    a = vect[0]
    b = vect[1]

    k = (x - a) / (b - a)

    return min(k, 1)


def mf(x, vect):
    """
    Membership function.
    Triangle or trapezoid is determined by the length of the vector

    :param x: Value for which to calculate the membership value
    :param vect: Vector describing the membership function
    :return: Membership value
    """

    a = vect[0]
    b = vect[1]

    try:
        k = (x - a) / (b - a)
    except ZeroDivisionError:
        k = (x - a) / 0.001

    vect_len = len(vect)

    if vect_len == 2:
        return max(min(k, 1), 0)

    c = vect[2]
    if vect_len == 3:
        l = (c - x) / (c - b)
        return max(min(k, l), 0)
    elif vect_len == 4:
        d = vect[3]
        try:
            n = (d - x) / (d - c)
        except ZeroDivisionError:
            n = (d - x)/0.001
        return max(min(min(k, n), 1), 0)


def fuzzyfy(x):
    """
    Iterate over a set of vectors (x) and call the membership function (mf) for each of them

    :param x: Set of vectors of which to calculate using a membership function
    :return: Set of vectors which are the result of the calls to the membership function
    """
    returnvect = []
    start = x[0][0]
    end = x[-1][-1]

    for vect in x:
        res = []

        numrange = numpy.arange(start, end, 0.1)

        for i in numrange:
            res.append(float(mf(i, vect)))

        returnvect.append(res)

    return returnvect


# if __name__ == '__main__':
#     # Create a range from 0 to 10 with a step of 0.1
#     numrange = numpy.arange(0, 10, 0.1)
#
#     # Call the fuzzyfy function with a set of vectors
#     mat = fuzzyfy([[5, 2], [2, 4, 6, 8], [6, 8]])
#
#     # For each vector returned by the fuzzyfy function, plot it over the range
#     for r in mat:
#         plt.plot(numrange, r)
#
#     # Define x and y axis
#     plt.axis([0, 10, 0, 1.5])
#     # Show the plot
#     plt.show()
