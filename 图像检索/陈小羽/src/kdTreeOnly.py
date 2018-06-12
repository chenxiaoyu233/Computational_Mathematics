import readData as rd
import kdTree as kdt

testSet = rd.imageSetReader('../database/t10k-images-idx3-ubyte', 100)
trainSet = rd.imageSetReader('../database/train-images-idx3-ubyte', 1000)
print('data reading finish ...')

sz = trainSet.colNumber * trainSet.rowNumber

testSet.imageSet = testSet.imageSet[20].reshape(sz)
trainSet.imageSet = [image.reshape(sz) for image in trainSet.imageSet]
print('data trasform finish ...')

kd = kdt.KDTree(sz, trainSet.imageSet)
print('kd-tree build finish ...')

ans = kd.query(
    testSet.imageSet,
    10,
    kd.root
)


def my_print(mat):
    for i in range(28):
        for j in range(28):
            print("%3.0f" % mat[i][j], end=' ')
        print('')
    print('')


print([item[1] for item in ans])
my_print(testSet.imageSet.reshape([28, 28]))
for i in range(10):
    my_print(ans[i][0].reshape([28, 28]))
