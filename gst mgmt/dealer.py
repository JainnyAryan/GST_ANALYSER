from tkinter import *
from PIL import Image,ImageTk
import mysql.connector as msql
from tkcalendar import Calendar,DateEntry
from tkinter import messagebox as msg
from gst_mgmt import RunApp
# root=Tk()
# root.geometry('800x600')
mydbb=msql.connect(
    host="localhost",
    user="root",
    passwd="1234")

mcurr=mydbb.cursor()

def runsql(c): 
	mcurr.execute(c)
	mydbb.commit()
	for i in mcurr:
		print(i)

runsql('create database if not exists temp;')
runsql('use temp')

def dealer_desk(parent,otbd,type,serial,gstin=None):
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
    def chk(P):
        if P.isdigit()==True:
            return True
        elif P=='':
            return True
        else:
            return False

    def check_data():
        def yesno():
            yn=msg.askquestion('Proceed','Do you want to continue with the data you entered?\nHave you checked the data before proceeding?')
            if yn=='yes':
                try:
                    runsql(f'''insert into {gstin}(s_no,type,year,month,gstin,firm_name,invoice_no,invoice_date,commodity_name,value,tax_rate,tax_amt) values({serial},'{type}','{year}','{month}','{pgstin}','{firm_name}','{invoice}','{invoice_date}','{commodity_name}',{value},{tax_rate},{tax_amt});''')
                    bproceed1.config(state=DISABLED)
                    if serial==1:
                        dealer_desk(parent=parent,otbd=[confirm,bcanvas,bscroll],type='Sale',serial=2,gstin=gstin)
                        parent.deiconify()
                        msg.showinfo('Success','Purchase details entered successfully!\nNow enter the sale details!')
                    if serial==2:
                        confirm.destroy()
                        msg.showinfo('Success','Sale info has been registered!\nYour bill has been successfully registered!')
                        parent.destroy()
                        RunApp(splash=False) #this will launch the main screen of the app without the splash screen
                        
                except Exception as ee:
                    print(ee)
                    msg.showerror('Error','Some error occured, please try again!')

            else: #block to be executed when NO is pressed in the askquestion messagebox
                confirm.destroy() #kills the window of confirmation if user hasn't verified what all he has entered
                parent.deiconify() #unhides the parent window
                msg.showinfo('Correction','Make corrections and then proceed !')
                
        year = year_var.get()
        month = month_var.get()
        pgstin = pgstin_var.get().strip()
        firm_name = firm_name_var.get().strip()
        invoice = invoice_var.get().strip()
        invoice_date = str(invoice_date_entry.get_date())
        commodity_name = commodity_name_var.get().strip()
        tax_rate=tax_rate_var.get()
        value=value_var.get()
        tax_amt=tax_amt_var.get()

        if year=='Choose year' or month=='Choose month' or len(pgstin)==0 or len(firm_name)==0 or len(invoice)==0 or len(commodity_name)==0 or len(value)==0 or tax_rate==0 or len(tax_amt)==0:
            if year=='Choose year':
                year_entry.config(bg='red')
            else:
                year_entry.config(bg='white')
            if month=='Choose month':
                month_entry.config(bg='red')
            else:
                month_entry.config(bg='white')
            if len(pgstin)==0 or len(pgstin)!=15:
                pgstin_entry.config(bg='red')
            else:
                pgstin_entry.config(bg='white')
            if len(firm_name)==0:
                firm_name_entry.config(bg='red')
            else:
                firm_name_entry.config(bg='white')
            if len(invoice)==0:
                invoice_entry.config(bg='red')
            else:
                invoice_entry.config(bg='white')
            if len(commodity_name)==0:
                commodity_name_entry.config(bg='red')
            else:
                commodity_name_entry.config(bg='white')
            if len(value)==0:
                value_entry.config(bg='red')
            else:
                value_entry.config(bg='white')
            if tax_rate==0:
                tax_rate_entry.config(bg='red')
            else:
                tax_rate_entry.config(bg='white')
            if len(tax_amt)==0:
                tax_amt_entry.config(bg='red')
            else:
                tax_amt_entry.config(bg='white')
            msg.showerror('Error!','Fill out all the fields!')

        elif len(pgstin)!=15:
            tax_amt_entry.config(bg='white')
            tax_rate_entry.config(bg='white')
            value_entry.config(bg='white')
            commodity_name_entry.config(bg='white')
            invoice_entry.config(bg='white')
            firm_name_entry.config(bg='white')
            month_entry.config(bg='white')
            year_entry.config(bg='white')
            pgstin_entry.config(bg='red')
            msg.showerror('Error','Enter valid GSTIN!')
        #------CONFIRMATION WINDOW-------
        else:
            tax_amt_entry.config(bg='white')
            tax_rate_entry.config(bg='white')
            value_entry.config(bg='white')
            commodity_name_entry.config(bg='white')
            invoice_entry.config(bg='white')
            firm_name_entry.config(bg='white')
            month_entry.config(bg='white')
            year_entry.config(bg='white')
            pgstin_entry.config(bg='white')
            value=int(value)
            tax_amt=int(tax_amt)
            def donothing(): #callback function to prevent closing of the confirmation window
                msg.showerror('Error','You cannot close the window\nPlease click on the proceed button !')
            
            parent.withdraw() #hides the parent window
            confirm=Tk()
            confirm.protocol('WM_DELETE_WINDOW',donothing) #this binds the 'X' close button with the function 'donothing'
            confirm.title('Confirm the entries')
            bframe1=Frame(confirm,padx=100,pady=40,bg='blue')
            Label(bframe1,text='---Before proceeding, once check what all you have entered---',font=(15),bg='red',fg='white').grid(row=0,columnspan=4,padx=10,sticky='nsew')
            a={'Year :':year,'Month :':month,'GSTIN :':pgstin,'Firm Name :':firm_name,'Invoice No. :':invoice,'Invoice Date':invoice_date,'Commodity Name :':commodity_name,'Value :':value,'Tax Rate (in %) :':tax_rate,'Tax Amt. :':tax_amt}
            c=1
            for field in a:
                Label(bframe1,text=field,font=(8),borderwidth=2,relief='solid',anchor=W,padx=5).grid(row=c,column=1,columnspan=1,sticky='nsew')
                Label(bframe1,text=a[field],font=(8),borderwidth=2,relief='solid',anchor=W,padx=5).grid(row=c,column=2,sticky='nsew',columnspan=1)
                c+=1
            
                #proceed button------------
            bproceed1=Button(bframe1,text='Proceed',font=(15),bg='orange',fg='white',padx=15,pady=5,command=yesno)
            bproceed1.grid(row=c+1,columnspan=4,sticky='nsew',padx=10)
            bframe1.pack()
            confirm.mainloop()
    
    
