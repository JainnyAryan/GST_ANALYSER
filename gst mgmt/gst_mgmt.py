# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 13:28:24 2020

@author: Aryan Jain
"""    
import os
from tkinter import *
import mysql.connector as sql
global run_gst_mgmt

mydb=sql.connect(
    host="localhost",
    user="root",
    passwd="1234")

mcur=mydb.cursor()
def sql(c): 
    mcur.execute(c)
    mydb.commit()
    for i in mcur:
        print(i)

sql('create database if not exists gst;')
sql('use gst')
sql('''create table if not exists dealers
(dealer_gstin char(15) primary key,
dealer_name varchar(50),
dealer_address text,
dealer_contact bigint(20),
dealer_email varchar(100),
time_added datetime);
''')
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


def RunApp(splash):
    import dealer
    import officer
    from tkinter.font import Font
    import time
    from threading import Thread as th
    from tkinter import messagebox as msg
    from PIL import Image,ImageTk
    from image_animation import fade_animation
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True


    def run_gst_mgmt():

        def loginscreen():
            frame1.destroy()
            frame2.destroy()
            global frame3
            frame3=Frame(root,bg='red')
            Label(frame3,text='Dashboard',font=(25),fg='white',bg='red').pack(anchor=CENTER)
            frame3.pack(anchor=CENTER,expand=True,fill=X,ipady=20)
            b1=Button(frame3,text='I am a dealer',font=(20),padx=15,bg='orange',fg='white',command=dealer_info)
            b2=Button(frame3,text='I am a officer',font=(20),padx=15,bg='blue',fg='white',command=officer_info)
            Label(frame3,text='\n',bg='red').pack()
            b1.pack(pady=25)
            b2.pack(pady=25)
        

        def dealer_work(a): #going to dealer.py
            #otbd >>> objects to be destroyed
            dealer.dealer_desk(parent=root,otbd=[frame4,frame5,dealer_enter],gstin=a,type='Purchase',serial=1)
            
        def officer_work(): #going to officer.py
            #otbd >>> objects to be destroyed
            officer.officer_desk(parent=root,otbd=[frame5])
            
        def officer_info():
            # homepage_button.config(state=ACTIVE)
            def change_pswd():
                def checknew():
                    if len(change_pswd_var.get().strip())==0:
                        msg.showerror('Error','Please enter passcode !')
                    else:
                        if change_pswd_var.get().strip()==content:
                            create_pass()
                        else:
                            msg.showerror('Error','INCORRECT PASSCODE !')   
                #change password entry-------------
                for widget in frame5.winfo_children():
                    widget.destroy()
                change_pswd_var=StringVar()
                l3=Label(frame5,text='Old Passcode : ',font=(10),bg='blue',fg='white')
                l3.grid(row=0,column=1,sticky='w')
                change_pswd_entry=Entry(frame5,textvariable=change_pswd_var,bd=3,font=(10),show='*')
                change_pswd_entry.grid(row=0,column=2,sticky='w')
                #go button-------------
                Button(frame5,text='GO',font=(20),fg='white',bg='orange',command=checknew).grid(row=1,columnspan=5,pady=5)
            def check():
                if len(pswd_var.get().strip())==0:
                    msg.showerror('Error','Please enter passcode !')
                else:
                    if pswd_var.get().strip()==content:
                        officer_work() # going to officer's desk
                    else:
                        msg.showerror('Error','INCORRECT PASSCODE !')   
            def create_pass():
                def enter():
                    if len(pswd_var.get().strip())==0:
                        msg.showerror('Error','Please enter passcode !')
                    else:
                        f=open('do.not.open','a+')
                        f.truncate(0)
                        f.write(pswd_var.get().strip())
                        f.close()
                        frame5.destroy()
                        loginscreen()
                        msg.showinfo('Success','Passcode created!')
                
                for widget in frame5.winfo_children():
                    widget.destroy()
                #officer create passcode entry-------------
                pswd_var=StringVar()
                pswd_var.set('')
                lll=Label(frame5,text='New Passcode : ',font=(10),bg='blue',fg='white')
                lll.grid(row=0,column=1,sticky='w')
                pswd_entry=Entry(frame5,textvariable=pswd_var,bd=3,font=(10),show='*')
                pswd_entry.grid(row=0,column=2)
                #Enter button------------
                Button(frame5,text='Enter',font=(15),command=enter,justify=CENTER,fg='white',bg='orange',padx=30).grid(row=1,columnspan=5,pady=10)
                frame5.pack(expand=True)
                
            frame3.destroy()
            global frame5
            frame5=Frame(root,bg='blue',padx=80,pady=40)
            f=open('do.not.open','a+')
            f.close()
            f=open('do.not.open')
            content=f.read()
            f.close()
            if len(content)==0:
                #Create button------------
                b=Button(frame5,text='Create Passcode',font=(15),command=create_pass,justify=CENTER,fg='white',bg='orange',padx=30)
                b.grid(row=3,columnspan=5,pady=10)
            else:
                #officer password entry-------------
                pswd_var=StringVar()
                pswd_var.set('')
                l3=Label(frame5,text='Passcode : ',font=(10),bg='blue',fg='white')
                l3.grid(row=0,column=1,sticky='w')
                pswd_entry=Entry(frame5,textvariable=pswd_var,bd=3,font=(10),show='*')
                pswd_entry.grid(row=0,column=2,sticky='w')
                #go button-------------
                Button(frame5,text='GO',font=(20),fg='white',bg='orange',command=check).grid(row=1,columnspan=5,pady=5)
                #forgot button-------------
                Button(frame5,text='Change Passcode',fg='blue',command=change_pswd,padx=5).grid(row=2,pady=5,columnspan=5)
                Label(frame5,text='In case you forget the password, please contact your administrator',fg='white',bg='red').grid(row=3,pady=5,columnspan=5)
            frame5.pack(expand=True)
            
        def dealer_info():
            # homepage_button.config(state=ACTIVE)
            global frame4
            global frame5
            global dealer_enter
            
            def chk_gstin(P):
                if P.isdigit()==True:
                    return True
                elif P=='':
                    return True
                else:
                    if P.isupper()==True: #checks that the alphabet in the gstin is always capital
                        return True
                    else:
                        msg.showerror('Error','Only uppercase (capital) letters allowed in GSTIN!')
                        return False
            def chk_number(P):
                if P.isdigit()==True:
                    return True
                elif P=='':
                    return True
                else:
                    return False
            
            def write_to_database():
                dealer_gstin=dealer_gstin_var.get().strip()
                dealer_name=dealer_name_var.get().strip()
                dealer_add=dealer_add_var.get().strip()
                dealer_num=dealer_num_var.get().strip()
                dealer_email=dealer_email_var.get().strip()
                
                if len(dealer_gstin)!=0 and len(dealer_gstin)!=15:
                    dealer_gstin_entry.config(bg='red')
                    dealer_name_entry.config(bg='white')
                    dealer_add_entry.config(bg='white')
                    dealer_num_entry.config(bg='white')
                    dealer_email_entry.config(bg='white')
                    msg.showerror('Error!','Invalid GSTIN, please enter full GSTIN !')
                    return

                if (len(dealer_gstin)==0) or (len(dealer_name)==0) or (len(dealer_add)==0) or (len(dealer_num)==0) or len(dealer_email)==0: #checks that no field is left empty
                    #for making the entry color red if entry not filled
                    if (len(dealer_name)==0):
                        dealer_name_entry.config(bg='red')
                    else:
                        dealer_name_entry.config(bg='white')
                    if (len(dealer_add)==0):
                        dealer_add_entry.config(bg='red')
                    else:
                        dealer_add_entry.config(bg='white')
                    if (len(dealer_num)==0):
                        dealer_num_entry.config(bg='red')
                    else:
                        dealer_num_entry.config(bg='white')
                    if (len(dealer_gstin)==0):
                        dealer_gstin_entry.config(bg='red')
                    else:
                        dealer_gstin_entry.config(bg='white')
                    msg.showerror('Error!','Fill out all the fields!')
                    if len(dealer_email)==0:
                        dealer_email_entry.config(bg='red')
                    else:
                        dealer_email_entry.config(bg='white')
                
                elif '@' not in dealer_email:
                    dealer_gstin_entry.config(bg='white')
                    dealer_name_entry.config(bg='white')
                    dealer_add_entry.config(bg='white')
                    dealer_email_entry.config(bg='red')
                    dealer_num_entry.config(bg='white')
                    msg.showerror('Error!','Invalid email id, please enter again !')
                    
                elif (len(dealer_num))<10: #checks that the contact no. entered is of 10 or more digits (landline no. can be lengthier than mobile no.)
                    dealer_gstin_entry.config(bg='white')
                    dealer_name_entry.config(bg='white')
                    dealer_add_entry.config(bg='white')
                    dealer_email_entry.config(bg='white')
                    dealer_num_entry.config(bg='red')
                    msg.showerror('Error!','Invalid contact number, please enter again !')
                    
                else:
                    dealer_name_entry.config(bg='white')
                    dealer_add_entry.config(bg='white')
                    dealer_gstin_entry.config(bg='white')
                    dealer_email_entry.config(bg='white')
                    try:
                        dealer_num_entry.config(bg='white')
                        sql(f'''insert into dealers(dealer_gstin,dealer_name,dealer_address,dealer_contact,dealer_email,time_added) values('{dealer_gstin}','{dealer_name}','{dealer_add}',{dealer_num},'{dealer_email}',now());''')
                        sql('use temp')
                        sql(f'''create table {dealer_gstin}
                                (s_no int,
                                type varchar(8),
                                year varchar(7),
                                month varchar(2),
                                gstin char(15),
                                firm_name varchar(100),
                                invoice_no varchar(50),
                                invoice_date varchar(12),
                                commodity_name varchar(30),
                                value bigint,
                                tax_rate int,
                                tax_amt bigint);''')
                        #disabling (greying out) the entry fields do that no change can be made after pressing enter button 
                        dealer_gstin_entry.config(state=DISABLED)
                        dealer_name_entry.config(state=DISABLED)
                        dealer_add_entry.config(state=DISABLED)
                        dealer_num_entry.config(state=DISABLED)
                        dealer_email_entry.config(state=DISABLED)
                        dealer_enter.config(state=NORMAL,fg='green',text='Registered :)\nClick here to proceed to bill entry',command=lambda: dealer_work(dealer_gstin))
                    except Exception as e: #in case some error occrus while writing to SQL database
                        print(e)
                        msg.showerror('Error!','Some error occured, please try again !\n(Maybe the GSTIN is already logged to the system)')
                    
            frame3.destroy()
            frame4=Frame(root)
            frame4.pack()
            dealer_welcome=Label(frame4,text='Hello Dealer, please enter the following the information',font=(20))
            dealer_welcome.pack()
            Label(frame4,text='\n"Note: You can not make changes to your info once entered!"\n\n',fg='red',font=(15)).pack()
            frame5=Frame(root,bg='blue',padx=100,pady=60)
            frame5.pack()
            # dealer gstin entry--------------
            dealer_gstin_var=StringVar()
            l4=Label(frame5,text='GSTIN : ',font=(10),bg='blue',fg='white')
            l4.grid(row=0,column=1)
            dealer_gstin_entry=Entry(frame5,textvariable=dealer_gstin_var,bd=3,font=(10),validate='key',validatecommand=(root.register(chk_gstin),'%P'))
            dealer_gstin_entry.grid(row=0,column=2)
            #Dealer name entry---------------
            dealer_name_var=StringVar()
            l1=Label(frame5,text='Name : ',font=(10),bg='blue',fg='white')
            l1.grid(row=1,column=1)
            dealer_name_entry=Entry(frame5,textvariable=dealer_name_var,bd=3,font=(10))
            dealer_name_entry.grid(row=1,column=2)
            #dealer address entry----------------
            dealer_add_var=StringVar()
            l2=Label(frame5,text='Address : ',font=(10),bg='blue',fg='white')
            l2.grid(row=2,column=1)
            dealer_add_entry=Entry(frame5,textvariable=dealer_add_var,bd=3,font=(10))
            dealer_add_entry.grid(row=2,column=2)
            #dealer contact entry-------------
            dealer_num_var=StringVar()
            l3=Label(frame5,text='Contact No. : ',font=(10),bg='blue',fg='white')
            l3.grid(row=3,column=1)
            dealer_num_entry=Entry(frame5,textvariable=dealer_num_var,bd=3,font=(10),validate='key',validatecommand=(root.register(chk_number),'%P'))
            dealer_num_entry.grid(row=3,column=2)
            dealer_num_entry.delete(0, END)
            #dealer email entry------------
            dealer_email_var=StringVar()
            l4=Label(frame5,text='Email Id. : ',font=(10),bg='blue',fg='white')
            l4.grid(row=4,column=1)
            dealer_email_entry=Entry(frame5,textvariable=dealer_email_var,bd=3,font=(10))
            dealer_email_entry.grid(row=4,column=2)
            #enter button---------------
            dealer_enter=Button(root,text='Enter',padx=15,pady=8,font=(20),command=write_to_database)
            dealer_enter.pack(side=TOP)
            
#-----------MAIN SCREEN-----------          
        root=Tk()
        root.title('GST Analyser')
        w = root.winfo_screenwidth()-350
        h = root.winfo_screenheight()-155
        root.geometry(f'{w}x{h}')
        #title frame------------
        titleframe=Frame(root,bg='aqua')
        titleframe.pack(side=TOP,fill=X)

        image = Image.open("title.png")
        photo = ImageTk.PhotoImage(image)
        topimg=Label(titleframe,image=photo)
        topimg.pack(side=LEFT)
            #title frame title
        fontstyle=Font(family='Broadway',size=40)
        toplabel=Label(titleframe,text='GST Analyser',font=fontstyle,bg='black',fg='white')
        toplabel.pack(fill=Y,side=LEFT,ipadx=110)
        
        fontstyle=Font(family='Algerian',size=32)
        frame1=Frame(root)
        frame1.pack()
        topic=Label(frame1,text='Let\'s begin with GST Analysis',font=fontstyle,justify=CENTER,pady=50,padx=100)
        topic.pack(fill=X)
        #Proceed button frame-----------
        frame2=Frame(root)
        frame2.pack()
        Label(frame2,text='\n\n').pack()
        l=Label(frame2,text='Welcome! Click below to proceed to login screen : ',font=(20),bg='yellow')
        l.pack()
        b=Button(frame2,text='Proceed to login',font=(20),command=loginscreen,padx=15,pady=15)
        b.pack()

        root.mainloop()

    def launch_main(): #takes to the main window
        root.destroy()
        run_gst_mgmt()

#launch intro/splash screen---------------   
    if splash==True: #if app is being run from beginning then splash screen will be shown or directly main screen will be shown
        root=Tk()
        
        w=root.winfo_screenwidth()
        h=root.winfo_screenheight()
        ww=502 #ww >> window width
        wh=255 #wh >> window height
        x,y=(w/2-ww/2),(h/2-(wh/2))
        geometry_text = "%dx%d+%d+%d" % (ww,wh,x,y) #this keeps the splash screen at the center of the screen
        root.geometry(geometry_text)
        root.overrideredirect(True) #this hides the title bar so that it looks like a splash screen
        xyz=Label(root)
        xyz.pack()
        fade_animation(img_name='splash.png',img_label=xyz) #function from 
        xyz.after(3500,launch_main)
        root.mainloop()
    else:
        run_gst_mgmt()


if __name__=='__main__':
    RunApp(splash=True)
