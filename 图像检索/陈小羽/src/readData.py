import numpy as np
from matplotlib import pyplot as plt

class dataReader(object):
    # rawIn       : other of rawIn
    # pt          : readpoint
    # magicNumber : magic number
    # itemNumber  : number of items
    def readInt(self):
        ret = 0
        for i in range(4):
            ret <<= 8
            ret += self.rawIn[i + self.pt]
        self.pt += 4
        return ret

    def readByte(self):
        ret = self.rawIn[self.pt]
        self.pt += 1
        return ret

    def __init__(self, path):
        self.path = path
        self.pt = 0
        dataIn = open(self.path, 'rb')
        self.rawIn = dataIn.read()
        self.magicNumber = self.readInt()
        self.itemNumber = self.readInt()
        self.rawIn = self.rawIn[self.pt:]
        self.pt = 0
        dataIn.close()

#test for dataReader
#data = dataReader('../database/t10k-images-idx3-ubyte')
#print(data.magicNumber, data.itemNumber)

class imageSetReader(dataReader):
    # magicNumber : magic number
    # itemNumber  : number of items
    # rowNumber   : number of rows
    # colNumber   : number of columns
    # imageSet    : the Set of the images
    def readImage(self):
        ret = []
        for i in range(self.rowNumber):
            row = []
            for j in range(self.colNumber):
                row.append(self.readByte())
            ret.append(row)
        ret = np.array(ret)
        return ret

    def __init__(self, path):
        dataReader.__init__(self, path)
        self.rowNumber = self.readInt()
        self.colNumber = self.readInt()
        self.imageSet = []
        for i in range(self.itemNumber):
            self.imageSet.append(self.readImage())

        del self.pt
        del self.rawIn

    def showImg(self, which):
        plt.imshow(self.imageSet[which])

#test for imageSetReader
#img = imageSetReader('../database/t10k-images-idx3-ubyte')
#img.showImg(0)

class labelSetReader(dataReader):
    # magicNumber : magic number
    # itemNumber  : number of items
    # labelSet    : the Set of the label
    def __init__(self, path):
        dataReader.__init__(self, path)
        self.labelSet = self.rawIn

        del self.rawIn
        del self.pt

    def showLabel(self, which):
        print(self.labelSet[which])

#test for imageSetReader
#label = labelSetReader('../database/t10k-labels-idx1-ubyte')
#label.showLabel(0)
