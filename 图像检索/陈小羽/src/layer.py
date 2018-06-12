

class Neuron(object):
    # sonList : 孩子列表 [[儿子节点, weight]]
    # weight : [w, dw] -> parameter
    # delta : d(loss) / d(value)
    def __init__(self):
        self.sonList = []
        self.value = None
        self.delta = 0


class Layer(object):
    # shape : layer的形状, [x, y, z] / [通道数, 行数, 列数]
    # outFunc : 该层使用的非线性函数
    # outFuncDel : outFunc 的导函数
    # inputs : 上一层神经元
    # neuronList : 神经元列表, 二维list
    def genList(self, shape, F):
        List = []
        for i in range(shape[0]):
            tmp1 = []
            for j in range(shape[1]):
                tmp2 = []
                for k in range(shape[2]):
                    tmp2.append(F())
                tmp1.append(tmp2)
            List.append(tmp1)
        return List

    def buildNeuronList(self):
        self.neuronList = self.genList(self.shape, Neuron)

    def buildOffset(self):
        self.offset = []
        for i in range(self.shape[0]):
            self.offset.append([0, 0])

    def __init__(self, shape, outFunc, outFuncDel, inputs=None):
        self.buildOffset()
        self.inputs = inputs
        self.shape = shape
        self.outFunc = outFunc
        self.outFuncDel = outFuncDel
        self.buildNeuronList()
        # buildConnection

    def buildParameterBase(self, shape):
        self.parameter = self.genList(shape, lambda: [0, 0])

    def loadParameterBase(self, shape, par):
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    self.parameter[i][j][k][0] = par[i][j][k][0]
                    self.parameter[i][j][k][1] = par[i][j][k][1]

    def BPAlgorithmUpdate(self, rt, offset):
        for son in rt.sonList:
            son[0].delta += rt.delta * self.outFuncDel(rt.value) * son[1][0]
            son[1][1] += rt.delta * self.outFuncDel(rt.value) * son[0].value
            offset[1] += rt.delta * self.outFuncDel(rt.value)

    def BPAlgorithmUpdateLayer(self):
        for i in self.shape[0]:
            for j in self.shape[1]:
                for k in self.shape[2]:
                    self.BPAlgorithmUpdate(self.neuronList[i][j][k], self.offset[i])

    def BPAlgorithmUpdateLayerREC(self):
        self.BPAlgorithmUpdateLayer()
        if self.inputs is None:
            return
        else:
            self.inputs.BPAlgorithmUpdateLayerREC()

    def nodeValueUpdate(self, rt, offset):
        for son in rt.sonList:
            rt.value += son[0].value * son[1][0]
            son[1][1] = 0
        rt.value -= offset[0]
        rt.value = self.outFunc(rt.value)
        rt.delta = 0

    def nodeValueUpdateLayer(self):
        for i in self.shape[0]:
            self.offset[i][1] = 0
            for j in self.shape[1]:
                for k in self.shape[2]:
                    self.nodeValueUpdate(self.neuronList[i][j][k], self.offset[i])

    def nodeValueUpdateLayerREC(self):
        if self.inputs is None:
            return
        else:
            self.inputs.nodeValueUpdateLayerREC()
            self.nodeValueUpdateLayer()

    def genParameterList(self):
        lst = []
        for x in self.offset:
            lst.append(x)
        for x in self.parameter:
            for y in x:
                for z in y:
                    lst.append(z)
        if self.inputs is None:
            return lst
        else:
            return lst + self.inputs.genParameterList()


class convLayer(Layer):
    # kernelShape : 卷积核的形状 [x, y] / [行数(奇数), 列数(奇数)]
    # parameter :  参数列表
    def buildLinkIt(self):
        offset = [(item-1)//2 for item in self.kernelShape]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for k in range(self.shape[2]):
                    x = j + offset[0]
                    y = k + offset[1]
                    for dx in range(self.kernelShape[0]):
                        for dy in range(self.kernelShape[1]):
                            sx = x + dx - offset[0]
                            sy = y + dy - offset[1]
                            for to in range(self.inputs.shape[0]):
                                self.neuronList[i][j][k].sonList.append(
                                    [self.inputs[to][sx][sy], self.parameter[i][dx][dy]]
                                )

    def buildParameter(self):
        self.buildParameterBase(
            [self.shape[0], self.kernelShape[0], self.kernelShape[1]]
        )

    def loadParameter(self, par):
        self.loadParameterBase(
            [self.shape[0], self.kernelShape[0], self.kernelShape[1]], par
        )

    def __init__(self, shape, outFunc, outFuncDel, kernelShape, inputs=None):
        Layer.__init__(shape, outFunc, outFuncDel, inputs)
        self.kernelShape = kernelShape
        self.buildParameter()
        self.buildLinkIt()


class poolLayer(Layer):
    # kernelShape : 卷积核的形状 [x, y] / [行数(奇数), 列数(奇数)]
    def buildLinkIt(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for k in range(self.shape[2]):
                    for to in range(self.inputs.shape[0]):
                        x = i * self.kernelShape[0]
                        y = j * self.kernelShape[1]
                        for dx in range(self.kernelShape[0]):
                            for dy in range(self.kernelShape[1]):
                                sx = x + dx
                                sy = y + dy
                                self.neuronList[i][j][k].sonList.append(
                                    [self.inputs[to][sx][sy], self.parameter[i][dx][dy]]
                                )

    def buildParameter(self):
        self.buildParameterBase(
            [self.shape[0], self.kernelShape[0], self.kernelShape[1]]
        )

    def loadParameterBase(self, par):
        self.loadParameterBase(
            [self.shape[0], self.kernelShape[0], self.kernelShape[1]], par
        )

    def __init__(self, shape, outFunc, outFuncDel, kernelShape, inputs=None):
        Layer.__init__(shape, outFunc, outFuncDel, inputs)
        self.kernelShape = kernelShape
        self.buildParameter()
        self.buildLinkIt()


class fcLayer(Layer):
    def buildLinkIt(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for k in range(self.shape[2]):
                    for to in range(self.inputs.shape[0]):
                        for dj in range(self.inputs.shape[1]):
                            for dk in range(self.inputs.shape[2]):
                                self.neuronList[i][j][k].sonList.append(
                                    [self.inputs[to][dj][dk], self.parameter[i][dj][dk]]
                                )

    def buildParameter(self):
        self.buildParameterBase(
            [self.shape[0], self.inputs.shape[1], self.inputs.shape[2]]
        )

    def loadParameterBase(self, par):
        self.loadParameterBase(
            [self.shape[0], self.inputs.shape[1], self.inputs.shape[2]], par
        )

    def __init__(self, shape, outFunc, outFuncDel, inputs=None):
        Layer.__init__(shape, outFunc, outFuncDel, inputs)
        self.buildParameter()
        self.buildLinkIt()
