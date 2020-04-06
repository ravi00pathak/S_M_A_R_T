#this is the real program that uses the information provided by the finalpro.py and create a illusion of the required software demanding by user
# this is the import section
import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import date
from tkinter import messagebox 
from csv import DictWriter
import os
from csv import DictReader
from csv import reader
from csv import writer
from functools import partial

# these are 3 process to read data from the file created by the finalpro.py
with open("pnam.csv","r") as e:
    csd=DictReader(e)
    for row in csd:
        project=row['Project_Name']
        databasen=row['Database']
       
with open("Pass.csv","r") as p:
    csv=DictReader(p)
    for row in csv:
        choice=row["choice"]

with open("entry.csv","r") as e:
    csd=DictReader(e)
    for row in csd:
        entry=row['Entry_Name'].split(",")
    en=[]
    for i in entry:
        en.append(i.replace(" ","_"))
#till here
    
# this is fuction that read data form the database and fill the selected treeview that i want .
# here a is the parameter that show the no. of selected treeview  
def action(a,trev):
    if a==5 and choice != 'housework':
        order=order_var5.get()
    elif a==7:
        name=name_search.get()
    con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
    mycursor=con.cursor()
    if a==3:
        mycursor.execute(f"SELECT * FROM {databasen}")
    elif a==5:
        if choice=='education':
            mycursor.execute(f"SELECT * FROM {databasen} where Fee>0 and {en[1]}=\"{order}\" ")
        if choice=='housework':
            mycursor.execute(f"SELECT * FROM {databasen} where {en[1]}>0  ")
    elif a==7:
        mycursor.execute(f"SELECT * FROM {databasen} where {en[0]}=\"{name}\" ")
    else:
        mycursor.execute(f"SELECT * FROM {databasen}")
    result=mycursor.fetchall()
    if result == [] and a != 9:
        messagebox.showinfo('info',"No value find")
    trev.delete(*trev.get_children())
    index=iid=0
    for i in result:
        trev.insert("",index,iid,values=i)
        index=iid=index+1
    con.commit()
    
# fuction that contain the logic used for print the data through the ms excel
def action6(a):
    con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
    mycursor=con.cursor()
    listf2=[]
    listf2=en.copy()
    if choice == 'education':
        listf2.append("Fee")
    if choice == 'housework':
        listf2.append('Payment_done')
    if a==1:
        mycursor.execute(f"SELECT * FROM {databasen}")
    elif a==2:
        if choice == 'education':
            mycursor.execute(f"SELECT * FROM {databasen} where Fee>0")
        if choice == 'housework':
            mycursor.execute(f"SELECT * FROM {databasen} where {en[1]}>0")
    else:
        order=order_var5.get()
        mycursor.execute(f"SELECT * FROM {databasen} where Fee>0 and {en[1]}=\"{order}\" ")
    result=mycursor.fetchall()
    with open('file.csv','w',newline='') as f:
        csw=DictWriter(f,fieldnames=[i for i in listf2])
        if os.stat('file.csv').st_size==0:
            csw.writeheader()
        for i in result:
            csw.writerow({listf2[k]:i[k] for k in range(len(listf2))})    
    file="file.csv"
    os.startfile(file)
    page(1)
    
# fuction that is used to pack or unpack the selected frame    
def page(n):
    f1.pack_forget()
    f2.pack_forget()
    f3.pack_forget()
    f4.pack_forget()
    f5.pack_forget()
    f6.pack_forget()
    frame.pack_forget()
    frameoption.grid_forget()
    if n==1:
        f1.pack(side="left")
    elif n==2:
        f2.pack(side="left")
    elif n==3:
        f3.pack(side="left")
        action(3,trev1)
    elif n==4:
        if choice == "other":
            frame.pack(side="left")
        else:
            f4.pack(side="left")
    elif n==5:
        if choice == "other":
            frame.pack(side="left")
        else:
            f5.pack(side="left")
            if choice == 'education':
                global order_var5
                global o2
                o2.grid_forget()
                global classname
                classname=[]
                with open ('Prem.csv','r') as c:
                    csv=DictReader(c)
                    classname=[row['class'] for row in csv]
                o2=ttk.Combobox(f5,values=classname,width=30,textvariable=order_var5,state="readonly")
                o2.current(0)
                o2.grid(row=2,column=0,padx=10)
            if choice == 'housework':
                action(5,trev2)
    elif n==6:
        action6(1)
    else:
        f6.pack(side="left")
        frameuser.grid(row=1,column=0)
        if choice=="housework":
            global l
            l.grid_forget()
            with open("Prem.csv","r") as fh:
                csb=DictReader(fh)
                for row in csb:
                    mongn=row['amount']
            l=ttk.Label(framebug,text=f"Your current budget ramain {mongn} rs...")
            l.grid(row=5,column=0,pady=5)
        action(9,trev4)


