# coding=utf-8
# Led Puzzle-最少步数计算

# 二进制数i的从右往左第k位代表第k盏灯的开闭，1为开，0为关

leaststeps=[]  # 记录最少步数值的空列表

# 获取二进制数n的第k位
def getdig(n,k):
    return (n//(2**(k-1))) % 2

# 反转二进制数n的第k位
def revdig(n,k):
    if getdig(n,k) == 1:
        return n-2**(k-1)
    else:
        return n+2**(k-1)

# 根据已证明的数学结论，判断一个初始序列可否到达全亮状态
def able(n):
    sum = getdig(n,1)+getdig(n,2)+getdig(n,4)+getdig(n,5)+getdig(n,7)+getdig(n,8)
    if sum % 2 == 1:
        return 0
    return 1

# 实现游戏规定的操作
def alter(n,k):
    n=revdig(n,k)
    if k!=1:
        n=revdig(n,k-1)
    if k!=8:
        n=revdig(n,k+1)
    return int(n)

# 计算二进制数n确定的最小序列
def LeastStep(n):
    dis = [-1 for j in range(256)]
    dis[n] = 0
    get = False
    round = 0
    # 广度优先搜索
    new=False
    while not get:
        new=False
        for i in range(256):
            if dis[i] == round:
                for k in range(1,9):
                    if dis[alter(i, k)] == -1:
                        new=True
                        dis[alter(i, k)] = round+1  # 新到达的状态标记最小距离
        if not new:
            return -1
        round += 1
        if dis[255]>0:
            get=True  # 到达全亮状态，停止
    return dis[255]

for i in range(255):
    leaststeps.append(LeastStep(i))
leaststeps.append(0)
print(leaststeps)
