from sakshat import SAKSHAT
import pyaudio
import time
import struct
#声音输入端
pa = pyaudio.PyAudio()
SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
NUM_SAMPLES = 4096
#扩展板
SAKS = SAKSHAT()
#建两个字典实现对应关系
dic1 = {'a':'.-','b':'-...','c':'-.-.','d':'-..','e':'.','f':'..-.','g':'--.','h':'....','i':'..','j':'.---','k':'-.-','l':'.-..','m':'--','n':'-.','o':'---','p':'.--.','q':'--.-','r':'.-.','s':'...','t':'-','u':'..-','v':'...-','w':'.--','x':'-..-','y':'-.--','z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----','/':'-..-.','?':'..--..','.':'.-.-.-'}
dic2 = {'.-':'a','-...':'b','-.-.':'c','-..':'d','.':'e','..-.':'f','--.':'g','....':'h','..':'i','.---':'j','-.-':'k','.-..':'l','--':'m','-.':'n','---':'o','.--.':'p','--.-':'q','.-.':'r','...':'s','-':'t','..-':'u','...-':'v','.--':'w','-..-':'x','-.--':'y','--..':'z','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6','--...':'7','---..':'8','----.':'9','-----':'0','-..-.':'/','..--..':'?','.-.-.-':'.'}
#蜂鸣器
b = SAKS.buzzer
b.beep(0)
#一个点叫的秒数
point = 0.03
#一划叫的秒数
line = point*3
#选择进入哪种模式
print('which type?word/code/voice?')
ty = input()
#英文输摩尔斯电码
if ty == 'word':
	print('Please input your word, my prince/princess')
	onone1 = [False,]*4+[True,]*4
	onone2= [True,]*4+[False,]*4
	s = input()
	everypart = s.split()
	#对每一个最小单元依次扫描
	for i in everypart:
		for j in i:
			jreal = dic1[j]
			for k in jreal:
				#如果遇到点
				if k=='.':
					b.beep(point)
					SAKS.digital_display.show('6.66.6')
					SAKS.ledrow.set_row(onone2)
				#如果遇到划
				elif k=='-':
					b.beep(line)
					SAKS.digital_display.show('2.333')
					SAKS.ledrow.set_row(onone1)
				time.sleep(point)
			SAKS.ledrow.off()
			time.sleep(point*2)
		#单词之间输出8888
		SAKS.digital_display.show('8888')
		time.sleep(point*4)
		
#摩尔斯电码输出英文
elif ty=='code':
	print('Please input your code, my prince/princess')
	s = input()
	everypart = s.split()
	for i in everypart:
		print(dic2[i]),

#输入声音输出英文
elif ty=='voice':
	voi = []
	i = 0
	s = ''
	while True:
		stream = pa.open(format = pyaudio.paInt16,channels = 1,rate = SAMPLING_RATE,input = True,frames_per_buffer = NUM_SAMPLES)
		string_audio_data= stream.read(NUM_SAMPLES)
		#声音大小
		k= max(struct.unpack('%dh'%(NUM_SAMPLES,),string_audio_data)	)
		stream.close()
		#大到一定程度记1，连续记录
		if k>10000:
			i+=1
		else:
			#点
			if i>1 and i<=3:
				s+='.'
				SAKS.digital_display.show('6.66.6')
				i = 0
			#划
			elif i>=6 and i<=10:
				s+='-'
				SAKS.digital_display.show('2.333')
				i = 0
			#极短地叫一下极为空格
			elif i==1:
				voi.append(s)
				s=''
				i=0
				SAKS.digital_display.show('8888')
			elif i>13 and i<=25:
				break
			#声音持续时间过长或过短均极为没有输入
			elif i>25:
				i = 0
				s=''
			else:
				i = 0
		print(i)
		print(s)
		print(voi)
	for i in voi:
		print(dic2[i]),
