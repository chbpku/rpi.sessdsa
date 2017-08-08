#!/usr/bin/python
# coding:utf-8

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv
import os
import wx
from sakshat import SAKSHAT
import time
import sys, urllib, urllib2, json


def mustache(evt):
    # 加载底图
    base_img = Image.open('/home/pi/Desktop/face/2.1.jpeg')
    # 转化为RGBA
    base_img = base_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print base_img.size,base_img.mode
    # 加载需要P上去的图片
    tmp_img = Image.open('/home/pi/Desktop/face/shipin/mtsc11572.png')
    # 转化为RGBA
    tmp_img = tmp_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print tmp_img.size,tmp_img.mode

    # 这里可以选择一块区域或者整张图片
    # region = tmp_img.crop((0,0,304,546)) #选择一块区域
    # 或者使用整张图片
    region = tmp_img
    # 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
    # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
    # 提前将图片进行缩放，以适应box区域大小
    # region = region.resize((box[2] - box[0], box[3] - box[1]),Image.ANTIALIAS)
    # region.show()
    region = region.resize((int(base_img.size[0] / 3), int(base_img.size[1] / 5)))
    box = ((int(base_img.size[0] / 2) - int(tmp_img.size[0] / 3.4)),
           (int(base_img.size[1] * 0.93) - int(tmp_img.size[1])))  # 底图上需要P掉的区域的左上角坐标
    # 分离透明通道
    r, g, b, a = region.split()
    base_img.paste(region, box, mask=a)
    base_img.show()  # 查看合成的图片
    base_img.save('/home/pi/Desktop/face/4.1.jpeg', 'jpeg', quality=95)  # 保存图片


def ears(evt):
    # 加载底图
    base_img = Image.open('/home/pi/Desktop/face/2.1.jpeg')
    # 转化为RGBA
    base_img = base_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print base_img.size,base_img.mode
    # 加载需要P上去的图片
    tmp_img = Image.open('/home/pi/Desktop/face/shipin/mtsc11704.png')
    # 转化为RGBA
    tmp_img = tmp_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print tmp_img.size,tmp_img.mode

    # 这里可以选择一块区域或者整张图片
    # region = tmp_img.crop((0,0,304,546)) #选择一块区域
    # 或者使用整张图片
    region = tmp_img

    # 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
    # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
    # 提前将图片进行缩放，以适应box区域大小
    # region = region.resize((box[2] - box[0], box[3] - box[1]),Image.ANTIALIAS)
    # region.show()
    region = region.resize((int(base_img.size[0] / 1.5), int(base_img.size[1] / 3)))
    box = ((int(base_img.size[0] / 2) - int(tmp_img.size[0] / 0.9)), 0)  # 底图上需要P掉的区域的左上角坐标
    # 分离透明通道
    r, g, b, a = region.split()
    base_img.paste(region, box, mask=a)
    base_img.show()  # 查看合成的图片
    base_img.save('/home/pi/Desktop/face/4.1.jpeg', 'jpeg', quality=95)  # 保存图片


def note(evt):
    # 加载底图
    base_img = Image.open('/home/pi/Desktop/face/2.1.jpeg')
    # 转化为RGBA
    base_img = base_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print base_img.size,base_img.mode
    # 加载需要P上去的图片
    tmp_img = Image.open('/home/pi/Desktop/face/shipin/mtsc10907.png')
    # 转化为RGBA
    tmp_img = tmp_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print tmp_img.size,tmp_img.mode

    # 这里可以选择一块区域或者整张图片
    # region = tmp_img.crop((0,0,304,546)) #选择一块区域

    # 或者使用整张图片
    region = tmp_img

    # 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
    # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
    # 提前将图片进行缩放，以适应box区域大小
    # region = region.resize((box[2] - box[0], box[3] - box[1]),Image.ANTIALIAS)
    # region.show()
    region = region.resize((int(base_img.size[0] / 1.5), int(base_img.size[1] / 3)))
    box = ((int(base_img.size[0]) - int(tmp_img.size[0] / 0.7)), 0)  # 底图上需要P掉的区域的左上角坐标
    # 分离透明通道
    r, g, b, a = region.split()
    base_img.paste(region, box, mask=a)
    base_img.show()  # 查看合成的图片
    base_img.save('/home/pi/Desktop/face/4.1.jpeg', 'jpeg', quality=95)  # 保存图片


