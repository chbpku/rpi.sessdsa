from PyQt5 import QtWidgets  
#从PyQt库导入QtWidget通用窗口类  
class mywindow(QtWidgets.QWidget):  
#自己建一个mywindows类，以class开头，mywindows是自己的类名，  
#（QtWidgets.QWidget）是继承QtWidgets.QWidget类方法，  
    def __init__(self):  
        super(mywindow,self).__init__()  
  
import sys  
app = QtWidgets.QApplication(sys.argv)  
windows = mywindow()  
label=QtWidgets.QLabel(windows)     #在窗口中绑定label  
label.setText("hello world")  
  
windows.show()  
sys.exit(app.exec_())  
/boot/overlay/README


/boot/overlay/README

http://blog.csdn.net/weixuedianzi/article/details/65935313?locationNum=9&fps=1
