# coding=utf-8
# 反应测试游戏
# 游戏介绍：游戏开始后，蜂鸣器会随机响起，玩家在听到声音后立刻按下按键，从而测试玩家的反应速度，
# 在三次游戏后数码管上会显示玩家最终得分，反应速度越快得分越高
from sakshat import SAKSHAT
import time
import random
import math

SAKS=SAKSHAT()
buz=SAKS.buzzer
ledr=SAKS.ledrow
digr=SAKS.digital_display
tactr=SAKS.tactrow

# 蜂鸣器响五声，LED灯全亮，数码管显示0000,3秒后一起熄灭，提醒玩家游戏开始
buz.beepAction(0.2,0.2,5)
ledr.on()
digr.show("0000")
time.sleep(3)
ledr.off()
digr.off()


def tact(pin,status):#设置按键动作
    if status:
        actt=time.time()                         #记录按下按键的时刻
        gap=actt-prest                           #用按下按键的时间减去蜂鸣器响起的时间作为反应时间
        print(gap)
        a=(math.floor(gap))%10                   #算出反应时间各位数字
        b=(math.floor(10*gap))%10
        c=(math.floor(100*gap))%10
        d=(math.floor(1000*gap))%10
        digr.show("%d.%d%d%d"%(a,b,c,d,))      #在数码管上显示反应时间
        time.sleep(1)
        result=a+0.1*b+0.01*c+0.001*d
        resultlst.append(mark(result))           #将本次游戏的结果计入结果列表
        digr.off()                               #熄灭数码管


def mark(gap):#设置计分方式
    if gap>=0.5:
        return 0
    elif gap>=0.3:
        return 150-300*gap
    elif gap>=0.18:
        return 135-250*gap
    else:
        return 100-55*gap


SAKS.tact_event_handler=tact                     #开始按键操作

resultlst=[]                                     #创建记录结果的列表
for round in range(3): #进行3次游戏
    beept=3+random.randrange(7)                  #随机设置一个大于3秒的等待时间
    time.sleep(beept)
    prest=time.time()                            #记录下开始时刻
    buz.beep(0.03)                               #蜂鸣器响起
time.sleep(3)

SAKS.tact_event_handler=None                    #停止按键操作
print(resultlst)
average=(resultlst[0]+resultlst[1]+resultlst[2])/3 #计算3次结果的平均值
a=(average//10)%10                              #计算平均结果的各位数字
b=(math.floor(average))%10
c=(math.floor(10*average))%10
d=(math.floor(100*average))%10
digr.show("%d%d.%d%d"%(a,b,c,d,))             #在数码管显示平均结果
if average>=60:                                #不同位置的LED灯根据结果的好坏亮起
    ledr.on_for_index((math.floor(average)-60)//5)
time.sleep(3)                                  #停止3秒后全部熄灭游戏结束
ledr.off()
digr.off()