#------------MAIN WINDOW----------------------
    try: #clearing the window-------
        for obj in otbd: #otbd -->> Objects to be destroyed
            obj.destroy()
    except Exception as ee:
        print('dealer.py : ',ee)

    bcanvas=Canvas(parent,bg='blue')
    bscroll=Scrollbar(parent,orient='vertical',command=bcanvas.yview)
    bframe=Frame(bcanvas,padx=100,pady=40,bg='blue')
    Label(bcanvas,text=f'{type} Details',font=(20),fg='white',bg='black').pack()
    # Declaring the textvariables------------------
    pgstin_var,firm_name_var,invoice_var,commodity_name_var,year_var,month_var=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    value_var,tax_rate_var,tax_amt_var=StringVar(),IntVar(),StringVar()
    #year entry-------------
    years=['17-18','18-19','19-20','20-21']
    year_label=Label(bframe,text='Year : ',font=(10),justify=LEFT,bg='blue',fg='white')
    year_label.grid(row=0,column=1,sticky='w')
    year_entry=OptionMenu(bframe,year_var,*years)
    year_entry.grid(row=0,column=2,sticky='w')
    year_var.set('Choose year') 
    #month entry------------
    months=['01','02','03','04','05','05','06','07','08','09','10','11','12']
    year_label=Label(bframe,text='Month : ',font=(10),bg='blue',fg='white')
    year_label.grid(row=1,column=1,sticky='w',pady=10)
    month_entry=OptionMenu(bframe,month_var,*months)
    month_entry.grid(row=1,column=2,sticky='w',pady=10)
    month_var.set('Choose month')
    #purchase gstin entry-------------
    pgstin_label=Label(bframe,text='GSTIN : ',font=(10),bg='blue',fg='white')
    pgstin_label.grid(row=2,column=1,sticky='w',pady=10)
    pgstin_entry=Entry(bframe,textvariable=pgstin_var,font=(10),bd=3,validate='key',validatecommand=(parent.register(chk_gstin),'%P'))
    pgstin_entry.grid(row=2,column=2,sticky='w',pady=10)
    #firm name entry-------------
    firm_name_label=Label(bframe,text='Firm Name : ',font=(10),bg='blue',fg='white')
    firm_name_label.grid(row=3,column=1,sticky='w',pady=10)
    firm_name_entry=Entry(bframe,textvariable=firm_name_var,font=(10),bd=3)
    firm_name_entry.grid(row=3,column=2,sticky='w',pady=10)
    #invoice no. entry------------
    invoice_label=Label(bframe,text='Invoice No. : ',font=(10),bg='blue',fg='white')
    invoice_label.grid(row=4,column=1,sticky='w',pady=10)
    invoice_entry=Entry(bframe,textvariable=invoice_var,font=(10),bd=3)
    invoice_entry.grid(row=4,column=2,sticky='w',pady=10)
    #invoice date entry-------------
    invoice_date_label=Label(bframe,text='Invoice Date : ',font=(10),bg='blue',fg='white')
    invoice_date_label.grid(row=5,column=1,sticky='w',pady=10)
    invoice_date_entry=DateEntry(bframe,width=12, background='darkblue',foreground='white', borderwidth=3)
    invoice_date_entry.grid(row=5,column=2,sticky='w',pady=10)
    #commodity name entry------------
    commodity_name_label=Label(bframe,text='Commodity Name : ',font=(10),bg='blue',fg='white')
    commodity_name_label.grid(row=6,column=1,sticky='w',pady=10)
    commodity_name_entry=Entry(bframe,textvariable=commodity_name_var,font=(10),bd=3)
    commodity_name_entry.grid(row=6,column=2,sticky='w',pady=10)
    #value entry------------
    value_label=Label(bframe,text='Value : \n(in Rs. , enter full value in digits) ',font=(10),bg='blue',fg='white',justify=LEFT)
    value_label.grid(row=7,column=1,sticky='w',pady=10)
    value_entry=Entry(bframe,textvariable=value_var,font=(10),bd=3,validate='key',validatecommand=(parent.register(chk),'%P'))
    value_entry.grid(row=7,column=2,sticky='w',pady=10)    
    #tax rate entry-----------
    rates_of_tax=[5,12,18,28]
    tax_rate_label=Label(bframe,text='Rate of tax (in %) : ',font=(10),bg='blue',fg='white',justify=LEFT)
    tax_rate_label.grid(row=8,column=1,sticky='w',pady=10)
    tax_rate_entry=OptionMenu(bframe,tax_rate_var,*rates_of_tax)
    tax_rate_entry.grid(row=8,column=2,sticky='w',pady=10)
    #tax amt entry-----------
    tax_amt_label=Label(bframe,text='Tax amount : \n(in Rs. , enter full value in digits) ',font=(10),bg='blue',fg='white',justify=LEFT)
    tax_amt_label.grid(row=9,column=1,sticky='w',pady=10)
    tax_amt_entry=Entry(bframe,textvariable=tax_amt_var,font=(10),validate='key',bd=3,validatecommand=(parent.register(chk),'%P'))
    tax_amt_entry.grid(row=9,column=2,sticky='w',pady=10)      
    #proceed button------------
    bproceed=Button(bframe,text='Proceed',font=(15),bg='orange',fg='white',padx=15,pady=5,command=check_data)
    bproceed.grid(row=11,columnspan=5,sticky='nsew')
    #setting up the scrollbar in the canvas
    bcanvas.create_window(0,0,anchor='center',window=bframe)
    bcanvas.update_idletasks()
    bcanvas.configure(scrollregion=bcanvas.bbox('all'),yscrollcommand=bscroll.set)
    bcanvas.pack(fill='both',expand=True,side='left')
    bscroll.pack(side=RIGHT,fill=Y)
    
    # parent.mainloop()

# dealer_desk(root,[])

