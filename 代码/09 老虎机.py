from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import time
import random

SAKS = SAKSHAT()#瑞士军刀扩展版组件
b = SAKS.buzzer#蜂鸣
c = 100#金额
d = 0#选的灯
l = 0#中奖的灯
x = 0#正在设置的数位
o = 1#是否静音
f = 0#连输次数
a = [0,0,0,0]#下注金额
mode = 0#模式
m = {0:1,1:0,2:3,3:2,4:5,5:4,6:7,7:6}#用以匹配同颜色的灯

def bzy(n):#把数字转成可调用的形式
    s = ''
    s += str(int(n/1000)) if n >= 1000 else '#'
    s += str(int(n/100%10)) if  n >= 100 else '#'
    s += str(int(n/10%10)) if  n >= 10 else '#'
    s += str(int(n%10))
    return s

def tty(a,x):#把四位数字的列表转为可调用的形式
    s = ''
    for i in range(3-x):
        s += '#'
    for i in range(x+1):
        s += str(a[x-i])
    return s

def num(a):#把四位数字的列表转为数字
    t = 0
    for i in range(4):
        t += a[i]*10**i
    return t

def win():#播放通关动画
    global o
    SAKS.digital_display.show('9999')
    if o:
        b.beep(1.5)
    t = 0
    while True:
        SAKS.ledrow.off()
        SAKS.ledrow.on_for_index(t)
        time.sleep(0.1)
        t += 1
        if t == 8:
            t = 0
    
def dip_switch_status_changed_handler(status):#触发拨码开关时运行
    global f,o,a,c,d,l,mode,x,bzytty
    if not status[0]:#当拨码开关1被触发且为开时：初始化所有数据
        c = 100
        d = 0
        l = 0
        x = 0
        o = 1
        f = 0
        a = [0,0,0,0]
        mode = 0
        SAKS.ledrow.off()
        SAKS.digital_display.show('#100')
    if not status[1]:#当拨码开关2被触发时：若为关则进入秘籍模式
        mode = 3
        bzytty = ''
        SAKS.ledrow.off()
        SAKS.digital_display.show('####')
    if status[1]:#当拨码开关2被触发时：若为开则回到正常模式并改变是否静音
        mode = 0
        if o:
            o = 0
        else:
            o = 1
        SAKS.digital_display.show(bzy(c))

def tact_event_handler(pin,status):#触发轻触开关时运行
    global f,o,a,c,d,l,mode,x,bzytty
    if pin == PINS.TACT_LEFT and status == True:#当左轻触开关被触发且为按下时：
        if mode == 1:
            #若在下注模式则给正在设置的数位+1
            a[x] += 1
            #若超过9或者超过可设置金额则变为0
            if a[x] == 10:
                a[x] = 0
            if len(str(c)) == x + 1:
                if str(a[x]) > str(c)[0]:
                    a[x] = 0
                if str(a[x]) == str(c)[0]:
                    t = 0
                    for i in range(x):
                        t += a[i]*10**i
                    if c % 10**x < t:
                        a[x] = 0
            SAKS.digital_display.show(tty(a,x))   
        if mode == 2:
            #若在选灯模式则选择下一个灯
            d += 1
            #若超过最后一个灯则变为第一个灯
            if d == 8:
                d = 0
            SAKS.ledrow.off()
            SAKS.ledrow.on_for_index(d)
            SAKS.digital_display.show(bzy(c))
        if mode == 3:
            #若为秘籍模式则记为输入一个0
            bzytty += '0'
            #若秘籍输入正确则金额+9000
            if bzytty == '100110':
                c += 9000
                
    if pin == PINS.TACT_RIGHT and status == True:#当右轻触开关被触发且为按下时：
        if mode == 0:#若为开奖模式则进入下注模式
            mode = 1
            SAKS.ledrow.off()
            SAKS.digital_display.show(tty(a,x))
        elif mode == 1:#若为下注模式检测是否可以继续设置下一数位
            t = 0
            for i in range(x+1):
                t += a[i]*10**i
            if len(str(c)) == x + 1 or (len(str(c)) == x + 2 and c % 10**(x+1) < t and str(c)[0] == '1'):#否则进入选灯模式
                mode = 2
                c -= num(a)
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(d)
                SAKS.digital_display.show(bzy(c))
            else:#是则进入下一数位的设置
                x += 1
                SAKS.digital_display.show(tty(a,x))
        elif mode == 2:#若为选灯模式则进入开奖模式
            mode = 0
            l = random.randint(0,7)#随机选出中奖的灯
            for i in range(41+l):
                time.sleep(-1/(i-41-l))
                SAKS.ledrow.off()
                SAKS.ledrow.on_for_index(i%8)
                if o:
                    b.beep(0.01)
            if l == d:#若选中同一灯则加10倍赌注
                f = 0
                c += 10*num(a)
                if c >= 10000:#若金额超过10000则播放通关动画
                    win()
                SAKS.digital_display.show(bzy(c))
                if o:
                    b.beep(1)
            elif l == m[d]:#若选中同一颜色灯则加5倍赌注
                f = 0
                c += 5*num(a)
                if c >= 10000:#若金额超过10000则播放通关动画
                    win()
                SAKS.digital_display.show(bzy(c))
                if o:
                    b.beep(0.3)
            else:
                f += 1
                if f == 10:#若连输10次则金额减半
                    f = 0
                    c = int(c/2)
                    if o:
                        b.beep(0.1)
                        time.sleep(0.1)
                if o:
                    b.beep(0.1)
                SAKS.digital_display.show(bzy(c))
            a = [0,0,0,0]
            x = 0
        else:
            bzytty += '1'

if __name__ == '__main__':
    SAKS.tact_event_handler = tact_event_handler
    SAKS.dip_switch_status_changed_handler = dip_switch_status_changed_handler
    SAKS.ledrow.off()
    SAKS.digital_display.show('#100')
    input()