def non_mainstream(evt):
    # 加载底图
    base_img = Image.open('/home/pi/Desktop/face/2.1.jpeg')
    # 转化为RGBA
    base_img = base_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print base_img.size,base_img.mode
    # 加载需要P上去的图片
    tmp_img = Image.open('/home/pi/Desktop/face/shipin/mtsc11711.gif')
    # 转化为RGBA
    tmp_img = tmp_img.convert('RGBA')
    # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
    # print tmp_img.size,tmp_img.mode

    # 这里可以选择一块区域或者整张图片
    # region = tmp_img.crop((0,0,304,546)) #选择一块区域
    # 或者使用整张图片
    region = tmp_img

    # 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
    # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
    # 提前将图片进行缩放，以适应box区域大小
    # region = region.resize((box[2] - box[0], box[3] - box[1]),Image.ANTIALIAS)
    # region.show()
    region = region.resize((int(base_img.size[0] / 2), int(base_img.size[1] / 2)))
    box = (0, (int(base_img.size[1] / 2) - int(tmp_img.size[1] / 2)))  # 底图上需要P掉的区域的左上角坐标
    # 分离透明通道
    r, g, b, a = region.split()
    base_img.paste(region, box, mask=a)
    base_img.show()  # 查看合成的图片
    base_img.save('/home/pi/Desktop/face/4.1.jpeg', 'jpeg', quality=95)  # 保存图片


def detect_object(image):
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    cascade = cv.Load("/usr/share/opencv/haarcascades/haarcascade_frontalface_alt_tree.xml")
    rect = cv.HaarDetectObjects(grayscale, cascade, cv.CreateMemStorage(), 1.1, 2,
                                cv.CV_HAAR_DO_CANNY_PRUNING, (20, 20))

    result = []
    for r in rect:
        result.append((r[0][0], r[0][1], r[0][0] + r[0][2], r[0][1] + r[0][3]))

    return result


def process(infile):
    image = cv.LoadImage(infile);
    if image:
        faces = detect_object(image)

    im = Image.open(infile)
    path = os.path.abspath(infile)
    save_path = os.path.splitext(path)[0] + "_face"
    try:
        os.mkdir(save_path)
    except:
        pass
    count = 0
    if faces:
        draw = ImageDraw.Draw(im)
        for f in faces:
            count += 1
            draw.rectangle(f, outline=(255, 0, 0))
            a = im.crop(f)
            file_name = os.path.join(save_path, str(count) + ".jpg")
            a.save(file_name)

        drow_save_path = os.path.join(save_path, "out.jpg")
        im.save(drow_save_path, "JPEG", quality=80)
        im.show()
    else:
        print "Error: cannot detect faces on %s" % infile
    print count


def find_face(evt):
    process('/home/pi/Desktop/face/1.1.jpg')


def contact(evt):
    Im = Image.open("/home/pi/Desktop/contact.jpg")
    Im.show()


def intro(evt):
    Im = Image.open("/home/pi/Desktop/intro.jpg")
    Im.show()


def Filter(evt):
    Im = Image.open("/home/pi/Desktop/face/1.2.jpg")
    Im = Im.filter(ImageFilter.CONTOUR)
    Im = Im.resize((880, 1000))
    Im.show()


app = wx.App()
# 创建Frame
win = wx.Frame(None, title='P_T', size=(1000, 800))
win.SetFont(wx.Font(20, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.BOLD, False))
# 创建Panel
panel = wx.Panel(win)
panel.SetBackgroundColour((100, 100, 100))
# 创建open，save按钮

