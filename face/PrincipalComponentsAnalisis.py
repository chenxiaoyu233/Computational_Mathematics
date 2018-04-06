#本文件主要用于实现PCA, 用于对输入图片的降维

import numpy as np

def PCA(data, inputCntDim, outputCntDim, cntVec):
    """
    这个函数用于提供计算PCA的功能.
    输入: 
        data: 用于进行PCA处理的数据(二维矩阵)
        inputCntDim: 输入数据data中待处理的数据的维数
        outputCntDim: 输出数据中希望保留的维数
        cntVec: data中包含的独立的向量的个数
    输入矩阵的形式:
        /  x[1][1]         x[1][2]      ...    x[1][inputCntDim]    \\
        |  x[2][1]         x[2][2]      ...    x[2][inputCntDim]     |
        |    ...             ...        ...       ...                |
        \\x[cntVec][1]    x[cntVec][2]  ...   x[cntVec][inputCntDim] /
        <=>
        / Img[1]     \\
        | Img[2]     |
        |  ...       |
        \\Img[cntVec]/
    输出:
        一个矩阵, 包含和data相同的行数, 列数变为outputCntDim, 丢失尽量少测信息
     """
    print('test')
    pass

if __name__ == '__main__': #用于测试
    pass
