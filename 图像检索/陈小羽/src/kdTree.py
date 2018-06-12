import numpy as np
import random as rand


class kdTreeNode(object):
    # pt  : the point in the origin list
    # dim : the dim that this Node is used for seperate the point
    # son : the sons on the KDTree
    def __init__(self, pt, dim=0, son=[None, None]):
        self.pt = pt
        self.dim = dim
        self.son = son


class KDTree(object):
    # dimNum : dimention
    # ptList : list of point(np.array) pair with an id
    def calcDel(self, ptList):
        mean = np.zeros(self.dimNum)
        for pt in ptList:
            mean += pt[0]
        mean /= len(ptList)
        delta2 = np.zeros(self.dimNum)
        for pt in ptList:
            delta = pt[0] - mean
            delta2 += delta * delta
        return delta2  # 这个地方除不除n都没有影响了

    def selectDim(self, ptList):
        delta = self.calcDel(ptList)
        maxx, maxwhe = -1, 0
        for i in range(self.dimNum):
            if(delta[i] > maxx):
                maxx, maxwhe = delta[i], i
        return maxwhe

    def genKeyFunc(self, type, dim=0):
        if(type == 'id'):
            def key(x):
                return x[1]
            return key
        elif(type == 'dim'):
            def key(x):
                return x[0][dim]
            return key

    def throw(self, curData, pivot, key):
        under, over, mid = [], [], []
        for item in curData:
            if key(item) < key(pivot):
                under.append(item)
            elif key(item) > key(pivot):
                over.append(item)
            else:
                mid.append(item)
        return under, over, mid

    # a nth_element() implement
    def select(self, data, n, key):
        curData = data
        N = n
        while True:
            pivot = rand.choice(curData)
            under, over, mid = self.throw(curData, pivot, key)
            if n < len(under):
                curData = under
            elif n < len(under) + len(mid):
                under, over, mid = self.throw(data, pivot, key)
                data = under + mid + over
                pivot = data[N]
                return data, pivot
            else:
                curData = over
                n -= len(under) + len(mid)
        pass

    def build(self, ptList):
        if len(ptList) == 0:
            return None
        n = len(ptList) - 1
        mid = n//2
        curDim = self.selectDim(ptList)
        # print(curDim, end=' ')
        ptList, pivot = self.select(ptList, mid, self.genKeyFunc('dim', curDim))
        return kdTreeNode(pivot, curDim, [self.build(ptList[:mid]), self.build(ptList[mid+1:])])

    def __init__(self, dimNum, ptList):
        self.dimNum = dimNum
        self.ptList = [[ptList[i], i] for i in range(len(ptList))]
        self.root = self.build(self.ptList)

    # p1, p2 <- np.array
    def distance(self, p1, p2):
        dt = p1 - p2
        return dt.dot(dt)  # 没有开方的必要

    def updateAns(self, ans, newAns, maxN, pt):
        ret = []
        p1, p2 = 0, 0
        while p1 < len(ans) or p2 < len(newAns):
            if p1 >= len(ans):
                ret.append(newAns[p2])
                p2 += 1
            elif p2 >= len(newAns):
                ret.append(ans[p1])
                p1 += 1
            else:
                if self.distance(ans[p1][0], pt) <= self.distance(newAns[p2][0], pt):
                    ret.append(ans[p1])
                    p1 += 1
                else:
                    ret.append(newAns[p2])
                    p2 += 1
        if len(ret) > maxN:
            ret = ret[0:maxN]
        return ret

        pass

    def query(self, pt, maxN, rt):
        ans = []
        if rt is None:
            return ans
        fst = 0 if pt[rt.dim] <= rt.pt[0][rt.dim] else 1
        sec = 1 - fst
        ans = self.updateAns(ans, self.query(pt, maxN, rt.son[fst]), maxN, pt)
        ans = self.updateAns(ans, [rt.pt], maxN, pt)
        dimDis = pt[rt.dim] - rt.pt[0][rt.dim]
        dimDis *= dimDis
        if self.distance(ans[-1][0], pt) > dimDis:
            ans = self.updateAns(ans, self.query(pt, maxN, rt.son[sec]), maxN, pt)
        return ans


class KDTreeTest(object):
    def __init__(self, dimNum, ptList):
        self.dimNum = dimNum
        self.ptList = [[ptList[i], i] for i in range(len(ptList))]

    def distance(self, p1, p2):
        dt = p1 - p2
        return dt.dot(dt)  # 没有开方的必要

    def update(self, ans, pt, p, maxN):
        ans = ans.copy()
        for i in range(len(ans)):
            if self.distance(pt, p[0]) < self.distance(pt, ans[i][0]):
                ans[i], p = p, ans[i]
        ans.append(p)
        if len(ans) > maxN:
            ans = ans[0:maxN]
        return ans

    def query(self, pt, maxN):
        ans = []
        for p in self.ptList:
            ans = self.update(ans, pt, p, maxN)
        return ans


# KDTree test


# rand.seed(10)
# f = open('main.in', 'r')
# sz = int(f.readline())
# n = int(f.readline())
# data = []
# for i in range(n):
#     str = f.readline().split(' ')
#     str = str[:-1]
#     str = [int(item) for item in str]
#     data.append(np.array(str))
#
# str = f.readline().split(' ')
# str = str[:-1]
# str = [int(item) for item in str]
# target = np.array(str)
#
# kd = KDTree(sz, data)
# print('finish building kdtree ...')
# test = KDTreeTest(sz, data)
# print('finish building test ...')
#
# maxN = 10
#
# ans_kd = kd.query(target, maxN, kd.root)
# ans_test = test.query(target, maxN)
#
# for i in range(maxN):
#     print(ans_kd[i][1], ans_test[i][1])
#     print(kd.distance(ans_kd[i][0], target), kd.distance(ans_test[i][0], target))
#
#     if kd.distance(ans_kd[i][0], target) != test.distance(ans_test[i][0], target):
#         exit(0)
#
# exit(1)
