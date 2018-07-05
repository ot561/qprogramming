from makestuff import *
from functools import partial 
from quantumprograms import *
class Control():

    def __init__(self,frame):
        self.frame = frame
        self.buttons = {}
        self.row = 0
        self.make_button("test",partial(print,15))
        
    def make_button(self,label,cmd):
        print('cmd', cmd)
        self.buttons[label] = MakeButton(self.frame,2,0,"Submit",cmd)
        self.buttons[label].button.grid(row=self.row,column=0)
        self.row = self.row + 1

    def clear_all(self):
        for key in self.input:
            self.buttons[key].destroy()
        self.row = 0

