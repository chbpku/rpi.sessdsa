# coding=utf-8
# Led Puzzle

from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import time
import random
import math

# 预先求好的各状态最少步数，-1表示不可到达
Leaststeps=[3, -1, -1, 2, 3, -1, -1, 2, -1, 3, 4, -1, -1, 3, 4, -1, -1, 2, 3, -1, -1, 4, 3, -1, \
            2, -1, -1, 3, 2, -1, -1, 1, 3, -1, -1, 2, 3, -1, -1, 2, -1, 3, 4, -1, -1, 3, 4, -1, \
            -1, 2, 3, -1, -1, 4, 3, -1, 2, -1, -1, 3, 2, -1, -1, 1, -1, 3, 4, -1, -1, 5, 4, -1, \
            3, -1, -1, 4, 3, -1, -1, 2, 4, -1, -1, 3, 4, -1, -1, 3, -1, 4, 5, -1, -1, 4, 5, -1, \
            -1, 3, 4, -1, -1, 5, 4, -1, 3, -1, -1, 4, 3, -1, -1, 2, 4, -1, -1, 3, 4, -1, -1, 3, \
            -1, 4, 5, -1, -1, 4, 5, -1, -1, 2, 3, -1, -1, 4, 3, -1, 2, -1, -1, 3, 2, -1, -1, 1, \
            3, -1, -1, 2, 3, -1, -1, 4, -1, 5, 4, -1, -1, 3, 4, -1, -1, 4, 5, -1, -1, 4, 5, -1, \
            4, -1, -1, 3, 4, -1, -1, 3, 3, -1, -1, 4, 3, -1, -1, 2, -1, 3, 4, -1, -1, 5, 4, -1, \
            2, -1, -1, 3, 2, -1, -1, 1, -1, 2, 3, -1, -1, 4, 3, -1, -1, 3, 4, -1, -1, 3, 4, -1, \
            3, -1, -1, 2, 3, -1, -1, 2, 2, -1, -1, 1, 2, -1, -1, 3, -1, 4, 3, -1, -1, 2, 3, -1, \
            -1, 1, 2, -1, -1, 3, 2, -1, 1, -1, -1, 2, 1, -1, -1, 0]

# bool值状态转换
def switch(stat):
    if stat==False:
        return True
    else:
        return False

# 统计当前点亮的灯数
def lightcounter():
    lighted=0
    for index in range(8):
        if ledr.is_on(index):
            lighted+=1
    return lighted

# 将bool列表转化为整数，以便调用最少步数
def rowstat_to_int(rowstat):
    res=0
    for i in rowstat:
        res*=2
        if i==True:
            res+=1
    print(res)
    print(Leaststeps[res])
    return res

# 程序结束处理（计分与显示）
def end(status):
    SAKS.tact_event_handler=None
    if status==0:  # 失败
        lights=lightcounter()
        mark=5*lights
        digr.show("%d%d.00"%(mark//10,mark%10,))
        ledr.off()
        buz.beep(3)
        digr.off()
        input("Press 'ENTER' to exit")
        exit()
    elif status==1:  # 成功
        finishtime=time.time()
        usetime=finishtime-begintime
        stepdiff=actstep-best
        print(usetime)
        print(stepdiff)
        # 分段计算时间分
        if usetime>130:
            timemark=0
        elif usetime>30:
            timemark=130-usetime/10
        else:
            timemark=20-usetime/3
        print(timemark)
        # 计算步数分
        if stepdiff<=10:
            stepmark=20-stepdiff*2
        elif stepdiff>10:
            stepmark=0
        else:  # 步数比最小步数更少，将报错
            digr.show("9999")
            time.sleep(3)
            exit()
        print(stepmark)
        result =60+timemark+stepmark
        print(result)
        
        a=(math.floor(result))//10
        b=(math.floor(result))%10
        c=(math.floor(10*result))%10
        d=(math.floor(100*result))%10
        digr.show("%d%d.%d%d"%(a,b,c,d,))
        buz.beepAction(0.3,0.3,3)
        # 流水灯庆祝
        for round in range(20):
            for index in range(8):
                ledr.on_for_index(index)
                ledr.off_for_index((index-1)%8)
                time.sleep(0.02)
        digr.off()
        ledr.off()
        input("Press 'ENTER' to exit")
        exit()

# 触控开关事件处理
def tact(pin,status):
    global curdig,actstep
    if status==False:
        return
    # 左开关移动所控制的位置
    if pin==PINS.TACT_LEFT:
        curdig=(curdig+1)%8
        digr.show("%d%d#%d"%(actstep//10,actstep%10,curdig,))
    # 右开关实现规定操作一次
    elif pin==PINS.TACT_RIGHT:
        rowstat[curdig]=switch(rowstat[curdig])
        if curdig!=0:
            rowstat[curdig-1]=switch(rowstat[curdig-1])
        if curdig!=7:
            rowstat[curdig+1]=switch(rowstat[curdig+1])
        ledr.set_row(rowstat)
        actstep+=1
        if actstep>99:
            end(0)
            return
        digr.show("%d%d#%d"%(actstep//10,actstep%10,curdig,))
        if lightcounter()==8:
            end(1)
            return

SAKS=SAKSHAT()
ledr=SAKS.ledrow
tactr=SAKS.tactrow
digr=SAKS.digital_display
buz=SAKS.buzzer
# 开始提示
buz.beepAction(0.2,0.2,5)
ledr.on()
digr.show("0000")
time.sleep(3)
ledr.off()

# 生成puzzle
rowstat=[True]*8
steps=random.randrange(15,30)
for step in range(steps):
    dig=random.randrange(8)
    rowstat[dig]=switch(rowstat[dig])
    if dig!=0:
        rowstat[dig-1]=switch(rowstat[dig-1])
    if dig!=7:
        rowstat[dig+1]=switch(rowstat[dig+1])
best=Leaststeps[rowstat_to_int(rowstat)]
ledr.set_row(rowstat)
SAKS.tact_event_handler=tact
begintime=time.time()
digr.show("00#0")
curdig=0
actstep=0
# time.sleep(1000)
