from math import exp


def Sigmoid(x):
    return 1 / (1 + exp(-x))


def SigmoidDel(x):
    return exp(-x) / ((1 + exp(-x)) ** 2.0)


def tanh(x):
    return (exp(x) - exp(-x)) / (exp(x) + exp(-x))


def tanhDel(x):
    return 1 - (tanh(x) ** 2)


def relu(x):
    return max(0, x)


def reluDel(x):
    if x < 0:
        return 0
    else:
        return 1
