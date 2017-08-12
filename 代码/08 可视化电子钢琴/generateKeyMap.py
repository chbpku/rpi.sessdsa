import pygame
from pygame.locals import *

class noteName:
    '''
    关于音名的类
    '''
    base='CDEFGAB'
    def __init__(self, name:str):
        self.name=name

    def __next__(self):
        s=self.name[1]
        index=self.base.index(s)
        if s != 'B':
            new = self.base[index + 1]
            return noteName(self.name[0]+new)
        else:
            new=str(1+int(self.name[0]))
            return noteName(new+'C')

    def __str__(self):
        return self.name

keys = 'zxcvnm|asdfjklqweriop'
note=noteName('3C')
for key in keys:
    print("(K_%s, True):'%s+',"%(key, note))
    note=note.__next__()
