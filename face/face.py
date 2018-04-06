#python 库
import sys
import os

#scipy 库
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#本地库
import PrincipalComponentsAnalisis as pca
import LinearRegression as linreg

def classify(sample, dataBase, distance):
    """
    int classify(sample, dataBase, simplify, distance)
    用于判断sample到底归属于dataBase中的哪一个类别
    sample 和 dataBase 中的数据都已经降维
    输入:
        sample : numpy.ndarray
        dataBase : [numpy.ndarray] (注意到这个数据的外层套了一个list)
        其中dataBase中的每一个ndarray表示了一个空间的基
        distance : 距离函数(用于求sample到每个空间的距离)
    输出:
        返回一个整数, 表示sampleOri属于的那个dataBaseOri项的编号
    """
    dis = [distance(sample, item) for item in dataBase]
    minx, minWhere = dis[0], 0 
    l = len(dis)
    for i in range(l):
        if dis[i] < minx:
            minx, minWhere = dis[i], i
    return minWhere

def getGreyPicture(data, picType):
    """
    输入:
        一幅图, data, 有RGB三色
    """
    if picType == 'pgm': #这种图本身就是灰度图
        return data * 1.0

    ret = data[:, :, 0] + data[:, :, 1] + data[:, :, 2] / 3.0
    return ret

def getSimple(data, simplify):
    data = simplify(data, data.shape[1], 10, data.shape[0]) #可以调整精度
    data = data.reshape([1, data.size])
    return data

def readPerson(Dir, picType, simplify):
    files = os.listdir(Dir)
    dirs = [Dir + '/' + File for File in files 
            if File[-len(picType) : ] == picType]
    faces = getSimple(getGreyPicture(mpimg.imread(dirs[0]), picType), simplify)
    l = len(dirs)
    for i in range(1, l):
        tmpFace = getSimple(getGreyPicture(mpimg.imread(dirs[i]), picType), simplify)
        faces = np.append(faces, tmpFace, axis = 0)
    return faces

def recognizeFace(picType, faceWhere, dataBaseWhere, simplify, distance):
    """
    输入: 
        picType : 样本图片格式
        faceWhere : 样本位置(文件)
        dataBaseWhere : dataBase位置(目录)
        simplify : 降维函数
        distance : 距离函数
    输出:
        样本属于的人的名字(dataBase中文件夹名)
    """
    face = getSimple(getGreyPicture(mpimg.imread(faceWhere), picType), simplify)
    names = os.listdir(dataBaseWhere) #读取数据库中的文件夹的名字
    names = [item for item in names if item[0] != '.']
    dirs = [dataBaseWhere + '/' + name for name in names]
    dataBase = [readPerson(Dir, picType, simplify) for Dir in dirs] #好像dir被占了
    ID = classify(face, dataBase, distance)
    return names[ID]

if __name__ == '__main__' : #程序入口
    ans = recognizeFace('pgm', './10.pgm', './att_faces',
            pca.PCA, linreg.linearRegression)
    print(ans)