bt_Filter = wx.Button(panel, -1, label='\(≧▽≦)/ Face outlines', size=(45, 30))
bt_Filter.SetForegroundColour((255, 255, 255))
bt_Filter.SetBackgroundColour((131, 175, 155))
bt_Filter.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_Filter.Bind(wx.EVT_BUTTON, Filter)

bt_Find = wx.Button(panel, -1, label='￣∇￣ Find face', size=(45, 30))
bt_Find.SetForegroundColour((255, 255, 255))
bt_Find.SetBackgroundColour((252, 157, 154))
bt_Find.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_Find.Bind(wx.EVT_BUTTON, find_face)  # 添加FIND按钮事件绑定

bt_note = wx.Button(panel, -1, label='=(￣ω￣)= note++', size=(45, 30))
bt_note.SetForegroundColour((255, 255, 255))
bt_note.SetBackgroundColour((252, 157, 154))
bt_note.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_note.Bind(wx.EVT_BUTTON, note)  # 添加FIND按钮事件绑定

bt_non_mainstream = wx.Button(panel, -1, label='V(^▽^)V non_mainstream', size=(45, 30))
bt_non_mainstream.SetForegroundColour((255, 255, 255))
bt_non_mainstream.SetBackgroundColour((249, 205, 173))
bt_non_mainstream.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_non_mainstream.Bind(wx.EVT_BUTTON, non_mainstream)  # 添加CUTE++按钮事件绑定

bt_mustache = wx.Button(panel, -1, label='[^.^] mustache++', size=(45, 30))
bt_mustache.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_mustache.SetForegroundColour((255, 255, 255))
bt_mustache.SetBackgroundColour((131, 175, 155))
bt_mustache.Bind(wx.EVT_BUTTON, mustache)  # 添加introduce按钮事件绑定

bt_ears = wx.Button(panel, -1, label='$(￣∇￣)3 ears++', size=(45, 30))
bt_ears.SetForegroundColour((255, 255, 255))
bt_ears.SetBackgroundColour((252, 157, 154))
bt_ears.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_ears.Bind(wx.EVT_BUTTON, ears)  # 添加FIND按钮事件绑定

bt_intro = wx.Button(panel, -1, label='(^-^)V For more', size=(45, 30))
bt_intro.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_intro.SetForegroundColour((255, 255, 255))
bt_intro.SetBackgroundColour((131, 175, 155))
bt_intro.Bind(wx.EVT_BUTTON, intro)  # 添加introduce按钮事件绑定

bt_extra = wx.Button(panel, -1, label='⁄(⁄⁄⁄ω⁄⁄⁄)⁄ Contact us', size=(45, 30))
bt_extra.SetForegroundColour((255, 255, 255))
bt_extra.SetBackgroundColour((252, 157, 154))
bt_extra.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
bt_extra.Bind(wx.EVT_BUTTON, contact)  # 添加FIND按钮事件绑定

# 添加布局管理器
bsizer_all = wx.GridSizer(2, 4)
panel.SetSizer(bsizer_all)
bsizer_all.Fit(panel)
bsizer_all.Add(bt_Filter, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_Find, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_non_mainstream, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_mustache, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_note, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_ears, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_intro, 1, flag=wx.EXPAND)
bsizer_all.Add(bt_extra, 1, flag=wx.EXPAND)


def saks(num):
    if num<=8:
        for i in range(num):
            SAKS.ledrow.on_for_index(i)
        SAKS.buzzer.beepAction(0.15, 0.15, num)
    else:
        for i in range(8):
            SAKS.ledrow.on_for_index(i)
            SAKS.buzzer.beepAction(1, 0, 1)
    SAKS.digital_display.show(("%3d" % num).replace(' ','#')) #数码管显示人脸数值
    time.sleep(5)
    SAKS.ledrow.off()# LED关闭
    SAKS.buzzer.beepAction(1.5, 0, 1)
    SAKS.digital_display.show('0000')# 数码管显示'0000'

win.Show()
app.MainLoop()

