# -*- coding: utf-8 -*-
# @Author: Ren Qingjie
# @Date:   2017-05-14 15:48:55
# @Last Modified by:   Ren Qingjie
# @Last Modified time: 2017-05-19 00:33:03


import time
import os
import sakshat
import picamera
import face_recognition
import PIL
import dlib
import RPi

# 设置相机和扩展版
s = sakshat.SAKSHAT()
c = picamera.PiCamera()


# 总体名单及对应的编号
leaders = {0: 'DengXiaoping', 1: 'HuaGuofeng', 2: 'HuJintao', 3: 'HuYaobang', 4: 'JiangZeMin',
           5: 'LiKeqiang', 6: 'MaoZedong', 7: 'WenJiabao', 8: 'XijinPing', 9: 'Zhaoziyang'}
inv_leaders = {value: key for key, value in leaders.items() }


# 识别照片的函数
def check(total, sample):
    # total为全体，是一个字典类型
    # sample为样本，是一个图片格式，通过拍照获得
    image = face_recognition.load_image_file(sample)
    face_locations = face_recognition.face_locations(image)
    # face_landmarks_list = face_recognition.face_landmarks(image)

    # 处理已知的名单和已知的图片
    known_image = []
    for i in os.listdir('leaderFaces'):
        known_image.append(
            face_recognition.load_image_file('leaderFaces/' + i))
    # 把已知人员全部加载为编码格式便于比对
    biden_encoding = []
    for i in known_image:
        biden_encoding = biden_encoding + face_recognition.face_encodings(i)

    # 处理读入的图片
    face_image_list = []
    # results记录成功签到和未签到的人数
    results = {total[i]: False for i in total}
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        face_image_list.append(face_image)
        unknown_encoding = face_recognition.face_encodings(face_image)[0]

        if True in face_recognition.compare_faces(biden_encoding, unknown_encoding, 0.5):
            # 识别情况
            recognition = face_recognition.compare_faces(
                biden_encoding, unknown_encoding, 0.5)
            # 确定对应的人
            leader = recognition.index(True)
            # 添加到结果中
            results[leaders[leader]] = True
            # results[total[face_recognition.compare_faces(biden_encoding,
            # unknown_encoding, 0.5).index(True)] = True;
    return results


# # 自动拍摄函数
# def take(button, camera=c, t=5):
#     # 开关作为触发机制
#     if button is True:
#         # 开始预览
#         camera.start_preview()
#         # 停顿5秒
#         time.sleep(t)
#         # 拍照
#         camera.capture("sample.jpg")
#         # 结束预览
#         camera.stop_preview()


# 延时拍照函数
def take(camera=c, t=10):
    camera.start_preview()
    time.sleep(t)
    camera.capture("sample.jpg")
    camera.stop_preview()


# main process
def main():
    # 开始拍照
    take(camera=c, t=10)
    # 引入变量
    total = leaders
    sample = "sample.jpg"
    # 比较，得到结果
    print(check(total, sample))
    # 通过显示器和扩展版显示出来结果


if __name__ == '__main__':
    main()
