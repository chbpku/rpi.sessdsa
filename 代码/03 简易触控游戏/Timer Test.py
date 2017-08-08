#时间估计小游戏
#游戏介绍：游戏开始后，数码管会显示出一个时间，随后蜂鸣器响起，玩家在蜂鸣器响起后经过指定时间以后按下按键，在三次游戏后数码管上会显示玩家最终得分，误差越小得分越高
from sakshat import SAKSHAT
import time
import random
import math

def mark(errorpc):#根据估计误差计算分数
    if errorpc>0.5:
        return 0
    elif errorpc>0.25:
        return 120-240*errorpc
    elif errorpc>0.1:
        return 85-100*errorpc
    else:
        return 100-150*errorpc

def tact(pin,status):#设置按键动作
    if status:
        endtime=time.time()                                    #记录按下按键的时刻
        yourtime=endtime-starttime                             #用按下按键的时间减去蜂鸣器响起的时间作为估计时间
        print(yourtime)
        a=(math.floor(yourtime))//10                           #算出估计时间各位数字
        b=(math.floor(yourtime))%10
        c=(math.floor(10*yourtime))%10
        d=(math.floor(100*yourtime))%10
        digr.show("%d%d.%d%d"%(a,b,c,d,))                     #在数码管上显示估计时间
        marklist.append(mark(abs(yourtime-acqtime)/acqtime))   #将本次游戏的结果计入结果列表
        time.sleep(1)
        digr.off()

SAKS=SAKSHAT()
ledr=SAKS.ledrow
tactr=SAKS.tactrow
digr=SAKS.digital_display
buz=SAKS.buzzer

#蜂鸣器响五声，LED灯全亮，数码管显示0000,3秒后一起熄灭，提醒玩家游戏开始
buz.beepAction(0.2,0.2,5)
ledr.on()
digr.show("0000")
time.sleep(3)
ledr.off()

acqlist=[5,6,7,8,10,12,15,18,24,30]                           #设置要求时间的列表
marklist=[]                                                   #创建记录结果的列表
for round in range(3):#进行3次游戏
    acqtime=acqlist[random.randrange(10)]                     #在要求时间的列表里随机选取一个作为本次游戏的要求时间
    digr.show("%d%d.00"%(acqtime//10,acqtime%10,))           #显示本次游戏要求的时间
    time.sleep(2)                                             #2秒后蜂鸣器响起
    buz.beep(0.3)
    starttime=time.time()                                     #记录开始时间
    SAKS.tact_event_handler=tact                              #开始按键操作
    time.sleep(acqtime*1.5)                                   #等待玩家按下按键
    SAKS.tact_event_handler=None                             #停止按键操作

while len(marklist)<3:                                       #若无操作则自动记为0分
    marklist.append(0)
print(marklist)
average=(marklist[0]+marklist[1]+marklist[2])/3               #计算3次结果的平均值
a=(math.floor(average))//10                                   #计算平均结果的各位数字
b=(math.floor(average))%10
c=(math.floor(10*average))%10
d=(math.floor(100*average))%10
digr.show("%d%d.%d%d"%(a,b,c,d,))                           #在数码管显示平均结果
if average>60:                                               #不同位置的LED灯根据结果的好坏亮起
    ledr.on_for_index((math.floor(average)-60)//5)
time.sleep(5)                                                #停止3秒后全部熄灭游戏结束
digr.off()
ledr.off()