# menub works for the menu button
def menub():
    Menubu.pack_forget()
    f.pack(side='top',anchor='ne')
    framem.configure(style='My.TFrame')
    f.configure(style='My.TFrame')

# menub works for the back button 
def back():
    f.pack_forget()
    Menubu.pack(side='top',anchor='ne',padx=50,pady=30)
    framem.configure(style='Mynew.TFrame')
    f.configure(style='Mynew.TFrame')
    
# from here the main function is start
root=tk.Tk()
root.title(f"{project}")
w=root.winfo_screenwidth()
h=root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w,(h-70)))

style1=ttk.Style()
style1.configure('My.TFrame', background='#334353')
style1.configure('Mynew.TFrame', background='#f2f2f2')

# frame that shows in the top side 
fram=ttk.Frame(root,style='My.TFrame')
fram.configure(width=w,height=100)
fram.pack(side="top")

# frame on which the menu button is created in the right side
framem=ttk.Frame(root)
framem.configure(width=80,height=h,style='Mynew.TFrame')
framem.pack(side="right" ,fill="y",expand=0)
Menubu=ttk.Button(framem,text="--\n--\n--",command=menub)
Menubu.pack(side='top',anchor='ne',padx=50,pady=30)

# main frame on which different frame is created
fr=ttk.Frame(root,width=800,height=500)
fr.pack(side="top")
f1=ttk.Frame(fr)
f2=ttk.Frame(fr)
f3=ttk.Frame(fr)
f4=ttk.Frame(fr)
f5=ttk.Frame(fr)
f6=ttk.Frame(fr)
frame=ttk.Frame(fr)
ttk.Label(frame,text="PLEASE CONTACT US TO MANAGE PROCESS PHASE.",font="Andalus 20 italic").grid(row=0,column=0,pady=20)
    
# Frame that contain the menu button and it will shows after the menu button is pressed
f=ttk.Frame(framem,style='Mynew.TFrame')
page1btn=ttk.Button(f,text='HOME',command=partial(page,1))
page2btn=ttk.Button(f,text='EDIT',command=partial(page,2))
page3btn=ttk.Button(f,text='VIEW',command=partial(page,3))
if choice == "education":
    ch1="FEE DEPOSIT"
    ch2="FEE DEFAULTER"
elif choice == "business":
    ch1="MONEY DEPOSIT"
    ch2="MONEY DEFAULTER"
elif choice == "housework":
    ch1="PAYMENTS"
    ch2="PAYMENTS DUE"
else:
    ch1="DEPOSIT PAGE"
    ch2="DUE DEPOSITS"
page4btn=ttk.Button(f,text=ch1,command=partial(page,4))
page5btn=ttk.Button(f,text=ch2,command=partial(page,5))
page6btn=ttk.Button(f,text='PRINT LIST',command=partial(page,6))
page7btn=ttk.Button(f,text='USER SETTING',command=partial(page,7))
back=ttk.Button(f,text="BACK",command=back)
page1btn.pack(side="top",fill='x',padx=10,pady=5)
page2btn.pack(side="top",fill='x',padx=10,pady=5)
page3btn.pack(side="top",fill='x',padx=10,pady=5)
page4btn.pack(side="top",fill='x',padx=10,pady=5)
page5btn.pack(side="top",fill='x',padx=10,pady=5)
page6btn.pack(side="top",fill='x',padx=10,pady=5)
page7btn.pack(side="top",fill='x',padx=10,pady=5)
back.pack(fill='x',padx=50,pady=5)
f1.pack()

