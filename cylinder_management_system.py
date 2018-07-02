#!/usr/bin/python
import Tkinter
from Tkinter import *
import inspect
import socket
import sys
import time
import serial
import os
import os.path
import re   
import MySQLdb
import datetime 
import csv

gui=Tk()
frame=Frame(gui,bg="green")
frame.pack()


def create_table_consumer():
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    sql = """CREATE TABLE consumer (
            consumer_name CHAR(20) NOT NULL,
            cylinder_no  INT,
            date_issue  DATETIME,
            date_deposited  DATETIME,
            price_per_day  INT,
            days_expemted  INT,
            cylinder_status  INT,
            last_bill_due  INT,
            net_amount  INT,
            amount_paid  INT,
            security_deposite  INT,
            date_payment DATETIME ,
            cylinder_type INT)"""
    cursor.execute(sql)
    db.close()




def insert_into_table_consumer(cylinder_no,consumer_Name):
    data = []
    time_now = datetime.datetime.now()
    time_format = time_now.strptime(str(time_now)[:19], '%Y-%m-%d %H:%M:%S')
    data.insert(0,consumer_Name)
    data.insert(1,int(float(cylinder_no)))
    data.insert(2,time_format) #date_issue_entry
    data.insert(3,time_format)   # not needed
    data.insert(4,int(float(issue_price_per_day_entry.get())))
    data.insert(5,0)
    data.insert(6,2)
    data.insert(7,0)
    data.insert(8,0)
    data.insert(9,0)
    data.insert(10,int(float(issue_security_deposit_entry.get())))
    data.insert(11,time_format)   
    data.insert(12,int(float(issue_cylinder_type_entry.get())))
    print data 
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    sql = """INSERT INTO consumer(consumer_name,cylinder_no, date_issue, date_deposited, price_per_day,days_expemted,cylinder_status,last_bill_due,net_amount,amount_paid,security_deposite,date_payment,cylinder_type)
    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')""".format(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12])
    print sql
    try:
       cursor.execute(sql)
       print "1"
       db.commit()
    except:
       print "2"
       db.rollback()
    db.close()



def update_table_consumer(params, cylinder_no, c_typ):
    time_now = datetime.datetime.now()
    time_format = time_now.strptime(str(time_now)[:19], '%Y-%m-%d %H:%M:%S')
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    if params == "deposite": 
        expemted = 2  #days_expemted_entry.get()
        sql = "UPDATE consumer SET date_deposited = '{0}', cylinder_status = {1},days_expemted = {2}  WHERE  cylinder_no = {3} and cylinder_type = {4}".format(time_format,3,expemted,cylinder_no, 1 )
        
        print sql
    
    if params == "generate_bill": 
        # last_bill_due,net_amount,amount_paid   date_deposited_entry.get()
        sql = "UPDATE consumer SET status = 3 WHERE  cylinder_no = cylinder_no  "
    try:
       cursor.execute(sql)
       db.commit()
       print "pass"
    except:
       db.rollback()
    db.close()



def create_table_cylinder():
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    sql = """CREATE TABLE CylinderInfoTable (
            -- id  INT,
            cylinder_no  INT,
            consumer_name CHAR(20) NOT NULL,
            date_issue  DATETIME,
            date_depos  DATETIME,
            status INT,
            cylinder_type CHAR(3))"""
    cursor.execute(sql)
    db.close()


def insert_into_table_cylinder(cylinder_no,cyl_typ):   
    data = []
    time_now = datetime.datetime.now()
    time_format = time_now.strptime(str(time_now)[:19], '%Y-%m-%d %H:%M:%S') 
    Cylinder_no   =    cylinder_no
    consumer_name =    'none'            
    # date_issue    =   null
    # date_depos    =   null
    status        =   1
    Cylinder_type =   cyl_typ
    data.insert(0,Cylinder_no)
    data.insert(1,consumer_name)
    data.insert(2,time_format)
    data.insert(3,time_format)
    data.insert(4,status)
    data.insert(5,Cylinder_type)
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    sql = """INSERT INTO CylinderInfoTable(cylinder_no,consumer_name, date_issue, date_depos, status,cylinder_type) 
    values('{0}','{1}','{2}','{3}','{4}','{5}')""".format(data[0],data[1],data[2],data[3],data[4],data[5])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()




