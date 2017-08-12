
import pygame
from pygame.locals import *
import threading
import time
import queue
import os
# 判断是否为树莓派操作系统
isRPi = os.name == 'posix'
if isRPi:
    import Piano_SAKS

# 扫描时间差，参考：人耳最小分辨时间差为0.1s
TICK = 0.01

# 键位表字典，将pygame中按键常量映射为音名。传入二元元组，包含键、空格是否按下。默认八度符为0情况
# TODO 根据音符填充字典，添加右手小指
key2note = {
    (K_z, False): '3C',
    (K_x, False): '3D',
    (K_c, False): '3E',
    (K_v, False): '3F',
    (K_n, False): '3G',
    (K_m, False): '3A',
    (K_COMMA, False): '3B',
    (K_PERIOD, False):'4C',
    (K_a, False): '4C',
    (K_s, False): '4D',
    (K_d, False): '4E',
    (K_f, False): '4F',
    (K_j, False): '4G',
    (K_k, False): '4A',
    (K_l, False): '4B',
    (K_SEMICOLON, False): '5C',
    (K_q, False): '5C',
    (K_w, False): '5D',
    (K_e, False): '5E',
    (K_r, False): '5F',
    (K_i, False): '5G',
    (K_o, False): '5A',
    (K_p, False): '5B',
    (K_LEFTBRACKET, False): '6C',
    (K_z, True):'3C+',
    (K_x, True):'3D+',
    (K_c, True):'3F',
    (K_v, True):'3F+',
    (K_n, True):'3G+',
    (K_m, True):'3A+',
    (K_COMMA, True):'4C',
    (K_PERIOD, True):'4C+',
    (K_a, True):'4C+',
    (K_s, True):'4D+',
    (K_d, True):'4F',
    (K_f, True):'4F+',
    (K_j, True):'4G+',
    (K_k, True):'4A+',
    (K_l, True):'5C',
    (K_SEMICOLON, True):'5C+',
    (K_q, True):'5C+',
    (K_w, True):'5D+',
    (K_e, True):'5F',
    (K_r, True):'5F+',
    (K_i, True):'5G+',
    (K_o, True):'5A+',
    (K_p, True):'6C',
    (K_LEFTBRACKET, True):'6C+',
}

# 乐器列表
# TODO 随音源库的丰富，动态添加
instruments = ['piano', 'harp', 'violin', 'flute', 'musicbox', 'trumpet']


class note:
    '''
    关于音符的类。
    记录了音符的乐器、音高、开始或停止。
    作为键盘事件传入的信息，等待主线程处理
    '''

    def __init__(self, channel, tune: str, isStart: bool = True, volume: float = 1.0, stretch = False):
        '''
        初始化一个音符
        :param channel: music_channel对象，表示发出此音符的频道，借以获得乐器
        :param tune: 一个字符串，表示音符音名。和音源文件名字对应
        :param isStart: 是否开始或结束。可能会同时传入同一个乐器两次开始符。
        :param stretch: 是否延音，默认为False
        '''
        self.channel = channel
        self.tune = tune
        self.isStart = isStart
        self.volume = volume
        self.stretch = stretch

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        '''
        判断两个音符是不是同一个音符。
        判断是不是音高相同是无意义的，因此用id来进行判断
        :param other: 
        :return: 
        '''
        return id(self) == id(other)

    def __str__(self):
        '''
        音符的字符串表示
        :return: 
        '''
        return 'instrument: %s, tune: %s, isStart: %s, volume: %s' \
               % (self.channel.instrument, self.tune, self.isStart, self.volume)


