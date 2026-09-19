import mysql.connector
import datetime

def conn():
    try:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Dhamo@123#Db",
            database="project",
            auth_plugin="mysql_native_password"
        )
        if db.is_connected():
            print("database connection successfully:")
    except Exception as e:
        print(f"data base connection error:{str(e)}")
    return db
def deposite(amt):
    amount=100000
    db=conn()
    con=db.cursor()
    con.execute("select accno,pin from amt")
    data=con.fetchall()
    for i in data:
        if(i[0]==719552 and i[1]==2124):
            if(amount>=amt):
                amount-=amt
                print(amount)
            else:
                print("invalid amount")

conn()
print(datetime.datetime.now())
# def join(name,phone):
#     db=conn()
#     con=db.cursor()
#     con.execute("select n.name,n.address,n.phone,n.accno,a.pin from newacc n inner join amt a on n.accno=a.accno where n.name=%s and n.phone=%s",(name,phone))
#     data=con.fetchall()
#     print(data)
#     con.close()
# join("dhamo",9159112466)


# def ret():
#     db=conn()
#     con=db.cursor()
#     sql="select email,password from signup"
#     con.execute(sql)
#     row=con.fetchall()
#     for i in row:
#         print(i)
#         if(i[0]=="dhamo@gmail.com" and i[1]=="123456789"):
#             print("login successfull")
#         else:
#             print("not login")
#     con.close()
#     db.close()
# def user_exits(em):
#     db=conn()
#     con=db.cursor()
#     sql="select email from signup where email=%s"
#     val=(em,)
#     con.execute(sql,val)
#     ema=con.fetchall()
#     for i in ema:
#         if i==em:
#             print("user exists")
#         else:
#             print("not exists")
#     else:
#         print("not exists")
#     con.close()
#     db.close()
# user_exits("dha@gmail.com")
