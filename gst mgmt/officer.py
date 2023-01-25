from tkinter import *
from PIL import Image,ImageTk
import mysql.connector as msql1
from tkcalendar import Calendar,DateEntry
from tkinter import messagebox as msg
from datetime import datetime
import matplotlib.pyplot as plt

# from gst_mgmt import RunApp
# root=Tk()
# root.geometry('800x600')
mydbb1=msql1.connect(
    host="localhost",
    user="root",
    passwd="1234")

mcurr1=mydbb1.cursor()

def runsql1(c): 
	mcurr1.execute(c)
	mydbb1.commit()
	for i in mcurr1:
		print(i)
        
runsql1('use gst')

def analysis_window(gstin,parent):
    parent.state('zoomed') #maximizes the window
    def show_graph(): #graphs section
        value=info[1][9]
        tax_rate=info[1][10]
        inserted_tax=info[1][11]
        original_tax=value*(tax_rate/100)
        f,(graph_bar,graph_pie)=plt.subplots(1,2,sharex='col',figsize=(10,5))
        graph_bar.bar(['Original Tax','Inserted Tax \nby dealer'],[original_tax,inserted_tax],color=['orange','blue'])
        graph_bar.set_ylabel('Tax on sale of goods (in Rs.)')
        tax_not_given=abs(original_tax-inserted_tax) #absolute if the dealer enters original_tax greater than inserted_tax by mistake
        tax_not_given=round(tax_not_given,2) #rounding off the unpaid tax amount to 2 decimal places
        graph_pie.pie([original_tax,tax_not_given],labels=['Original Tax',f'Tax Unpaid\nRs. {tax_not_given}'],autopct='%1.1f%%',colors=['orange','red'])
        plt.show()

    runsql1('use temp')
    mcurr1.execute(f'select * from {gstin};')
    info=mcurr1.fetchall() #gets the purchase and sale details of the selected dealer
    
    main=PanedWindow(parent)
    graph_pane=LabelFrame(main,text='Graphical Analysis')
    main.add(graph_pane)
    main.pack(fill=X,expand=True)
    #creating purchase details pane----
    main1=PanedWindow(main,orient=VERTICAL)
    main.add(main1)
    purchase_details_pane=LabelFrame(main1,text='Purchase Details')
    main1.add(purchase_details_pane)
    
    #showing purchase details----
    a={'1. Year :':info[0][2],'2. Month :':info[0][3],'3. GSTIN :':info[0][4],'4. Firm Name :':info[0][5],'5. Invoice No. :':info[0][6],'7. Invoice Date':info[0][7],'8. Commodity Name :':info[0][8],'9. Value :':info[0][9],'10. Tax Rate (in %) :':info[0][10],'11. Tax Amt. :':info[0][11]} #info is the tuple of details from the sql database (at line 37)
    c=1
    for field in a:
        Label(purchase_details_pane,text=field,borderwidth=2,relief='solid',anchor=W,padx=5).grid(row=c,column=1,columnspan=1,sticky='nsew')
        Label(purchase_details_pane,text=a[field],borderwidth=2,relief='solid',anchor=W,padx=5).grid(row=c,column=2,sticky='nsew',columnspan=1)
        c+=1
    
    #creating sale details pane----
    main2=PanedWindow(main1)
    main1.add(main2)
    sale_details_pane=LabelFrame(main,text='Sale Details',height=100,width=10)
    main2.add(sale_details_pane)
    #showing sale details----
    a={'1. Year :':info[0][2],'2. Month :':info[0][3],'3. GSTIN :':info[0][4],'4. Firm Name :':info[0][5],'5. Invoice No. :':info[0][6],'7. Invoice Date':info[0][7],'8. Commodity Name :':info[0][8],'9. Value :':info[0][9],'10. Tax Rate (in %) :':info[0][10],'11. Tax Amt. :':info[0][11]}
    c=1
    for field in a:
        Label(sale_details_pane,text=field,font=(8),borderwidth=2,relief='solid',anchor=W,padx=5).grid(row=c,column=1,columnspan=1,sticky='nsew')
        Label(sale_details_pane,text=a[field],font=(8),borderwidth=2,relief='solid',anchor=W,padx=5).grid(row=c,column=2,sticky='nsew',columnspan=1)
        c+=1
            
    #show graphs button and alert label----
    b=Button(graph_pane,text='Show Graph',fg='white',bg='orange',font=(20),command=show_graph)
    b.pack(padx=10,anchor=CENTER)
    
    tax_rate=info[1][10]
    value=info[1][9]
    inserted_tax=info[1][11]
    original_tax=value*(tax_rate/100)
    if inserted_tax!=original_tax:
        Label(graph_pane,text='Unpaid tax found! \nCheck the graphs section!',fg='red',font=(20)).pack()
    else:
        Label(graph_pane,text='No tax issue found :)',fg='green',font=(20)).pack()
    
def officer_desk(parent,otbd):
    def get_selection():
        sel=dealer_listbox.get(ACTIVE)
        sel1=sel.split('|')
        gstin=sel1[0].strip()
        a.destroy()
        dealer_listframe.destroy()
        analysis_window(gstin=gstin,parent=parent)
    try: #clearing the window-------
        for obj in otbd: #otbd -->> Objects to be destroyed
            obj.destroy()
    except Exception as ee:
        print('officer.py : ',ee)
    
#------------MAIN WINDOW----------------------
    a=Label(parent,text='Welcome officer!',font=(20),padx=20,fg='white',bg='orange')
    a.pack(anchor=CENTER,side=TOP)
    
    dealer_listframe=LabelFrame(parent,text='List of dealers')
    dealer_listframe.pack(fill=X,side=TOP)
    
    scr=Scrollbar(dealer_listframe)
    scr.pack(fill=Y,side=RIGHT)
    
    b=Label(dealer_listframe,text='Format : GSTIN of the dealer | Dealer/Firm Name | Time Registered',font=(5))
    b.pack(anchor=CENTER)
    
    dealer_listbox=Listbox(dealer_listframe,yscrollcommand=scr.set)
    
    mcurr1.execute('select dealer_gstin,dealer_name,dealer_email,time_added from dealers order by time_added desc;')
    dealer_list=mcurr1.fetchall()
    
    for dealer in dealer_list:
        time=dealer[3].strftime("%d/%m/%Y, %H:%M:%S")
        dealer_listbox.insert(END,(dealer[0] + ' '*5 + '|' + ' '*5 + dealer[1] + ' '*5 + '|' + ' '*5 + dealer[2] + ' '*5 + '|' + ' '*5 + time))
    
    dealer_listbox.pack(expand=True,fill=X)
    
    scr.config(command=dealer_listbox.yview)
    
    open=Button(dealer_listframe,text='Open',font=(15),bg='blue',fg='white',padx=10,command=get_selection)
    open.pack()
    
    
    # parent.mainloop()

# officer_desk(root,[])