# fuction that works for the home button in the menu
def action1():
    con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
    result=True
    # for education choice
    if choice == "education":
        mycursor=con.cursor()
        mycursor.execute(f"INSERT INTO {databasen} ({en[0]}) VALUES (\"{entryvar[0].get()}\")")
        r=entryvar[1].get()
        with open("Prem.csv","r") as f:
            csv=DictReader(f)
            for row in csv:
                if row['class'] == r:
                    mycursor=con.cursor()   
                    mycursor.execute(f"update {databasen} set Fee=\"{row['fee']}\" where {en[0]}=\"{entryvar[0].get()}\"")
                    result=True
                    break
                else:    
                    result=False
            if result == False:
                messagebox.showerror("Error","Unknown course name \n Please add the course name and it\'s fee first")    
                mycursor=con.cursor()   
                mycursor.execute(f"delete from {databasen} where {en[0]}=\"{entryvar[0].get()}\" ")
    
    # for housework choice        
    if choice == "housework":
        r=entryvar[0].get()
        mycursor=con.cursor()   
        mycursor.execute(f"select {en[0]},{en[1]} from  {databasen}  where {en[0]}=\"{entryvar[0].get()}\" ")
        resultd=mycursor.fetchall()
        if resultd == []:
            mycursor=con.cursor()
            mycursor.execute(f"insert into {databasen} ({en[0]},{en[1]}) values (\"{entryvar[0].get()}\",\"{entryvar[1].get()}\")")
            result=True
            messagebox.showinfo('Info',"Data has been added")            
        else:
            mycursor=con.cursor()
            mycursor.execute(f"update {databasen} set {en[1]}=\"{int(resultd[0][1])+int(entryvar[1].get())}\" where {en[0]}=\"{entryvar[0].get()}\"  ")
            result=False     
            messagebox.showinfo('Info',f"Bill Amount has been added into the account of '{entryvar[0].get().upper()}' ")            
    
    # for other choice
    if choice =='other':
        mycursor=con.cursor()
        mycursor.execute(f"INSERT INTO {databasen} ({en[0]}) VALUES (\"{entryvar[0].get()}\")")
        result=True
    
    # logic that write the input data in the database
    if result==True:           
        mycursor=con.cursor()
        k=0
        for j in range(len(en)):
            if k==0:
                k=1
                continue            
            mycursor.execute(f"update {databasen} set {en[j]}=\"{entryvar[j].get()}\" where {en[0]}=\"{entryvar[0].get()}\"  ")
        if choice == 'housework':
            mycursor=con.cursor()
            mycursor.execute(f"update {databasen} set Payment_done=0 where {en[0]}=\"{entryvar[0].get()}\"  ") 
    con.commit()
    for e in entryvar:
        e.delete(0, "end")
        e.insert(0,"")
         
#this is the piece of code that uses the above fuction and implement the home button logic        
bigl1=ttk.Label(f1,text="HOME")
bigl1.configure(font="Andalus 24 bold",justify="center")
bigl1.grid(row=0,columnspan=3)
style1.configure('My2.TLabel',font="Algerian 12 italic")
rown=1
for i in entry:
    ttk.Label(f1,text=i.upper(),style='My2.TLabel').grid(row=rown,column=0,sticky=tk.W)
    rown=rown+1
entryvar=[]
rown=1
for i in range(len(entry)):
    entryvar.append(ttk.Entry(f1,width=30))
    entryvar[i].grid(row=rown,column=1,padx=10,pady=10)
    rown=rown+1
entryvar[0].focus()
style1.configure('My3.TButton',font='bold')
ttk.Button(f1,text="SUBMIT",style='My3.TButton',command=action1).grid(row=rown,columnspan=3)
#till here 



# function for the Edit button on the menu bar
def selectitem(event):
    curItem=trev3.focus()
    d=trev3.item(curItem)
    list=d['values']
    win=tk.Tk()
    win.title("Edit")
    frame=ttk.Frame(win)
    frame.pack()
    rown=1
    for i in entry:
        ttk.Label(frame,text=i,style='My2.TLabel').grid(row=rown,column=0,sticky=tk.W)
        rown=rown+1
    entryv=[]
    rown=1
    for i in range(len(entry)):
        entryv.append(ttk.Entry(frame,width=30))
        entryv[i].insert(0,list[i])
        entryv[i].grid(row=rown,column=1,padx=10,pady=10)
        rown=rown+1
    #fuction that is used by selectitem and actually update the table in the database
    def action2():
        if choice == 'education':
            whn=list[0]
            whr=list[1]
            if entryv[1].get()==whr:
                con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
                mycursor=con.cursor()
                mycursor.execute(f"UPDATE {databasen} SET {en[0]}=\"{entryv[0].get()}\" where {en[0]}=\"{whn}\" and {en[1]}=\"{whr}\"    ")
                for kk in range(1,len(en)):
                    mycursor.execute(f"UPDATE {databasen} SET {en[kk]}=\"{entryv[kk].get()}\" where {en[0]}=\"{entryv[0].get()}\" " )
                con.commit()
            else:
                messagebox.showerror('Error','You can\'t change the course. ') 
        
        if choice == 'housework':
            whn=list[0]
            whr=list[1]
            if int(entryv[1].get())==int(whr):
                con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
                mycursor=con.cursor()
                mycursor.execute(f"UPDATE {databasen} SET {en[0]}=\"{entryv[0].get()}\" where {en[0]}=\"{whn}\" and {en[1]}=\"{whr}\"    ")
                for kk in range(1,len(en)):
                    mycursor.execute(f"UPDATE {databasen} SET {en[kk]}=\"{entryv[kk].get()}\" where {en[0]}=\"{entryv[0].get()}\" " )
                con.commit()
            else:
                  messagebox.showerror('Error','You can\'t change the Bill amount ') 
        
        if choice == 'other':
            whn=list[0]
            whr=list[1]
            con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
            mycursor=con.cursor()
            mycursor.execute(f"UPDATE {databasen} SET {en[0]}=\"{entryv[0].get()}\" where {en[0]}=\"{whn}\" and {en[1]}=\"{whr}\"    ")
            for kk in range(1,len(en)):
                mycursor.execute(f"UPDATE {databasen} SET {en[kk]}=\"{entryv[kk].get()}\" where {en[0]}=\"{entryv[0].get()}\" " )
            con.commit()
        win.destroy()
        action(7,trev3)
    ttk.Button(frame,text="SUBMIT",command=action2).grid(row=8,columnspan=3)

