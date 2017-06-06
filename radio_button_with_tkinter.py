from Tkinter import *
import pyautogui

chon = ''

def sel():
    print(chon)
    if chon == 1:
        pyautogui.alert(text='Chon 1', title='Warning', button='OK')
    elif chon == 2:
        pyautogui.alert(text='Chon 2', title='Warning', button='OK')
    elif chon == 3:
        pyautogui.alert(text='Chon 3', title='Warning', button='OK')
    else:
        pyautogui.alert(text='Chua chon ', title='Warning', button='OK')
def se2():
    global chon
    chon = var.get()
    pass

root = Tk()
var = IntVar()
R1 = Radiobutton(root, text="Option 1", variable=var, value=1,command=se2)
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Option 2", variable=var, value=2,command=se2)
R2.pack( anchor = W )

R3 = Radiobutton(root, text="Option 3", variable=var, value=3,command=se2)
R3.pack( anchor = W)

B = Button(root, text ="Start", command = sel)
B.pack( anchor = W)
label = Label(root)
label.pack()
root.mainloop()
