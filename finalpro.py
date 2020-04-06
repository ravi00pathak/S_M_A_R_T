# hii my name is ravendra kumar pathak and i am the developer of this program. I am going to explain the struture of this program.
# this is the import section.
# these are some module that i have used in the program.
import tkinter as tk
from tkinter import ttk
import os
import shutil
from csv import DictWriter
import mysql.connector
from functools import partial
from tkinter import messagebox 
from tkinter import messagebox

#this is fuction containing the logic for << and >> button 
frn=1
def action(n):
    global frn
    r=frn+n
    if r==0 or r==5:
        return 0
    else:
        frn+=n
        f1.pack_forget()
        f2.pack_forget()
        f3.pack_forget()
        f4.pack_forget()
        if(r==1):
            f1.pack()
        if(r==2):
            f2.pack()
        if(r==3):
            f3.pack()
        if(r==4):
            f4.pack()
        
#this is fuction containing the logic for next>> button of page-1 
def action1():
    global frn
    frn+=1
    f1.pack_forget()
    f2.pack()

#this is fuction containing the logic for next>> button of page-2    
def action2():
    global frn
    frn+=1
    e.delete(0,'end')
    if userchoice.get()=="education":
        e.insert('end',"STUDENT NAME,COURSE,")
    if userchoice.get()=="business":
        e.insert('end','Organization name,')
    if userchoice.get()=="housework":
        e.insert('end',"Bill From,Bill Amount,")
    f2.pack_forget()
    f3.pack()

#this is fuction containing the logic for next>> button of page-3   
def action3():
    global frn
    frn+=1
    f3.pack_forget()
    f4.pack()

#this is fuction containing the logic for FINISH button of page-4
def action4():
    global frn
    frn+=1
    pr=e1.get()
    databasen=e2.get()
    try:
        os.mkdir(f"{pr}")
    except FileExistsError:
        messagebox.showerror("Error","Project name is already exist")
        return 0
    try:
        # phase-1 >> in this phase the directory structure is created
        
        
        shutil.copy("project.py",f"{pr}/software.py")
        with open(f'{pr}/pnam.csv','w',newline="") as f:
            csv=DictWriter(f,fieldnames=["Project_Name","Database"])
            csv.writeheader()
            csv.writerow({
                "Project_Name":pr,
                "Database":databasen
            })
        
        # phase-2 >> in this phase the database is created
        r=e.get()
        with open(f'{pr}/entry.csv','w',newline="") as f:
            csv=DictWriter(f,fieldnames=["Entry_Name"])
            csv.writeheader()
            csv.writerow({
            "Entry_Name":r  
            })
        r=r.split(",")
        entry=[]
        for i in r:
            entry.append(i.replace(" ","_"))
        con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
        mycursor=con.cursor()
        mycursor.execute(f"CREATE TABLE {databasen} ({entry[0]} varchar(100))")
        k=0
        for i in entry:
            if k==0:
                k=1
                continue
            mycursor=con.cursor()
            mycursor.execute(f"ALTER TABLE {databasen} ADD COLUMN {i} varchar(100)")
        con.commit()
    
        # phase-3 >> in this phase the data ,given by the user,writes in their respective folder 
        user=ee1.get()
        passw=ee2.get()
        choice=userchoice.get()
        with open(f'{pr}/Pass.csv','w',newline="") as f:
            csw=DictWriter(f,fieldnames=['username','password','choice'])
            csw.writeheader()
            csw.writerow({

                'username':user,
                'password':passw,
                'choice':choice
            })
        if choice == "education":
            with open(f'{pr}/Prem.csv','w',newline="") as g:
                csw=DictWriter(g,fieldnames=['class','fee'])
                csw.writeheader()
                csw.writerows([{'class':'bca','fee':'30000'},{'class':'bba','fee':'28000'},{'class':'b.com','fee':'16000'},{'class':'bsc','fee':'23000'}])
            databasen=e2.get()
            con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
            mycursor=con.cursor()
            mycursor.execute(f"ALTER TABLE {databasen} ADD COLUMN Fee varchar(10)")
        elif choice == "housework":
            with open(f'{pr}/Prem.csv','w',newline="") as g:
                csw=DictWriter(g,fieldnames=['name','amount'])
                csw.writeheader()
                csw.writerow({
                    'name':"budget",
                    'amount':"20000"
                })
            databasen=e2.get()
            con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
            mycursor=con.cursor()
            mycursor.execute(f"ALTER TABLE {databasen} ADD COLUMN Payment_Done varchar(15)")
        con.commit()
        f4.pack_forget()
        f5.pack()
        b1.pack_forget()
        b2.pack_forget()
    
    except mysql.connector.errors.ProgrammingError as err:
        print(err)
        shutil.rmtree(f"E:\{e1.get()}")
        con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
        mycursor=con.cursor()
        mycursor.execute(f"DROP TABLE {databasen} ")
        con.commit()
        messagebox.showerror("Error","Error regarding  database ")
        return 0

    except Exception:
        shutil.rmtree(f"E:\{e1.get()}")
        con=mysql.connector.connect(host="localhost",user="root",password="",database="project")
        mycursor=con.cursor()
        mycursor.execute(f"DROP TABLE {databasen} ")
        con.commit()
        messagebox.showerror("Error","An unknown error has occured ! ")
        return 0
        
        
    