def update_table_cylinder(param,Cylinder_no,consumer_name):
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    if param == "issue" : 
        sql = "UPDATE CylinderInfoTable SET status = 2 WHERE  cylinder_no = {0} and cylinder_type = {1}".format(Cylinder_no, 1 ) # and cylinder_type = type
        print sql
    elif param == "deposite" : 
        sql = "UPDATE CylinderInfoTable SET status = 3 WHERE  cylinder_no = {0} and cylinder_type = {1}".format(Cylinder_no, 1 ) # and cylinder_type = type
    elif param == "export" : 
        sql = "UPDATE CylinderInfoTable SET status = 4 WHERE  cylinder_no = {0} and cylinder_type = {1}".format(Cylinder_no, 1 ) # and cylinder_type = type
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def fetch(sql_command,name,typ):
    # print sql_command
    db = MySQLdb.connect("localhost","root","root","cylinder_management_system" )
    cursor = db.cursor()
    sql = str(sql_command)
    cursor.execute(sql)
    response = cursor.fetchall()       
    db.close()
    print response
    # generate_csv(response ,name,typ )

# def generate_csv(data,name,typ):
#     time_now = datetime.datetime.now()
#     time_format = time_now.strptime(str(time_now)[:19], '%Y-%m-%d %H:%M:%S')
#     file_name = name + str(time_format)
#     populate = [data]
#     with open(file_name, 'w', newline='') as csvfile:
#         spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         if typ == 'consumerwise':
#             spamwriter.writerow(['consumer_name','cylinder_no','date_issue','date_deposited','price_per_day','days_expemted','cylinder_status','last_bill_due','net_amount','amount_paid','security_deposite','date_payment','cylinder_type'])
#         elif typ == 'cylinderwise':
#             spamwriter.writerow(['cylinder_no','consumer_name','date_issue','date_depos','status','cylinder_type'])    
#         spamwriter.writerow(populate)


def factory_import():
    import_no = import_cylinder_no_entry.get()
    import_type = import_cylinder_type_entry.get()
    insert_into_table_cylinder(import_no,import_type)



def issue():
    cylinder_no = issue_cylinder_no_entry.get()
    consumer_Name = issue_consumer_name_entry.get()
    insert_into_table_consumer(cylinder_no,consumer_Name);
    update_table_cylinder('issue',cylinder_no,consumer_Name)
    



def deposite():
    cylinder_no = cylinder_no_entry.get()    
    c_typ = cylinder_type_entry.get()    
    # days_expemted =  days_expemted_entry.get()
    update_table_cylinder("deposite",cylinder_no,'none')
    update_table_consumer("deposite",cylinder_no, c_typ)

def factory_export():
    cylinder_no = export_cylinder_no_entry.get()
    update_table_cylinder('export',cylinder_no,'none')
    




def search_consumerwise():
    name = track_consumer_entry.get()
    typ = track_consumer_cylinder_type_entry.get()
    sql_query = "select * from consumer where consumer_name = '" + str(name) + "' and cylinder_type = " + typ
    fetch(sql_query,name, 'consumerwise')
    # result_entry.delete(0,END)
    # result_entry.insert(INSERT,str(msg.payload))
    pass

def search_cylinderwise():
    number = track_cylinder_no_entry.get()
    typ_cyl = track_cylinder_type_entry.get()
    sql_query = "select * from CylinderInfoTable where cylinder_no = " + number + " and cylinder_type = " + typ_cyl
    fetch(sql_query,number,'cylinderwise' )
    # result_entry.delete(0,END)
    # result_entry.insert(INSERT,str(msg.payload))
    pass

def generate_bill(consumer_name):
    pass

gui.title('cylinder management system ')

import_label=Label(frame,text="factory import",bg="green",fg="black")
import_label.grid(row=4,column=1,sticky=NS)

import_cylinder_no_label=Label(frame,text="cylinder_no",bg="green",fg="black")
import_cylinder_no_label.grid(row=5,column=0,sticky=W)
import_cylinder_no_entry=Entry(frame)
import_cylinder_no_entry.grid(row=5,column=1,sticky=W)

import_cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
import_cylinder_type_label.grid(row=6,column=0,sticky=W)
import_cylinder_type_entry=Entry(frame)
import_cylinder_type_entry.grid(row=6,column=1,sticky=W)

import_Button =Button(frame, text="import", command=factory_import,bg="green",fg="black")
import_Button.grid(row=8,column=1, sticky='NS')
################################################################################

export_label=Label(frame,text="factory export",bg="green",fg="black")
export_label.grid(row=4,column=4,sticky=NS)