# this is the piece of code that is used for implementing the edit button logic    
b1=ttk.Label(f2,text="EDIT",style="My2.TLabel")
b1.configure(font="Andalus 24 bold",justify="center")
b1.grid(row=0,columnspan=5)
ttk.Label(f2,text=f"Enter the {en[0]} to search").grid(row=1,column=0,padx=10)
name_search=tk.StringVar()
e=ttk.Entry(f2,width=30,textvariable=name_search)
e.grid(row=2,column=0)
ttk.Label(f2,text="Double click on item to select").grid(row=4,column=0,sticky=tk.W)
fra=ttk.Frame(f2,style="MY.TFrame")
fra.configure(width=500,height=400)
fra.grid(row=5,columnspan=5)
fra.pack_propagate(0)
trev3=ttk.Treeview(fra)
s21=ttk.Scrollbar(fra,orient="horizontal",command=trev3.xview)
s22=ttk.Scrollbar(fra,orient="vertical",command=trev3.yview)
trev3.configure(xscrollcommand=s21.set,yscrollcommand=s22.set)
s21.pack(side="bottom",fill="x")
s22.pack(side="right",fill="y")
trev3.pack(side="top",expand=True,fill="both",pady=10)
trev3["columns"]=[i for i in en]
trev3["show"]="headings"
for k in en:
    trev3.heading(k,text=k)
trev3.bind('<Double-Button-1>',selectitem)
ttk.Button(f2,text="SHOW",command=partial(action,7,trev3)).grid(row=2,column=1,padx=15)  
# till here

# Instruction that implement the view button logic 
ttk.Label(f3,text="VIEW",font="Andalus 24 bold",justify="center").grid(row=0,columnspan=5)
fra=ttk.Frame(f3,style="MY.TFrame")
fra.configure(width=500,height=400)
fra.grid(row=3,columnspan=5)
fra.pack_propagate(0)
trev1=ttk.Treeview(fra)
s31=ttk.Scrollbar(fra,orient="horizontal",command=trev1.xview)
s32=ttk.Scrollbar(fra,orient="vertical",command=trev1.yview)
trev1.configure(xscrollcommand=s31.set,yscrollcommand=s32.set)
s31.pack(side="bottom",fill="x")
s32.pack(side="right",fill="y")
trev1.pack(side="top",expand=True,fill="both",pady=10)
listf=[]
listf=en.copy()
if choice == 'education':
    listf.append('Fee')
if choice == 'housework':
    listf.append('Payment_done')
trev1["columns"]=[i for i in listf]
trev1["show"]="headings"
for k in listf:
    trev1.heading(k,text=k)
#till here



