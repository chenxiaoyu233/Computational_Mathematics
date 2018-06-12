import numpy as np

class Neuron(object):
    def __init__(self):
        self.sonList = []
        self.weight = 0
        self.value = 0

class Layer(object):
    # unitShape : layer的形状
    # outFunc : 该层使用的非线性函数
    # outFuncDel : outFunc 的导函数
    def __init__(self, unitShape, outFunc, outFuncDel):