export_cylinder_no_label=Label(frame,text="cylinder_no",bg="green",fg="black")
export_cylinder_no_label.grid(row=5,column=3,sticky=W)
export_cylinder_no_entry=Entry(frame)
export_cylinder_no_entry.grid(row=5,column=4,sticky=W)

export_cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
export_cylinder_type_label.grid(row=6,column=3,sticky=W)
export_cylinder_type_entry=Entry(frame)
export_cylinder_type_entry.grid(row=6,column=4,sticky=W)

export_Button =Button(frame, text="export", command=factory_export,bg="green",fg="black")
export_Button.grid(row=8,column=4, sticky='NS')



########################################################################

track_label=Label(frame,text="track cylinder",bg="green",fg="black")
track_label.grid(row=4,column=7,sticky=NS)

track_cylinder_no_label=Label(frame,text="cylinder_no",bg="green",fg="black")
track_cylinder_no_label.grid(row=5,column=6,sticky=E)
track_cylinder_no_entry=Entry(frame)
track_cylinder_no_entry.grid(row=5,column=7,sticky=W)

track_cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
track_cylinder_type_label.grid(row=6,column=6,sticky=E)
track_cylinder_type_entry=Entry(frame)
track_cylinder_type_entry.grid(row=6,column=7,sticky=W)

track_Button =Button(frame, text="track", command=search_cylinderwise,bg="green",fg="black")
track_Button.grid(row=8,column=7, sticky='NS')
################################################################################

export_label=Label(frame,text="consumer active cylinders",bg="green",fg="black")
export_label.grid(row=4,column=10,sticky=NS)

track_consumer_label=Label(frame,text="consumer name",bg="green",fg="black")
track_consumer_label.grid(row=5,column=9,sticky=E)
track_consumer_entry=Entry(frame)
track_consumer_entry.grid(row=5,column=10,sticky=E)

track_consumer_cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
track_consumer_cylinder_type_label.grid(row=6,column=9,sticky=E)
track_consumer_cylinder_type_entry=Entry(frame)
track_consumer_cylinder_type_entry.grid(row=6,column=10,sticky=E)

export_Button =Button(frame, text="get consumer wise", command=search_consumerwise,bg="green",fg="black")
export_Button.grid(row=8,column=10, sticky='NS')

##############################################################
# space_label=Label(frame,text="  ",bg="green",fg="green")
# space_label.grid(row=9,column=10,sticky=NS)


# result_entry=Entry(frame)
# result_entry.grid(row=10,column=9,sticky= N )
# # result_entry.pack()
# result_entry.insert(INSERT,"    searched results")

# self.result_entry.delete(0,END)
# self.result_entry.insert(INSERT,str(msg.payload))

#########################################################################
space_label=Label(frame,text="  ",bg="green",fg="green")
space_label.grid(row=15,column=10,sticky=NS)

space_label=Label(frame,text="  ",bg="green",fg="green")
space_label.grid(row=17,column=10,sticky=NS)


###################################################
_label=Label(frame,text="issue cylinder",bg="green",fg="black")
_label.grid(row=20,column=1,sticky=NS)

issue_consumer_name_label=Label(frame,text="consumer_name",bg="green",fg="black")
issue_consumer_name_label.grid(row=22,sticky=W)
issue_consumer_name_entry=Entry(frame)
issue_consumer_name_entry.grid(row=22,column=1,sticky=W)

issue_cylinder_no_label=Label(frame,text="cylinder_no",bg="green",fg="black")
issue_cylinder_no_label.grid(row=23,sticky=W)
issue_cylinder_no_entry=Entry(frame)
issue_cylinder_no_entry.grid(row=23,column=1,sticky=W)

# issue_date_issue_label=Label(frame,text="date_issue",bg="green",fg="black")
# issue_date_issue_label.grid(row=24,sticky=W)
# issue_date_issue_entry=Entry(frame)
# issue_date_issue_entry.grid(row=24,column=1,sticky=W)


issue_price_per_day_label=Label(frame,text="price_per_day",bg="green",fg="black")
issue_price_per_day_label.grid(row=25,sticky=W)
issue_price_per_day_entry=Entry(frame)
issue_price_per_day_entry.grid(row=25,column=1,sticky=W)



issue_security_deposit_label=Label(frame,text="security_deposit",bg="green",fg="black")
issue_security_deposit_label.grid(row=26,sticky=W)
issue_security_deposit_entry=Entry(frame)
issue_security_deposit_entry.grid(row=26,column=1,sticky=W)