class music_channel:
    '''
    音轨类,可能是一个键盘音轨，可能是一个文件音轨。
    
    '''

    # TODO 添加一个信息，可以在创建音轨时确定的特异信息，类似Hash，与音符一起送进队列，并且和对象本身可以互查

    def __init__(self, instrument='piano', source: str = 'KEY'):
        '''
        初始化混音器，初始化混音列表
        :param instrument: 乐器种类，用一个字符串表示。键盘音轨可以更换。
        :param source: 音轨输入源，字符串KEY或FILE
        '''
        self.source = source
        # 存放已编译好的声音文件，即mixer.channel对象的字典
        self.sound_dict = {}
        # 设置乐器
        self.instrument = ''
        self.set_instrument(instrument)
        # 由于混音器统一调度，需要对接队列
        self.queue = None
        # TODO 解耦，可以不需要这个bind变量
        # 是否已和某个混音器结合。
        self.bind = False
        # 音量,0-1
        self.volume = 1.0
        

    def set_instrument(self, instrument: str):
        '''
        设定键盘输入的乐器种类。注意：自由模式无限制，录音模式不可以修改，放音模式只能修改录音的乐器种类。
        :param instrument: 一个字符串，表示乐器种类
        :return: 
        '''
        # TODO 将所有导入音频文件的操作放在这一步
        # 保证乐器名合法
        assert instrument in instruments, 'No Such Instrument Here!'
        self.instrument = instrument
        self.sound_dict.clear()
        dir_name = './%s'%(instrument)
        # 对声音字典进行预处理
        for file_name in os.listdir(dir_name):
            # 获取音乐完整的相对路径
            path = '/'.join([dir_name, file_name])
            # 获取音源的音名
            note_name = os.path.splitext(file_name)[0]
            # 解码声音文件
            channel = pygame.mixer.Sound(path)
            self.sound_dict[note_name] = channel
        return None

    def key_input(self):
        '''
        开始监听键盘输入，转换成note对象并放入队列中
        同时监听空格，作为
        作为一个键盘线程的target
        :param queue: 要放入的队列
        :return: None
        '''
        # 八度标识符
        octave = 0
        # 已定义过判断系统的变量
        global isRPi
        assert self.source == 'KEY'
        # 记录当前有哪些键被按下的字典，值为该键对应的发出的note对象，已备release时发出
        pygame.event.set_allowed([KEYUP,KEYDOWN,QUIT])
        down_dict = {}
        try:
            while True:
                # 对每个键盘事件，判断类型
                # TODO 并没有捕获键盘事件的迹象
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if (event.key, False) in key2note.keys():
                            # 如果按下的键在映射列表中，进行操作，
                            # 获得空格是否按下
                            press_list = pygame.key.get_pressed()
                            space_pressed = press_list[K_SPACE]
                            alt_pressed = press_list[K_LALT]
                            # 延音踏板
                            shift_pressed = press_list[K_LSHIFT]
                            del press_list
                            # 获得映射列表对应的音名（未改变八度）
                            note_name = key2note[(event.key, space_pressed)]
                            
                            if note_name not in self.sound_dict.keys():
                                # 如果没有在音符列表中，则直接放弃
                                continue
                            # 用alt做弱音踏板
                            self.volume = 0.6 if alt_pressed else 1
                            # 我们终于做好了预处理，可以创建音符了！
                            newNote = note(self, note_name, True, self.volume, shift_pressed)
                            # 放进“正在播放”字典中
                            down_dict[event.key] = newNote
                            # 将音符和相关信息放进队列

                            if self.bind:
                                self.queue.put(newNote)
                        elif event.key == K_ESCAPE:
                            print('正常退出')
                            self.quit()
                        elif event.key == K_TAB:
                            # TODO 如果做GUI，则这部分删除，添加鼠标事件
                            # TAB键用于切换乐器
                            if isRPi:
                                # 如果在树莓派上，全部亮起表示正在更换乐器中
                                Piano_SAKS.SAKS.ledrow.on()
                                Piano_SAKS.button_time = 0
                            self.sound_dict.clear()
                            # 获取下一个乐器。暂时不使用GUI调整乐器
                            newIndex = (instruments.index(self.instrument) + 1) % len(instruments)
                            self.set_instrument(instruments[newIndex])
                            if isRPi:
                                # 关闭树莓派的灯，准备开始读取
                                Piano_SAKS.SAKS.ledrow.off()

                    elif event.type == KEYUP:
                        # 抬起按键，将对应的音符改成松开模式送进队列
                        if event.key in down_dict.keys():
                            # 如果在已按下的列表里，才进行操作
                            popNote = down_dict.pop(event.key)
                            # 同一个音符改成“松开模式”
                            popNote.isStart = False
                            if self.bind:
                                self.queue.put(popNote)
                                # print(popNote)
                    elif event.type == QUIT:
                        self.quit()
                    else:
                        continue

        except Exception as e:
            # 异常退出
            print('程序因为某些原因异常关闭！')
            self.quit()

    def file_input(self, readable, queue: queue.Queue):
        '''
        从文件中输入音符。用于录音文件的播放。
        可以与键盘相叠加，也可以互相叠加。
        :param readable: 
        :param queue: 
        :return: 
        '''

    def quit(self):
        '''
        退出钢琴
        :return: 
        '''
        if isRPi:
            Piano_SAKS.stop = True
            # 等待秒表完成
            time.sleep(1)
            Piano_SAKS.cleanUp()
        pygame.quit()

        exit()

