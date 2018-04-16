#python 库
import sys
import os
import pickle

#scipy 库
from PIL import Image
import numpy as np
from scipy import linalg

#本地库
import PrincipalComponentsAnalisis as pca
import LinearRegression as linreg

def classify(sample, dataBase, distance):
    """
    int classify(sample, dataBase, simpFunc, distance)
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
    dis = []
    for i in range(len(dataBase)):
        dis.append(distance(sample, dataBase[i]))
    minx, minWhere = dis[0], 0 
    l = len(dis)
    for i in range(l):
        if dis[i] < minx:
            minx, minWhere = dis[i], i
    return minWhere

def getPicture(Dir):
    """
    输入:
        一幅图的位置
    输出:
        一个灰度矩阵(1 x n)
        内部值为float64
        且归一化
    """
    data = Image.open(Dir)
    data = data.resize((20, 20)) #调整图片的大小
    data = np.asarray(data)
    data = data.astype('float64') #将所有输入的图片都转化为float64类型
    if len(data.shape) == 3: #这说明这个是一张彩图
        data = data[:, :, 0] + data[:, :, 1] + data[:, :, 2] / 3.0
    data.reshape([1, data.size])
    data = data / linalg.norm(data) #归一化
    return data.reshape([1, data.size])

def readPerson(Dir):
    """
    用于读取某个人的全部的数据集
    输入:
        Dir : 数据集目录 (str)
    输出:
        一个人的照片矩阵
        其中每一个照片为矩阵的一行
    """
    files = os.listdir(Dir)
    dirs = [Dir + '/' + File for File in files if File[0] != '.']
    faces = getPicture(dirs[0])
    l = len(dirs)
    for i in range(1, l):
        tmpFace = getPicture(dirs[i])
        faces = np.append(faces, tmpFace, axis = 0)
    return faces

def genPersonDir(dataBaseWhere):
    """
    用于生成dataBaseWhere的下级目录
    """
    names = os.listdir(dataBaseWhere) #读取数据库中的文件夹的名字
    names = [item for item in names if item[0] != '.'] #注意去掉隐藏文件
    names.sort();
    dirs = [dataBaseWhere + '/' + name for name in names]
    return names, dirs


def learningAllPerson(dataBaseWhere, simplify, fresh = False):
    """
    输入: 
        dataBaseWhere : dataBase位置(目录)
        simplify : 降维函数
        fresh : 是否需要更新之前的学习数据
    输出:
        无
    功能:
        生成一个转移矩阵, 存放在dataBaseWhere/.info中
        为每个人的照片集生成一个已经降维的矩阵, 存放在dataBaseWhere/Person/.info中
    """
    if os.path.exists(dataBaseWhere + '/' + '.info') and (not fresh):
        return

    dirs = genPersonDir(dataBaseWhere)[1]

    data = readPerson(dirs[0])
    for i in range(1, len(dirs)):
        data = np.append(data, readPerson(dirs[i]), axis = 0)

    output = open(dataBaseWhere + '/' + '.info', 'wb')
    simpFunc = simplify(data, data.shape[1], 40, data.shape[0], mode = 'func')
    pickle.dump(simpFunc, output)
    output.close()

    func = pca.genTrans(simpFunc)
    for Dir in dirs:
        curDir = Dir + '/' + '.info'
        output = open(curDir, 'wb')
        pickle.dump(func(readPerson(Dir)), output)
        output.close()



def recognizeFace(faceWhere, dataBaseWhere, distance):
    """
    输入: 
        faceWhere : 样本位置(文件)
        dataBaseWhere : dataBase位置(目录)
        保证dataBaseWhere中存放了各个不同的人的文件夹
        |-dataBaseWhere
            |-Person 1
            |-Person 2
            |-Person 3
            |...
            |-Person n
        distance : 距离函数
    输出:
        样本属于的人的名字(dataBaseWhere中文件夹名)
    """
    face = getPicture(faceWhere)
    names, dirs = genPersonDir(dataBaseWhere)

    dataBase = []
    for Dir in dirs:
        info = open(Dir + '/' + '.info', 'rb')
        dataBase.append(pickle.load(info))
        info.close()

    info = open(dataBaseWhere + '/' + '.info', 'rb')
    simpFunc = pca.genTrans(pickle.load(info))
    info.close()

    ID = classify(simpFunc(face), dataBase, distance)

    return names[ID]

if __name__ == '__main__' : #程序入口
    fs = False
    if len(sys.argv) >= 4 and sys.argv[3] == 'fresh':
        fs = True
    learningAllPerson(sys.argv[1], pca.PCA, fresh = fs)
    ans = recognizeFace(sys.argv[2], sys.argv[1], linreg.linearRegression)
    print (ans)