issue_cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
issue_cylinder_type_label.grid(row=27,sticky=W)
issue_cylinder_type_entry=Entry(frame)
issue_cylinder_type_entry.grid(row=27,column=1,sticky=W)

issue_Button =Button(frame, text="issue", command=issue,bg="green",fg="black")
issue_Button.grid(row=32,column=1, sticky='NS')

###########################################################################

_label=Label(frame,text="deposite issued cylinder",bg="green",fg="black")
_label.grid(row=15,column=6,sticky=NS)


cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
cylinder_type_label.grid(row=22,column=5,sticky=W)
cylinder_type_entry=Entry(frame)
cylinder_type_entry.grid(row=22,column=6,sticky=W)

cylinder_no_label=Label(frame,text="cylinder_no",bg="green",fg="black")
cylinder_no_label.grid(row=23,column=5,sticky=W)
cylinder_no_entry=Entry(frame)
cylinder_no_entry.grid(row=23,column=6,sticky=W)

# date_deposited_label=Label(frame,text="date_deposited",bg="green",fg="black")
# date_deposited_label.grid(row=24,column=5,sticky=W)
# date_deposited_entry=Entry(frame)
# date_deposited_entry.grid(row=24,column=6,sticky=W)

# days_expemted_label=Label(frame,text="days_expemted",bg="green",fg="black")
# days_expemted_label.grid(row=25,column=5,sticky=W)
# days_expemted_entry=Entry(frame)
# days_expemted_entry.grid(row=25,column=6,sticky=W)

issue_Button =Button(frame, text="deposite", command=deposite,bg="green",fg="black")
issue_Button.grid(row=32,column=6, sticky='NS')

############################################################

# _label=Label(frame,text="generate bill",bg="green",fg="black")
# _label.grid(row=15,column=10,sticky=NS)

# consumer_name_label=Label(frame,text="consumer_name",bg="green",fg="black")
# consumer_name_label.grid(row=22,column=9,sticky=W)
# consumer_name_entry=Entry(frame)
# consumer_name_entry.grid(row=22,column=10,sticky=W)

# cylinder_no_label=Label(frame,text="cylinder_no",bg="green",fg="black")
# cylinder_no_label.grid(row=23,column=9,sticky=W)
# cylinder_no_entry=Entry(frame)
# cylinder_no_entry.grid(row=23,column=10,sticky=W)



# date_deposited_label=Label(frame,text="date_deposited",bg="green",fg="black")
# date_deposited_label.grid(row=24,column=9,sticky=W)
# date_deposited_entry=Entry(frame)
# date_deposited_entry.grid(row=24,column=10,sticky=W)




# days_expemted_label=Label(frame,text="days_expemted",bg="green",fg="black")
# days_expemted_label.grid(row=25,column=9,sticky=W)
# days_expemted_entry=Entry(frame)
# days_expemted_entry.grid(row=25,column=10,sticky=W)



# last_bill_due_label=Label(frame,text="last_bill_due",bg="green",fg="black")
# last_bill_due_label.grid(row=26,column=9,sticky=W)
# last_bill_due_entry=Entry(frame)
# last_bill_due_entry.grid(row=26,column=10,sticky=W)

# net_amount_label=Label(frame,text="net_amount",bg="green",fg="black")
# net_amount_label.grid(row=27,column=9,sticky=W)
# net_amount_entry=Entry(frame)
# net_amount_entry.grid(row=27,column=10,sticky=W)

# amount_paid_label=Label(frame,text="amount_paid",bg="green",fg="black")
# amount_paid_label.grid(row=28,column=9,sticky=W)
# amount_paid_entry=Entry(frame)
# amount_paid_entry.grid(row=28,column=10,sticky=W)

# payment_date_label=Label(frame,text="payment_date",bg="green",fg="black")
# payment_date_label.grid(row=29,column=9,sticky=W)
# payment_date_entry=Entry(frame)
# payment_date_entry.grid(row=29,column=10,sticky=W)

# cylinder_type_label=Label(frame,text="cylinder_type",bg="green",fg="black")
# cylinder_type_label.grid(row=30,column=9,sticky=W)
# cylinder_type_entry=Entry(frame)
# cylinder_type_entry.grid(row=30,column=10,sticky=W)

# space_label=Label(frame,text="  ",bg="green",fg="green")
# space_label.grid(row=31,column=10,sticky=NS)

# issue_Button =Button(frame, text="generate bill", command=generate_bill,bg="green",fg="black")
# issue_Button.grid(row=32,column=10, sticky='NS')

gui.mainloop()