class music_mixer:
    '''
    混音器类
    '''

    def __init__(self, mode: str = 'FREE'):
        '''
        初始化一个空混音器。
        :param mode: 初始模式。默认为自由模式，
        '''
        self.channels = []
        self.musicQueue = queue.Queue()
        # mode属性对外可写，对内可读
        self.mode = mode
        # playing_dict: 从note对象映射到正在播放的mixer.channel对象
        self.playing_dict = {}

    def get_instrument(self, channel: int):
        '''
        获取某个声部的当前乐器。
        :param channel: 一个整数
        :return: 字符串或None
        '''
        try:
            return self.channels[channel].instrument
        except:
            return None

    def add_channel(self, channel: music_channel):
        '''
        在混音器中添加一个channel，同时将队列与channel绑定
        :param channel: channel对象
        :return: 
        '''
        self.channels.append(channel)
        channel.queue = self.musicQueue
        channel.bind = True

    def remove_channel(self, channel: music_channel):
        '''
        将某个channel从混音器解绑，队列还原为空
        :param channel: 
        :return: True正确移除，FALSE不再channels中注册过
        '''
        if channel in self.channels:
            self.channels.remove(channel)
            channel.queue = None
            channel.bind = False
            return True
        else:
            return False

    def sound_process(self):
        '''
        用pygame处理声音的过程。包含播放和可能的录制。循环过程，直到打断
        :param queue: 
        :return: 
        '''
        # TODO 拨码开关可以打断此线程。在whileTRUE第一句对拨码事件判断
        startTime = time.time()
        global isRPi


        while True:
    
            item = self.musicQueue.get()
            # 获取的item应该是一个note对象，获取其状态
            assert isinstance(item, note), 'Not A Note Object!'
            if item.isStart:
                try:
                    # 是开始的音符，获取channel对象
                    # TODO 这里要调用相应的频道的字典，获取channel
                    sound = item.channel.sound_dict[item.tune]
                    # 获取开始时间戳
                    timing = time.time() - startTime
                    # self.playing_dict[note] = (sound, timing)
                    # TODO 是否加参数进行处理音色
                    # 音量处理
                    sound.set_volume(item.volume)
                    sound.play()
                    # TODO 录音状态下，将该部分写入缓冲区
                    # 添加GPIO操作，包括关灯开灯和数字显示
                    if isRPi:
                        threading.Thread(target=Piano_SAKS.ledOn, args=(item.tune,)).start()
                        Piano_SAKS.button_time+=1
                except Exception as e:
                    print(e)


            else:
                try:
                    # 是结束的音符，找到相应的音符进行结束处理
                    sound = item.channel.sound_dict[item.tune]
                    if not item.stretch:
                        # 非延音，则逐渐消失
                        sound.fadeout(600)
                    timing = time.time() - startTime
                    # TODO 录音状态下，将该部分写入缓冲区
                    # 添加GPIO操作，开灯关灯数字显示
                    # if isRPi:
                    #     threading.Thread(target=Piano_SAKS.ledOff, args=(item.tune,)).start()
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    pygame.init()
    mixer = music_mixer()
    key_channel = music_channel(instrument='piano')
    mixer.add_channel(key_channel)
    mixer_thread=threading.Thread(target=mixer.sound_process)
    key_thread = threading.Thread(target=key_channel.key_input)
    screen = pygame.display.set_mode((320, 240), 0, 32)
    pygame.display.set_caption('RPi Piano')
    mixer_thread.start()
    # key_thread.start()
    if isRPi:
        # 展示时间的操作
        threading.Thread(target=Piano_SAKS.display_count).start()
    key_channel.key_input()
