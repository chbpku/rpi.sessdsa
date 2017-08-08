# coding=utf-8
# Led Puzzle-最少步数计算

# 二进制数i的从右往左第k位代表第k盏灯的开闭，1为开，0为关
leaststeps = []  # 记录最少步数值的空列表

# 获取二进制数n的第k位
def getdig(n, k):
    return (n // (2 ** (k - 1))) % 2

# 反转二进制数n的第k位
def revdig(n, k):
    if getdig(n, k) == 1:
        return n - 2 ** (k - 1)
    else:
        return n + 2 ** (k - 1)

# 实现游戏规定的操作
def alter(n, k):
    n = revdig(n, k)
    if k != 1:
        n = revdig(n, k - 1)
    if k != 8:
        n = revdig(n, k + 1)
    return int(n)

# 计算二进制数n确定的最小序列
def LeastStep():
    dis = [-1 for j in range(256)]
    dis[255]=0
    round = 0
    # 动态规划
    new = False
    while True:
        new = False
        for i in range(256):
            if dis[i] == round:
                for k in range(1, 9):
                    if dis[alter(i, k)] == -1:
                        new = True
                        dis[alter(i, k)] = round + 1  # 新到达的状态标记最小距离
        if not new:
            return dis
        round += 1

print(LeastStep())