#fuction that is used for money deposit button on the menu
def action4():
    con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
    mycursor=con.cursor()
    if choice=="education":
        name=namestu.get()
        classs=classstu.get()
        mycursor=con.cursor()
        mycursor.execute(f"SELECT Fee from {databasen} where {en[0]}=\"{name}\" and {en[1]}=\"{classs}\" ")
        stu=mycursor.fetchone()
        if stu != None:
            fee=str(stu[0])
            if int(fee) == 0:
                messagebox.showerror('Error','Full fee deposit for this student')
            else:
                mycursor=con.cursor()
                with open("Prem.csv",'r') as f:
                    csv=DictReader(f)
                    for row in csv:
                        if classs==row['class']:
                            mon=row['fee']
                if int(money.get()) <= int(mon):
                    mycursor.execute(f"UPDATE {databasen} SET Fee={int(fee)-max(0,int(money.get()))} where {en[0]}=\"{name}\" AND {en[1]}=\"{classs}\" ")
                else:
                    mycursor.execute(f"UPDATE {databasen} SET Fee=0 where {en[0]}=\"{name}\" AND {en[1]}=\"{classs}\"  ")
                    messagebox.showinfo('Info',f'you have to return {int(money.get())-int(mon)} rupees to customer')
                messagebox.showinfo('Info','fee deposit')
            entryfee1.delete(0,"end")
            entryfee2.delete(0,"end")
            entryfee3.delete(0,"end")
        else:
            messagebox.showerror('Error','Name/class is not found in database')
    
    if choice == 'housework':
        nam=nmofc.get()
        mycursor=con.cursor()
        mycursor.execute(f"SELECT {en[1]},Payment_done from {databasen} where {en[0]}=\"{nam}\"  ")
        stu=mycursor.fetchone()
        if stu != None:
            if int(stu[0]) == 0:
                messagebox.showerror('Error','Full bill paid')
            else:
                mycursor=con.cursor()
                mon=money.get()
                with open('Prem.csv','r') as f:
                    csb=DictReader(f)
                    for row in csb:
                        bud=row['amount']
                if int(bud)<int(mon) or int(bud) == 0:
                    messagebox.showwarning('Warning','You have not sufficient budget')
                    return(0)
                if int(mon) <= int(stu[0]):
                    mycursor=con.cursor()
                    mycursor.execute(f"UPDATE {databasen} SET {en[1]}=\"{str(int(stu[0])-max(0,int(mon)))}\" where {en[0]}=\"{nam}\"  ")
                    mycursor=con.cursor()
                    mycursor.execute(f"UPDATE {databasen} SET Payment_done=\"{str(int(stu[1])+max(0,int(mon)))}\" where {en[0]}=\"{nam}\"  ")
                    pay=int(bud)-int(mon)
                else:
                    mycursor.execute(f"UPDATE {databasen} SET {en[1]}=\"0\" where {en[0]}=\"{nam}\"")
                    mycursor=con.cursor()
                    mycursor.execute(f"UPDATE {databasen} SET Payment_done=\"{str(int(stu[1])+max(0,int(mon)))}\" where {en[0]}=\"{nam}\"  ")
                    messagebox.showinfo('Info',f'you are paying {int(mon)-int(stu[0])} rs more')
                    pay=int(bud)-int(stu[0])
                with open('Prem.csv','w',newline="") as f:
                    csb=DictWriter(f,fieldnames=['name','amount'])
                    csb.writeheader()
                    csb.writerow({
                        'name':'budget',
                        'amount':pay
                    })                        
                messagebox.showinfo('Info',f'Amount paid to {nam.upper()}')
            nmofc.delete(0,"end")
            entryfee3.delete(0,"end")
        else:
            messagebox.showerror('Error','Data is not found in database')
    con.commit()

#code used in the money deposit button in the menu
ttk.Label(f4,text=ch1,font="Andalus 24 bold",justify="center").grid(row=0,columnspan=5)    
if choice =="education":
    ttk.Label(f4,text="NAME OF STUDENT",style='My2.TLabel').grid(row=1,column=0,sticky=tk.W,pady=5)
    namestu=tk.StringVar()
    entryfee1=tk.Entry(f4,width=30,textvariable=namestu)
    entryfee1.grid(row=2,column=0,sticky=tk.W)
    ttk.Label(f4,text="ClASS OF STUDENT",style='My2.TLabel').grid(row=3,column=0,sticky=tk.W,pady=5)
    classstu=tk.StringVar()
    entryfee2=tk.Entry(f4,width=30,textvariable=classstu)
    entryfee2.grid(row=4,column=0,sticky=tk.W)
elif choice =="housework":
    ttk.Label(f4,text="BILL SENDER NAME",style='My2.TLabel').grid(row=1,column=0,sticky=tk.W,pady=5)
    nmofc=ttk.Entry(f4,width=30)
    nmofc.grid(row=2,column=0,sticky=tk.W,pady=5)
ttk.Label(f4,text="AMOUNT OF MONEY",style='My2.TLabel').grid(row=7,column=0,sticky=tk.W,pady=5)
money=tk.StringVar()
entryfee3=ttk.Entry(f4,width=30,textvariable=money)
entryfee3.grid(row=8,column=0,sticky=tk.W)
ttk.Button(f4,text="DEPOSIT",command=action4).grid(row=10,columnspan=2,pady=5)
# till here
 
