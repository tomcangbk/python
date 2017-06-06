from Tkinter import *
import tkFileDialog
from pytube import YouTube
import subprocess, os

def function():
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent=top, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print "You chose %s" % tempdir
    
    
        
    
if __name__ == "__main__":
    top = Tk()
    top.wm_title("Title")
    
    B1 = Button(top, text ="Browser",bd = 3,  width = 15, font=("Consolas 13 bold italic"), command = function)
    B1.pack(side = TOP)
    L5 = Label(top, text="  ")

    top.mainloop()
