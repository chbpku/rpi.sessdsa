from sakshat import SAKSHAT
# from sakspins import SAKSPins as PINS
import time
import queue

#Declare the SAKS Board
SAKS = SAKSHAT()
soundToNum = {'C':1,'D':2,'E':3,'F':4,'G':5,'A':6,'B':7,'+':0}
temp = None
on_lights = queue.Queue()
stop = False
button_time = 0

def led_off_first(func):
    '''
    装饰器，先关
    :param func: 
    :return: 
    '''
    def wrapped(string):
        SAKS.ledrow.set_row([False,False,False,False,False,False,False,False])
        func(string)
    return func

def led_off_after_on(func):
    '''
    仅用于多线程，每次先关后开，隔半秒再关
    :param func: 
    :return: 
    '''
    def wrapped(string):
        func(string)
        time.sleep(0.5)
        temp = on_lights.get()
        SAKS.ledrow.off_for_index(temp)
        if temp == 0:
            temp = on_lights.get()
            SAKS.ledrow.off_for_index(temp)
        
    return wrapped

@led_off_after_on
def ledOn(string):
    #1-7显示音调，0显示升调
    if string[-1] == '+':
        temp = soundToNum[string[-2]]
        SAKS.ledrow.on_for_index(0)
        SAKS.ledrow.on_for_index(temp)
        on_lights.put(0)
        on_lights.put(temp)
    else:
        temp = soundToNum[string[-1]]
        SAKS.ledrow.on_for_index(temp)
        on_lights.put(temp)

def ledOff(string):
    if temp != None:
        SAKS.ledrow.off_for_index(0)
        SAKS.ledrow.off_for_index(temp)

def digitalPlay(string):
    if len(string) == 3:
        strToDisplay = string[0]+'#'+'.'+str(soundToNum[string[1]])+'.'+'#'
    else:
        strToDisplay = string[0]+'#'+str(soundToNum[string[1]])+'#'
    SAKS.digital_display.show(strToDisplay)

def displayTime(relative = True):
    '''
    由于不能及时显示数字造成混乱，我们决定用这个来作为秒表
    :return: 
    '''
    def seconds2minute(second:int):
        minute = str.zfill(str((second // 60) % 100), 2)
        second = str.zfill(str(second % 60), 2)
        return (minute, second)

    if relative:
        t = 0
        while not stop:
            # 多线程运行，半秒肯定不是半秒
            time.sleep(0.2)
            t += 1
            timeStr = '%s.%s'%seconds2minute(second=t)
            SAKS.digital_display.show(timeStr)
            time.sleep(0.2)
            timeStr = '%s%s' % seconds2minute(second=t)
            SAKS.digital_display.show(timeStr)
        cleanUp()

def display_count():
    '''
    展示按键次数的程序
    :return: 
    '''
    global button_time
    while not stop:
        SAKS.digital_display.show(str(button_time % 10000).zfill(4))
        time.sleep(0.1)


def cleanUp():
    SAKS.ledrow.off()
    SAKS.digital_display.show('####')
