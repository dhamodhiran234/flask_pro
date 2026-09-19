from flask import Flask,render_template,request,redirect,url_for
from database import conn
from random import randint
from datetime import datetime
app=Flask(__name__)

@app.route("/")
def dash():
    return render_template("dashboard.html")
def user_exits(em):
    db=conn()
    con=db.cursor()
    sql="select email from signup where email=%s"
    val=(em,)
    con.execute(sql,val)
    ema=con.fetchall()
    if(len(ema)==0):
        return True
    return False


@app.route("/sign",methods=["POST","GET"])
def sign():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        phone=request.form.get("phone")
        f=user_exits(email)
        if f:
            db=conn()
            con=db.cursor()
            sql="insert into signup(name,email,password,phone) values(%s,%s,%s,%s)"
            val=(name,email,password,phone)
            print(name,email,password,phone)
            con.execute(sql,val)
            db.commit()
            con.close()
            db.close()
            return redirect(url_for("log"))
        else:
            print("sign up page ::::  user already exists")
            return render_template("sign.html",error="USER ALREADY EXISTS PLEASE LOGIN")
    return render_template("sign.html")

@app.route("/log",methods=["POST","GET"])
def log():
    if (request.method=="POST"):
        email=request.form.get("email")
        password=request.form.get("password")
        db=conn()
        con=db.cursor()
        sql="select email,password from signup"
        con.execute(sql)
        data=con.fetchall()
        for i in data:
            if(i[0]==email):
                if( i[1]==password):
                    print("log in page  :::  success")
                    return redirect(url_for("home"))
        else:
            return render_template("log.html",error="NO USER EXISTS PLEASE SIGNUP FIRST")
    return render_template("log.html")
@app.route("/home",methods=["POST","GET"])
def home():
    return render_template("bank.html")


def used_ag(ph):
    db=conn()
    con=db.cursor()
    con.execute("select phone from newacc where phone=%s",(ph,))
    data=con.fetchall()
    le=len(data)
    return le==0


@app.route("/newaccount",methods=["POST","GET"])
def createaccount():
    if request.method=="POST":
            name=request.form.get("name").strip()
            add=request.form.get("address").strip()
            phone=request.form.get("phone").strip()
            amount=request.form.get("amt").strip()
            accno=randint(100000,999999)
            pin=randint(1000,9999)
            db=conn()
            con=db.cursor()
            if used_ag(phone):
                sql="insert into amt(accno,pin,amount) values(%s,%s,%s)"
                val=(accno,pin,amount)
                con.execute(sql,val)
                db.commit()
                con.close()
                db.close()
                db=conn()
                con=db.cursor()
                sql="insert into newacc(name,address,phone,accno) values(%s,%s,%s,%s)"
                val=(name,add,phone,accno)            
                con.execute(sql,val)
                db.commit()
                con.close()
                db.close()
                db=conn()
                con=db.cursor()
                sql="insert into hist(name,histy,datetime) values(%s,%s,%s)"
                histy="account created"
                dt=datetime.now()
                val=(name,histy,dt)            
                con.execute(sql,val)
                db.commit()
                con.close()
                db.close()
                return render_template("bank.html",success=f"account create successfully and then show accountnumber and pin is click accountdetails and enter your name with phone number")
            else:
                return render_template("bank.html",error="account already exits in phone number please try again")

@app.route("/withdraw",methods=["POST","GET"])
def withdraw():
    if request.method=="POST":
        accn=request.form.get("acc")
        pin=request.form.get("pin")
        amts=int(request.form.get("amt"))
        db=conn()
        con=db.cursor()
        con.execute("select amount from amt where accno=%s and pin=%s",(accn,pin))
        data=con.fetchall()
        con.close()
        db.close()
        for i in data:
            if amts<=i[0] and amts>=0:
                balance=i[0]
                new_bal=balance-amts
                print(new_bal,"new balance")
                print(balance,"old balance")
                print(amts,"put amount")
                db=conn()
                con=db.cursor()
                con.execute("update amt set amount=%s where accno=%s",(new_bal,accn))
                db.commit()
                con.close()
                db.close()
                db=conn()
                con=db.cursor()
                con.execute("select name from newacc where accno=%s",(accn,))
                data=con.fetchall()
                for i in data:
                    name=i[0]
                    db=conn()
                    con=db.cursor()
                    sql="insert into hist(name,histy,datetime) values(%s,%s,%s)"
                    histy=f"amount widthdraw:{amts}"
                    dt=datetime.now()
                    val=(name,histy,dt)            
                    con.execute(sql,val)
                    db.commit()
                    con.close()
                    db.close()

                con.close()
                db.close()
                
                return render_template("bank.html",success="withdraw amount successfully")
            else:
                return render_template("bank.html",error="insuffucient amount entered")
        else:
            return render_template("bank.html",error="account and pin number is invalid")
