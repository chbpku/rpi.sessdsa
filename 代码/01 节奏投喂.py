from sakshat import SAKSHAT
from sakshat.sakspins import SAKSPins as PINS
from datetime import timedelta
import threading,time,sched,random,datetime
from threading import Timer#导入各种需要用到的模块
SAKS=SAKSHAT()
timelist=[]
ledlist=[]#建立基本的用于存储的列表和字符串
sled=''

def tact_event_handler(pin,status):#该函数表示当轻触按钮状态改变时，对应要完成的指令
    global timelist
    global ledlist
    global tlist
    global sled#这里我们把所有在引用函数里用到的存储列表全局化
    ######################################################################输入阶段############################################################
    if pin == PINS.TACT_LEFT and status == True:#当左轻触按钮被按下（需要注意的是，对于轻触按钮来讲，按下和松开都是状态改变，我们只以按下计次）
        timelist.append(datetime.datetime.now())#使用datetime记录当前时间点
        SAKS.buzzer.beep(0.05)                  #蜂鸣器在轻触按钮按下时鸣叫0.05秒以与体验者互动
        sled=str(random.randrange(0,8))+sled    #与此同时，生成与按下次数相同长度的LED亮起随机顺序表,以字符串形式存储
        
    ######################################################################处理阶段############################################################
    elif pin == PINS.TACT_RIGHT and status == True:#当右轻触按钮被按下，输入过程结束
        tem=timelist[0]
        timelist=[(i-tem) for i in timelist]            #首先将时间点列表中的时间点转换为timedelta 格式，表示与第一下按下的时间间隔
        tlist=[(i.seconds + i.microseconds/ 1000000) for i in timelist]#转化为秒为单位的数字         
        sled='---'+sled+'0'                         #将led随机亮序补位，前面的---使得轮到最后一位数字到最右一位数码管时表示方便，末尾补位0方便切片
        
    ######################################################################输出阶段############################################################
        time.sleep(2) 
        threads=[]  #创建threads列表
        for i in range(len(tlist)):
            # threads.append(threading.Timer(tlist[i],nums,(i,)))
            threads.append(threading.Timer(tlist[i],bling,(i,)))#创建线程并添加进上述列表，括号内线程用Timer实现，三个参数依次代表延长的时间、任务、任务所需参数
            
        threads.append(threading.Timer((tlist[i]+0.5),over,))#添加最后一个线程，关闭所有的元件，清空所有列表和字符串
        for t in threads:
            t.setDaemon(True)
            t.start()                               #同时启动threads列表中的线程
        
##################
def bling(n):

    SAKS.ledrow.off_for_index(int(sled[(-1-n)]))    #关闭上一次亮起的led灯
    SAKS.buzzer.beep(0.025)                         #蜂鸣器工作
    SAKS.ledrow.on_for_index(int(sled[(-2-n)]))     #点亮当前轮到的LED灯
    
def nums(n):
    SAKS.digital_display.show(sled[(-n-5):(-n-1)]) #在四位数码管显示当前及紧随其后的三个即将亮起的LED灯编码
def over():
    SAKS.ledrow.off()
    SAKS.digital_display.off()                      #关闭各种显示，清空各种列表和字符串
    tlist[:]=[]
    timelist[:]=[]
    sled=''
#################
SAKS.tact_event_handler =tact_event_handler         #将原始的按钮反应函数修改为我们所定义的新按钮反应函数