#from here the main() fuction is start
root1=tk.Tk()
root1.title("S.M.A.R.T")
w=root1.winfo_screenwidth()
h=root1.winfo_screenheight()
root1.geometry(f"{w}x{h-50}+0+0")
b1=ttk.Button(root1,text="<<",command=partial(action,-1))
b1.pack(side='left',ipady=10,padx=10,pady=20)
b2=ttk.Button(root1,text=">>",command=partial(action,1))
b2.pack(side='right',ipady=10,padx=10,pady=20)

# A frame on root1 is created that is going to contain the other frames of page-1,page-2....
f=ttk.Frame(root1)
f.pack()
ttk.Label(f,text="WELCOME TO S.M.A.R.T !!!",font="Andalus 24 bold").pack(side="top",anchor="center",pady=20)

# Frame of page-1 is created that contain the component used in page-1 formation  
f1=ttk.Frame(f)
f1.pack()
ttk.Label(f1,text="PAGE-1",font="Andalus 24 bold").grid(row=0,columnspan=5,pady=5)
ttk.Label(f1,text="Enter your Project name").grid(row=1,column=0,sticky=tk.W)
e1=ttk.Entry(f1,width=40)
e1.focus()
e1.grid(row=2,column=0,pady=10)
ttk.Label(f1,text="Enter your Database name ").grid(row=3,column=0,sticky=tk.W)
e2=ttk.Entry(f1,width=40)
e2.grid(row=4,column=0,pady=10)
ttk.Button(f1,text="-SAVE-",command=action1).grid(row=5,column=0,pady=10)


# Frame of page-2 is created that contain the component used in page-2 formation
f2=ttk.Frame(f)
ttk.Label(f2,text="PAGE-2",font="Andalus 24 bold").grid(row=0,columnspan=5,pady=5)
ttk.Label(f2,text="Please Enter your Choice",font="Arial 18").grid(row=1,columnspan=2)
userchoice=tk.StringVar()
ttk.Radiobutton(f2,text="Education",value="education",variable=userchoice).grid(row=2,column=0,pady=10,sticky=tk.W)
ttk.Radiobutton(f2,text="Business",value="business",variable=userchoice).grid(row=3,column=0,pady=10,sticky=tk.W)
ttk.Radiobutton(f2,text="Housework",value="housework",variable=userchoice).grid(row=4,column=0,pady=10,sticky=tk.W)
ttk.Radiobutton(f2,text="Other",value="other",variable=userchoice).grid(row=6,column=0,pady=10,sticky=tk.W)
ttk.Button(f2,text="-SAVE-",command=action2).grid(row=7,columnspan=2)


# Frame of page-3 is created that contain the component used in page-3 formation
f3=ttk.Frame(f)
ttk.Label(f3,text="PAGE-3",font="Andalus 24 bold").grid(row=0,columnspan=5,pady=5)
ttk.Label(f3,text=f"Enter the entry name (Pre-entered entries is required)",font="TimesNewRoman 14 bold").grid(row=1,column=0,pady=20)
ttk.Label(f3,text="ENTRY\'s NAME:(seperate by Comma)",font="Arial 14 italic").grid(row=2,column=0,sticky=tk.W,pady=10)
e=ttk.Entry(f3,width=100)
e.grid(row=3,column=0,pady=10)
ttk.Button(f3,text="-SAVE-",command=action3).grid(row=4,column=0,pady=10)


# Frame of page-4 is created that contain the component used in page-4 formation
f4=ttk.Frame(f)
ttk.Label(f4,text="PAGE-4",font="Andalus 24 bold").grid(row=0,columnspan=5,pady=5)
ttk.Label(f4,text="Enter the username for software.").grid(row=1,column=0,sticky=tk.W)
ee1=ttk.Entry(f4,width=30)
ee1.focus()
ee1.grid(row=2,column=0,sticky=tk.W,pady=10)
ttk.Label(f4,text="Enter the password for software.").grid(row=3,column=0,sticky=tk.W)
ee2=ttk.Entry(f4,width=30)
ee2.grid(row=4,column=0,sticky=tk.W,pady=10)
ttk.Button(f4,text="FINISH",command=action4).grid(row=5,column=0,pady=10)

# A frame of last page is created that shows that the process has been completed and you can see your software after closing the smart program.
f5=ttk.Frame(f)
ttk.Label(f5,text="THANKYOU FOR USING THE S.M.A.R.T PROGRAM !\nPLEASE CONTACT US TO MANAGE PROCESS PHASE.",font="Andalus 20 italic").pack(anchor="center",pady=20)
ttk.Button(f5,text="(: EXIT :)",command=lambda :root1.destroy()).pack(pady=10)
root1.mainloop()

#end of the program