# code used in the money defaulter button in the menu
ttk.Label(f5,text=ch2,font="Andalus 24 bold",justify="center").grid(row=0,columnspan=5)
if choice !='housework' and choice !='other':
    ttk.Label(f5,text="SELECT YOUR CHOICE FORM THE DRAGBOX").grid(row=1,column=0)
    order_var5=tk.StringVar()
    classname=[]
    if choice == 'education':
        with open ('Prem.csv','r') as c:
            csv=DictReader(c)
            classname=[row['class'] for row in csv]
    o2=ttk.Combobox(f5,values=classname,width=30,textvariable=order_var5,state="readonly")
    o2.current(0)
    o2.grid(row=2,column=0,padx=10)
fra=ttk.Frame(f5,style="MY.TFrame")
fra.configure(width=500,height=400)
fra.grid(row=4,columnspan=5)
fra.pack_propagate(0)
trev2=ttk.Treeview(fra)
s11=ttk.Scrollbar(fra,orient="horizontal",command=trev2.xview)
s12=ttk.Scrollbar(fra,orient="vertical",command=trev2.yview)
trev2.configure(xscrollcommand=s11.set,yscrollcommand=s12.set)
s11.pack(side="bottom",fill="x")
s12.pack(side="right",fill="y")
trev2.pack(side="top",expand=True,fill="both",pady=10)
listf=[]
listf=en.copy()
if choice == 'education':
    listf.append('Fee')
if choice == 'housework':
    listf.append('Payment_done')
trev2["columns"]=[i for i in listf]
trev2["show"]="headings"
for k in listf:
    trev2.heading(k,text=k)
if choice == 'education':
    ttk.Button(f5,text="SHOW",command=partial(action,5,trev2)).grid(row=2,column=1,padx=15)
    ttk.Button(f5,text='PRINT LIST',command=partial(action6,2)).grid(row=5,columnspan=5)
    ttk.Button(f5,text='PRINT CLASS LIST',command=partial(action6,3)).grid(row=7,columnspan=5,pady=10)
if choice == 'housework':
    ttk.Button(f5,text='PRINT LIST',command=partial(action6,2)).grid(row=5,columnspan=5)
#till here  

# fuction that uses by the user setting button in the menu
def security():
    name=E1.get()
    password=E2.get()
    E1.delete(0,'end')
    E2.delete(0,'end')
    
    with open("Pass.csv",'r') as f:
        csv=DictReader(f)
        for row in csv:
            if row['username'] == name and row['password'] == password:
                frameuser.grid_forget()
                frameoption.grid(row=1,column=0)
                return 1
    messagebox.showerror("Error","Invalid username or password")
    return 0

def passc():
    name=uname.get()
    passr=passw.get()
    passR=rpassw.get()
    if passr == passR:
        with open ("Pass.csv",'w',newline="") as a:
            csw=DictWriter(a,fieldnames=['username','password'])
            if os.stat('Pass.csv').st_size==0:
                csw.writeheader()
            csw.writerow({'username':name,'password':passr})
        messagebox.showinfo('Info','Your username and password have been change')
    else:
        messagebox.showerror('Error','Please enter the right password!')
    en1.delete(0,'end')
    en2.delete(0,'end')
    en3.delete(0,'end')
    
def delitem(event):
    ms=tk.messagebox.askquestion('Delete Itmes','Are you sure you want to delete the item\items')
    if ms == 'yes':
        curItem=trev4.selection()
        con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
        
        for i in curItem:
            d=trev4.item(i)['values']
            nam1=d[0]
            nam2=d[1]
            mycursor=con.cursor()
            mycursor.execute(f"DELETE FROM {databasen} WHERE {en[0]}=\"{nam1}\" and {en[1]}=\"{nam2}\" ")
        
        messagebox.showinfo('info',"item\items have been deleted")
        con.commit()
        action(9,trev4)
    
def add():
    c=cname.get()
    ff=feea.get()
    with open('Prem.csv','a',newline='') as f:
        csv=DictWriter(f,fieldnames=['class','fee'])
        csv.writerow({'class':c,'fee':int(ff)})
    cname.delete(0,"end")
    feea.delete(0,"end")
    additemtotrev5()
    messagebox.showinfo('Info',"Class has been added.")

def additemtotrev5():
    with open('Prem.csv','r') as f:
        result=DictReader(f)
        g=[]
        for i in result:
            g.append(tuple(i.values()))
        trev5.delete(*trev5.get_children())
        index=iid=0
        for i in g:
            trev5.insert("",index,iid,values=i)
            index=iid=index+1
        
