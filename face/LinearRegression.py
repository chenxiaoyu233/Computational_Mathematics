#这个文件用于实现用多元线性回归

import numpy as np
from scipy import linalg

def linearRegression(y, A):
    """
    输入:
        y : numpy.ndarray
        A : numpy.ndarray
        需要保证y和A的列数相同(按照行向量的方式储存)
        y和A中的每一个行向量都是一张素材
    """
    dim = A.shape
    X = np.ones([1, dim[1]], dtype = 'float')
    X = np.append(X, A)
    X = X.reshape([dim[0]+1, dim[1]])
    b = linalg.inv(X.dot( X.transpose() ) + np.identity(dim[0]+1) * 1e-7).dot(X.dot( y.transpose() )) #加了一个单位矩阵, 保证可逆
    yPre = X.transpose().dot(b)
    dy = y.transpose() - yPre
    return linalg.norm(dy.transpose().dot(dy))

if __name__ == '__main__' : #测试
    y = np.array([[15.8, 16.0, 15.9, 16.2, 16.5, 16.3, 16.8, 17.4, 17.2]])
    A = np.array([[0, 1, 0, 1, 2, 0, 2, 3, 1],
                  [0, 0, 1, 1, 0, 2, 2, 1, 3]])
    linearRegression(y, A)

