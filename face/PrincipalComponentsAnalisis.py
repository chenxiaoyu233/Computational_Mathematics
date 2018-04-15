#本文件主要用于实现PCA, 用于对输入图片的降维

import numpy as np
from scipy import linalg

class eigPair(object):
    """
    用于储存特征值与特征向量的有序对, 构造比较函数
    最终参与排序
    """
    def __init__ (self, val, vec):
        """
        val : float64
        vec : numpy.array
        """
        self.val = abs(val) #需要按照绝对值的大小排序
        self.vec = vec
    def __lt__ (self, other):
        return self.val > other.val #按降序排列
    def __str__ (self): #用于调试输出
        return '[{}, {}]'.format(self.val, self.vec.__str__())

def PCA(data, inputCntDim, outputCntDim, cntVec, mode = 'ans'):
    """
    这个函数用于提供计算PCA的功能.
    输入: 
        data: 用于进行PCA处理的数据(二维矩阵)         (np.array)
        inputCntDim: 输入数据data中待处理的数据的维数 (int)
        outputCntDim: 输出数据中希望保留的维数        (int)
        cntVec: data中包含的独立的向量的个数          (int)
        mode: 希望得到的解的形式
              'ans' : 直接返回答案
              'func' : 返回转移矩阵
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
        具体实现时从0开始编号
    输出:
        一个矩阵, 包含和data相同的行数, 列数变为outputCntDim, 丢失尽量少测信息
    """
    data.dtype = 'float64' #确认类型
    #计算并剪去平均数
    mean = np.mean(data, axis = 0)
    for i in range(cntVec):
        data[i, :] -= mean

    #计算相关系数
    cov = np.cov(data, rowvar = False)
    
    #计算特征值与特征向量并排序
    eigenvalue, eigenvector = linalg.eig(cov)
    eigList = [eigPair(eigenvalue[i], eigenvector[:, i]) for i in range(inputCntDim)]
    eigList.sort()

    #选择前面outputCntDim个特征向量
    featureVec = eigList[0].vec
    for i in range(1, outputCntDim):
        featureVec = np.append(featureVec, eigList[i].vec)
    featureVec = featureVec.reshape([outputCntDim, inputCntDim]) #调整形状

    #得到PCA之后的结果
    def trans(data):
        return featureVec.dot(data.transpose()).transpose()

    if mode == 'ans': 
        return trans(data)
    elif mode == 'func':
        return featureVec, mean

def genTrans(func):
    def trans(data):
        for i in range(data.shape[0]):
            data[i, :] -= func[1]
        return func[0].dot(data.transpose()).transpose()
    return trans

if __name__ == '__main__': #用于测试
    data = np.array([[2.5, 2.4],
                     [0.5, 0.7],
                     [2.2, 2.9],
                     [1.9, 2.2],
                     [3.1, 3.0],
                     [2.3, 2.7],
                     [2.0, 1.6],
                     [1.0, 1.1],
                     [1.5, 1.6],
                     [1.1, 0.9]])
                     
    ans = PCA(data.copy(), data.shape[1], 1, data.shape[0], mode = 'func')
    func = genTrans(ans)
    ans = func(data)
    print(ans)