def additem(event):
    addcuritem=trev5.focus()
    l=trev5.item(addcuritem)
    itemlist=l['values']
    win=tk.Tk()
    itemframe=tk.Frame(win)
    ttk.Label(itemframe,text="CLASS NAME").grid(row=0,column=0,sticky=tk.W,pady=10)
    ttk.Label(itemframe,text="FEE AMOUNT").grid(row=1,column=0,sticky=tk.W,pady=10)
    itementry1=ttk.Entry(itemframe,width=30)
    itementry2=ttk.Entry(itemframe,width=30)
    itementry1.grid(row=0,column=1,sticky=tk.W,pady=10)
    itementry2.grid(row=1,column=1,sticky=tk.W,pady=10)
    itementry1.insert(0,itemlist[0])
    itementry2.insert(0,itemlist[1])
    itemframe.pack()
    
    def setvalue(a):
        with open('Prem.csv','r') as re:
            with open('copy.csv','w',newline="") as wr:
                csb1=DictReader(re)
                csb2=DictWriter(wr,fieldnames=['class','fee'])
                csb2.writeheader()
                for i in csb1:
                    l=list(i.values())
                    if(a==1):
                        if l[0]==itemlist[0] and l[1]==str(itemlist[1]):
                            csb2.writerow({'class':itementry1.get(),'fee':itementry2.get()})
                        else:
                            csb2.writerow({'class':l[0],'fee':l[1]})
                    if (a==2):
                        if l[0] == itemlist[0] and l[1] == str(itemlist[1]):
                            pass
                        else:
                            csb2.writerow({'class':l[0],'fee':l[1]})
        
        
        os.remove('Prem.csv')
        os.rename('copy.csv','Prem.csv')
        if a==1:
            messagebox.showinfo('Info',"Data has been changed.")
        if a==2:
            messagebox.showinfo('Info',"Data has been deleted.")
        additemtotrev5()
        win.destroy()
        
    ttk.Button(itemframe,text="SAVE CHANGES",command=partial(setvalue,1)).grid(row=3,column=0,pady=10)
    ttk.Button(itemframe,text="DELETE DATA",command=partial(setvalue,2)).grid(row=3,column=1,pady=10)
    win.mainloop()

def addmon():
    with open("Prem.csv","r") as f:
        csb=DictReader(f)
        for row in csb:
            mong=int(row['amount'])
    mon =int(enbug.get())
    ms=tk.messagebox.askquestion('Add money',f'Are you sure you want to add {mon}rs to your budget? ')
    if ms == 'yes':
        with open("Prem.csv","w") as g:
            csb=DictWriter(g,fieldnames=['name','amount'])
            csb.writeheader()
            csb.writerow({
                'name': 'budget',
                'amount': f"{mon+mong}"
                })
        tk.messagebox.showinfo('info',f"Now you budget has been {mon+mong}rs !")
        global l
        l.grid_forget()
        with open("Prem.csv","r") as fh:
            csb=DictReader(fh)
            for row in csb:
                mongn=row['amount']
        l=ttk.Label(framebug,text=f"Your current budget ramain {mongn} rs...")
        l.grid(row=5,column=0,pady=5)
        enbug.delete(0,'end')
#till here

# code that used in the user setting button in the menu
ttk.Label(f6,text="USER SETTING",font="Andalus 24 bold",justify="center").grid(row=0,columnspan=5)
frameuser=ttk.Frame(f6)
frameuser.configure(width=100,height=100)
frameuser.grid(row=1,column=0)

ttk.Label(frameuser,text="USERNAME",style='My2.TLabel').grid(row=0,column=0,pady=10,sticky=tk.W)
E1=ttk.Entry(frameuser,width=30)
E1.grid(row=1,column=0)
ttk.Label(frameuser,text="PASSWORD",style='My2.TLabel').grid(row=2,column=0,pady=10,sticky=tk.W)
E2=ttk.Entry(frameuser,width=30)
E2.grid(row=3,column=0)
ttk.Button(frameuser,text="LOG IN",command=security).grid(row=4,columnspan=2,pady=10)

frameoption=ttk.Frame(f6)
nb=ttk.Notebook(frameoption)
page1=ttk.Frame(nb)
page21=ttk.Frame(nb)
page22=ttk.Frame(nb)
page3=ttk.Frame(nb)
page1.configure(width=500,height=350)
nb.add(page1,text="DELETE")
if choice == "education":
    nb.add(page21,text="ADD CLASS AND FEE")
if choice == "housework":
    nb.add(page22,text="ADD MONEY TO THE BUDGET")
