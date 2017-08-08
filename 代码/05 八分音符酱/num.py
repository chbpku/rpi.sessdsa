#从score文件中读取当前分数, 并在树莓派上显示出来
#循环读取, 并且考虑正在写文件时, 文件内容为零的情况
import gpio_1

while True:
    with open("score.txt", "r") as f:
        lst = f.read().split()
        if len(lst) == 2:
            #在文件被写入之后, 读取的是两个数, 其中第一个为当前分数
            score = int(lst[0])
            gpio_1.number(score)
