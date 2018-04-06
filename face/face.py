#scipy 库
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#本地库
import PrincipalComponentsAnalisis as pca

def classify(sample, dataBase, distance):
    """
    int classify(sample, dataBase)
    用于判断sample到底归属于dataBase中的哪一个类别
    这里的sample和dataBase都是已经降维过后的数据
    输入:
        sample : numpy.ndarray
        dataBase : [numpy.ndarray] (注意到这个数据的外层套了一个list)
        其中dataBase中的每一个ndarray表示了一个空间的基
        distance : 距离函数(用于求sample到每个空间的距离)
    输出:
        返回一个整数, 表示sample属于的那个dataBase项的编号
    """
    dis = [distance(sample, item) for item in dataBase]
    minx, minWhere = dis[0], 0
    l = len(dis)
    for i in range(l):
        if dis[i] < minx : 
            minx, minWhere = dis[i], i
    return minWhere

if __name__ == '__main__' : #程序入口
    pass
