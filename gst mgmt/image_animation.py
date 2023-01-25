from tkinter import *
from PIL import Image,ImageTk
from threading import Thread as th
import time
'''root=Tk()'''

def fade_animation(img_name,img_label):
    initial_alpha_value=0
    def fade(img_name,img_label,initial_alpha_value):      
        if initial_alpha_value!=234:
            img=Image.open(img_name)
            img.putalpha(initial_alpha_value)
            img.save(img_name)
            img=Image.open(img_name)
            photoo=ImageTk.PhotoImage(image=img)
            img_label.configure(image=photoo)
            initial_alpha_value+=18
            img_label.after(150,fade(img_name,img_label,initial_alpha_value))
        else:
            img_label.after(2500)
            return
            
    t=th(target=fade,args=(img_name,img_label,initial_alpha_value))
    t.start()
    
'''b=Button(root,text='Go')
b.pack()
l=Label(root)
l.pack()
t=th(target=fade_animation,args=('gstt.png',l,b,0))
b.config(command=t.start)


root.mainloop()'''
