# 按键输入模式代码
from sakshat import SAKSHAT
from sakspins import SAKSPins as PINS
import time
import random
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *

# GPIO采用BCM编码
GPIO.setmode(GPIO.BCM)

# LED灯对应的三个端口号
DS = 6
SHCP = 19
STCP = 13

# 初始化pygame
pygame.init()

# 创建一个pygame窗口
screen = pygame.display.set_mode((1024,768), 0, 32)

# LED灯功能的实现：

# 定义GPIO的初始化函数
def init():
    
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(STCP, GPIO.OUT)
    
    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.LOW)

# 通过writebit实现LED灯的状态控制
def writeBit(data):
    GPIO.output(DS, data)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)

LEDlist = [0x00,0x01,0x03,0x07,0x0f,0x1f,0x3f,0x7f,0xff]

# 传入一个16进制的数最为LED灯的状态
def writeByte(data):
    for i in range (0, 8):
        # 转成2进制
        writeBit((data >> i) & 0x01)
    #状态刷新信号
    GPIO.output(STCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.HIGH)


# 调用SAKS
SAKS = SAKSHAT()
presstimes = 0
ledposition = 0

def beforegame() : # 准备开始游戏，返回一个点击目标字符串

    global ok
    # 做一个3秒的倒计时
    for i in range(1,5):
        time.sleep(1)
        t = 4-i
        SAKS.digital_display.show('###'+str(t))
    # 随机产生一个由1或2组成的4位数字符串
    t = ''
    for i in range(4):
        t += str(random.randint(1,2))
    SAKS.digital_display.show(t)
    if not ok:
        ok = True

    return t


init()
# 得分记作score
score = 0
# 没有犯规记作ok
ok = True
# 目标记作target
target = beforegame()
# 时间未到记作flag
flag = True


inittime = time.time()
# inittime用作记录当前时间，用于计算两次点击时间差（仅在触控开关函数中使用）

def tact_event_handler(pin, status):    # 触控开关函数
    
    global __light_status, presstimes, score, target, ledposition, ok, inittime,flag

    if pin == PINS.TACT_RIGHT and status == True:       # 如果按下的是右键：
        nexttime = time.time()                          # 利用当前时间计算两次敲击时间差
        timecost = nexttime - inittime
        inittime = nexttime


        if timecost > 0.08 and flag:                    # 如果时间没到而且时间差多于0.08s
            if target[presstimes] == '2':               # 右键对应2说明按对了
                target = target.replace('2', '6', 1)    # 将按对的字符替换为6
                SAKS.digital_display.show(target)
                presstimes += 1                         # 正确点击次数+1


            else:   # 如果不是那就说明按错了
                
                SAKS.digital_display.show('2333')
                ok = False  # 按键错误则ok变为False
                writeByte(0x00) # 流水灯清空，等待1.5秒后显示分数
                time.sleep(1.5)
                SAKS.digital_display.show('%04d'%(score))
                time.sleep(2)
                score = 0   # 一切重置重新开始游戏
                presstimes = 0
                ledposition = 0
                target = beforegame()
                flag = True

    elif pin == PINS.TACT_LEFT and status == True:      # 按下左键的情况与按下右键的情况刚好对称
        nexttime = time.time()
        timecost = nexttime - inittime
        inittime = nexttime
        if timecost > 0.08 and flag:
            if target[presstimes] == '1':
                target = target.replace('1', '6', 1)
                SAKS.digital_display.show(target)
                presstimes += 1
            else:
                SAKS.digital_display.show('2333')
                ok = False
                writeByte(0x00)
                time.sleep(1.5)
                SAKS.digital_display.show('%04d'%(score))
                time.sleep(2)
                score = 0
                presstimes = 0
                ledposition = 0
                target = beforegame()
                flag = True
                
    if presstimes == 4 and flag:        # 如果正确点击次数为4而且时间还没到
        score += 1        # 说明玩家正确完成一组游戏，得分+1
        presstimes = 0        #部分重置，开始下一次游戏
        ledposition = 0
        ok = False
        time.sleep(0.5)
        SAKS.digital_display.show('####')
        writeByte(0x00)
        target = beforegame()
        flag = True

while True:     # 无限循环，主循环
    t1 = time.time()
    for i in range(8):
        t2 = time.time()
        while t2 - t1 < 0.2 * 0.9**score:        # 计时，只要时间到一定值就多往前一个小灯，其余时间一直等待鼠标输入
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:         # 如果输入为鼠标点击
                    if event.button == 1:
                        if flag:
                            if target[presstimes] == '1':       # 如果按下左键而且按对了
                                target = target.replace('1', '6', 1)         # 将按对的字符替换为6
                                SAKS.digital_display.show(target)
                                presstimes += 1                     # 正确点击次数+1
                            else:       # 如果按错了
                                SAKS.digital_display.show('2333')# 显示“2333”
                                ok = False                # 按键错误则ok变为False
                                writeByte(0x00)           # 流水灯清空，等待1.5秒后显示分数
                                time.sleep(1.5)
                                SAKS.digital_display.show('%04d'%(score))
                                time.sleep(2)
                                score = 0                # 一切重置重新开始游戏
                                presstimes = 0
                                ledposition = 0
                                target = beforegame()
                                for sdbg in pygame.event.get():
                                    shenmedoubuzuo = 0
                                event.button = 2
                                flag = True

                    # 按下右键的情况与按下左键的情况刚好对称
                    elif event.button == 3:
                        if flag:
                            if target[presstimes] == '2':
                                target = target.replace('2', '6', 1)
                                SAKS.digital_display.show(target)
                                presstimes += 1
                                
                            else:
                                SAKS.digital_display.show('2333')
                                ok = False
                                writeByte(0x00)
                                time.sleep(1.5)
                                SAKS.digital_display.show('%04d'%(score))
                                time.sleep(2)
                                score = 0
                                presstimes = 0
                                ledposition = 0
                                target = beforegame()
                                for sdbg in pygame.event.get():
                                    shenmedoubuzuo = 0
                                event.button = 2
                                flag = True
                    
            t2 = time.time()            # 不断刷新时间

            if presstimes == 4 and flag:       # 正确点击次数为4而且时间没到，
                score += 1 # 得分加一
                presstimes = 0  # 重置参数，重新开始游戏
                ledposition = 0
                ok = False
                time.sleep(0.5)
                SAKS.digital_display.show('####')
                writeByte(0x00)
                target = beforegame()
                for sdbg in pygame.event.get(): # 清空事件列表中剩下的操作
                    shenmedoubuzuo = 0

                flag = True

            
        ledposition += 1        # 流水灯流到下一个位置
        writeByte(LEDlist[ledposition])
        t1 = time.time()
        
    
        if ledposition == 8: # 如果这个时候发现时间到了
            writeByte(0xff)
            SAKS.digital_display.show('2333')# 显示“2333”
            flag = False #flag倒了
            time.sleep(1.5)
        
            SAKS.digital_display.show('%04d'%(score))# 显示最终的得分
            time.sleep(1.5)
        
            score = 0#重置参数重新开始游戏
            presstimes = 0
            ledposition = 0
            ok = False
            writeByte(0x00)
        
            target = beforegame()
            for sdbg in pygame.event.get():#清空event列表
                    shenmedoubuzuo = 0

            flag = True


SAKS.digital_display.show('####')#游戏结束，初始化树莓派扩展板
GPIO.cleanup()