nb.add(page3,text="CHANGE ID AND PASSWORD")
nb.pack()
ttk.Label(page1,text="Press 'Enter' after Select items",style='My2.TLabel').grid(row=0,column=0,sticky=tk.W,pady=10)
fra=ttk.Frame(page1,style="MY.TFrame")
fra.configure(width=500,height=400)
fra.grid(row=1,columnspan=5)
fra.pack_propagate(0)
trev4=ttk.Treeview(fra)
s41=ttk.Scrollbar(fra,orient="horizontal",command=trev4.xview)
s42=ttk.Scrollbar(fra,orient="vertical",command=trev4.yview)
trev4.configure(xscrollcommand=s41.set,yscrollcommand=s42.set)
s41.pack(side="bottom",fill="x")
s42.pack(side="right",fill="y")
trev4.pack(side="top",expand=True,fill="both")
trev4["columns"]=[i for i in en]
trev4["show"]="headings"
for k in en:
    trev4.heading(k,text=k)
action(9,trev4)
trev4.bind('<Return>',delitem)


if choice !='other':
    framfee=ttk.Frame(page21)
    framfee.configure(width=700,height=700)
    nb2=ttk.Notebook(framfee)
    frame1=ttk.Frame(nb2)
    frame2=ttk.Frame(nb2)
    frame1.configure(width=700,height=700)
    nb2.add(frame1,text="ADD NEW CLASS")
    nb2.add(frame2,text="MODIFY CLASS NAME & FEE")
    nb2.pack()
    framfee.pack()



    ot=ttk.Frame(frame1)
    ttk.Label(ot,text="Enter the class name",style='My2.TLabel').grid(row=0,column=0,pady=5,sticky=tk.W)
    cname=ttk.Entry(ot,width=30)
    cname.grid(row=1,column=0,pady=5,sticky=tk.W)
    ttk.Label(ot,text="Enter the amount of fee",style='My2.TLabel').grid(row=2,column=0,pady=5,sticky=tk.W)
    feea=ttk.Entry(ot,width=30)
    feea.grid(row=3,column=0,pady=5,sticky=tk.W)
    ttk.Button(ot,text="ADD",command=add).grid(row=5,columnspan=5,pady=10)
    ot.pack()

    ttk.Label(frame2,text="Double click on the item to select ",style='My2.TLabel').grid(row=0,column=0,sticky=tk.W,pady=10)
    fraa=ttk.Frame(frame2,style="MY.TFrame")
    fraa.configure(width=500,height=400)
    fraa.grid(row=1,columnspan=5)
    fraa.pack_propagate(0)
    trev5=ttk.Treeview(fraa)
    s51=ttk.Scrollbar(fraa,orient="horizontal",command=trev5.xview)
    s52=ttk.Scrollbar(fraa,orient="vertical",command=trev5.yview)
    trev5.configure(xscrollcommand=s51.set,yscrollcommand=s52.set)
    s51.pack(side="bottom",fill="x")
    s52.pack(side="right",fill="y")
    trev5.pack(side="top",expand=True,fill="both")
    trev5["columns"]=["CLASS_NAME","FEE_AMOUNT"]
    trev5["show"]="headings"
    trev5.heading("CLASS_NAME",text="CLASS_NAME")
    trev5.heading("FEE_AMOUNT",text="FEE_AMOUNT")
    additemtotrev5()
    trev5.bind('<Double-Button-1>',additem)


    if choice=="housework":
        framebug=ttk.Frame(page22)
        framebug.pack()
        ttk.Label(framebug,text="ADD MONEY TO BUDGET").grid(row=0,column=0,pady=5)
        enbug=ttk.Entry(framebug,width=30)
        enbug.grid(row=1,column=0,pady=5)
        with open("Prem.csv","r") as fg:
            csb=DictReader(fg)
            for row in csb:
                mong=row['amount']
        l=ttk.Label(framebug,text=f"Your current budget ramain {mong} rs...")
        l.grid(row=3,column=0,pady=5)
        ttk.Button(framebug,text="ADD MONEY",command=addmon).grid(row=2,column=0,pady=5)


tframe=ttk.Frame(page3)
tframe.pack()
ttk.Label(tframe,text="ENTER NEW USERNAME",style="My2.TLabel").grid(row=0,column=0,pady=10)
uname=tk.StringVar()
en1=ttk.Entry(tframe,width=30,textvariable=uname)
en1.grid(row=1,column=0)
ttk.Label(tframe,text="ENTER NEW PASSWORD",style="My2.TLabel").grid(row=2,column=0,pady=10)
passw=tk.StringVar()
en2=ttk.Entry(tframe,width=30,textvariable=passw)
en2.grid(row=3,column=0)
ttk.Label(tframe,text="CONFIGURE PASSWORD",style="My2.TLabel").grid(row=4,column=0,pady=10)
rpassw=tk.StringVar()
en3=ttk.Entry(tframe,width=30,textvariable=rpassw)
en3.grid(row=5,column=0)
ttk.Button(tframe,text='SUBMIT',command=passc).grid(row=6,column=0)

root.mainloop()
#end of program