@app.route("/deposite",methods=["POST","GET"])
def deposite():
    if request.method=="POST":
        accn=request.form.get("acc")
        pin=request.form.get("pin")
        amts=int(request.form.get("amt"))
        db=conn()
        con=db.cursor()
        con.execute("select amount from amt where accno=%s and pin=%s",(accn,pin))
        data=con.fetchall()
        con.close()
        db.close()
        for i in data:
            if amts>=0:
                balance=i[0]
                new_bal=balance+amts
                print(new_bal,"new balance")
                print(balance,"old balance")
                print(amts,"put amount")
                db=conn()
                con=db.cursor()
                con.execute("update amt set amount=%s where accno=%s",(new_bal,accn))
                db.commit()
                con.close()
                db.close()
                db=conn()
                con=db.cursor()
                con.execute("select name from newacc where accno=%s",(accn,))
                data=con.fetchall()
                for i in data:
                    name=i[0]
                    db=conn()
                    con=db.cursor()
                    sql="insert into hist(name,histy,datetime) values(%s,%s,%s)"
                    histy=f"amount deposite:{amts}"
                    dt=datetime.now()
                    val=(name,histy,dt)            
                    con.execute(sql,val)
                    db.commit()
                    con.close()
                    db.close()
                return render_template("bank.html",success="deposite amount successfully")
            else:
                return render_template("bank.html",error="insuffucient amount entered")
        else:
            return render_template("bank.html",error="account and pin number is invalid")


@app.route("/balance",methods=["POST","GET"])
def balance():
    if request.method=="POST":
        accn=request.form.get("acc")
        pin=request.form.get("pin")
        db=conn()
        con=db.cursor()
        con.execute("select amount from amt where accno=%s and pin=%s",(accn,pin))
        data=con.fetchall()
        con.close()
        db.close()
        for i in data:
            balance=i[0]
            print(balance,"amount balance")
            db=conn()
            con=db.cursor()
            con.execute("select name from newacc where accno=%s",(accn,))
            data=con.fetchall()
            for i in data:
                name=i[0]
                db=conn()
                con=db.cursor()
                sql="insert into hist(name,histy,datetime) values(%s,%s,%s)"
                histy=f"check balance"
                dt=datetime.now()
                val=(name,histy,dt)            
                con.execute(sql,val)
                db.commit()
                con.close()
                db.close()
            return render_template("bank.html",success=f"balance amount={balance}")
        else:
            return render_template("bank.html",error="account and pin number is invalid")


@app.route("/accdet",methods=["POST","GET"])
def accountdetails():
    if request.method=="POST":
        name=request.form.get("name")
        phone=request.form.get("phone")
        db=conn()
        con=db.cursor()
        con.execute("select n.name,n.address,n.phone,n.accno,a.pin from newacc n inner join amt a on n.accno=a.accno where name=%s and phone=%s",(name,phone))
        data=con.fetchall()
        print(data)
        con.close()
        db.close()
        if len(data)!=0:
            db=conn()
            con=db.cursor()
            sql="insert into hist(name,histy,datetime) values(%s,%s,%s)"
            histy="account details view"
            dt=datetime.now()
            val=(name,histy,dt)            
            con.execute(sql,val)
            db.commit()
            con.close()
            db.close()
            return render_template("showdetails.html",dataset=data)
        else:
            return render_template("bank.html",error="name and phone number is invalid")
@app.route("/history",methods={"POST","GET"})
def history():
    db=conn()
    con=db.cursor()
    con.execute("select name,histy,datetime from hist")
    data=con.fetchall()
    print(data)
    con.close()
    db.close()
    if len(data)!=0:
        return render_template("histy.html",dataset=data)
    else:
        return render_template("bank.html",error="no histaory found")
if(__name__=="__main__"):
    app.run(debug=True)
