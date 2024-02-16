import mysql.connector
import random
import smtplib
from email.message import EmailMessage
import pywhatkit as p
mydb=mysql.connector.connect(host="localhost",user="banking",passwd="bank123",database="bank")
def recall():
    print("1. MAIN","2. EXIT", sep='\n')
    print()
    c=input("ENTER YOUR CHOICE :")
    if(c=='1'):
        main()
    elif(c=='2'):
        print()
        print("***** THANK YOU *****")
        print("***** HAVE A NICE DAY *****")
    else:
        print()
        print("** WRONG CHOICE **")
        print()
        recall()
def email_sender(to,subject,body):
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']= subject
    msg['to'] = f"{to}"
    user="publica022@gmail.com "
    msg['from']=user
    password="ghlchhjgzypuiwag"
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
def whatsapp_sender(bod,t):
    p.sendwhatmsg_instantly(f"+91{t}", bod,15,True,5)
def otp_verifier(z,em):
    x=0
    while (x==0):
        print(f"VERIFY YOUR {z}")
        otp= random.randint(100000, 999999)
        if(z=="EMAIL ID"):
            email_sender(em,"GLOBAL BANK OTP",f"YOUR OTP FOR NEW ACCOUNT OPENNING IS {otp}")
        else:
            whatsapp_sender(f"YOUR OTP FOR NEW ACCOUNT OPENNING IN GLOBAL BANK IS {otp}",em)
        otp_check= int(input(f"ENTER THE OTP SENT TO THE GIVEN {z}: "))
        if (otp_check==otp):
            return(1)
            break
        else:
            print("WRONG OTP")
            print("1.RETRY","2. MAIN","3. EXIT", sep='\n')
            c=input("ENTER YOUR CHOICE :")
            if(c=='1'):
                continue
            elif(c=='2'):
                main()
            elif(c=='3'):
                print()
                print("***** THANK YOU *****")
                print("***** HAVE A NICE DAY *****")
                return(2)
            else:
                print()
                print("** WRONG CHOICE **")
                print()
                continue
def openaccount():
    print()
    print("** OPEN NEW ACCOUNT **")
    print()
    na=input("ENTER NAME :")
    ac=random.randint(10000000000, 99999999999)
    ci=random.randint(1000000, 9999999)
    db = input("ENTER DATE OF BIRTH: ")
    ad = input("ENTER ADDRESS: ")
    p = input("ENTER PHONE NUMBER: ")
    y=otp_verifier("PHONE NUMBER",p)
    if(y==1):
        e = input("ENTER YOUR EMAIL ID: ")
        z=otp_verifier("EMAIL ID",e)
        if(z==1):
            pw = input("ENETR A STRONG PASSWORD: ")
            ob = input("ENTER OPENING BALANCE: ")
            data1 = (na,ac,ci,db,ad,p,e,pw,ob)
            data2 = (ac,na,ob)
            sql1 = 'insert into account values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql2 = 'insert into amount values(%s,%s,%s,0,0)'
            n=mydb.cursor()
            n.execute(sql1,data1)
            n.execute(sql2,data2)
            mydb.commit()
            email_sender(e,"GLOBAL BANK",f"  YOUR ACCOUNT NUMBER IS {ac} AND CUSTOMER ID IS {ci}")
            whatsapp_sender(f"  YOUR ACCOUNT NUMBER IS {ac} AND CUSTOMER ID IS {ci}",p)
            print()
            print("** YOUR ACCOUNT IS OPENED **")
            print(f"  YOUR ACCOUNT NUMBER IS {ac} AND CUSTOMER ID IS {ci}")
            print()
            recall()
        else:
            print("")
    else:
        print("")
def deposit():
    print()
    print("** DEPOSIT MONEY **")
    print()
    ac = int(input("ENTER ACCOUNT NUMBER :"))
    n=mydb.cursor()
    n.execute("select balance from amount where account_number=%s"%(ac))
    b=n.fetchall()
    if len(b)==0:
        print("** THERE IS NOT ANY ACCOUNT WITH THIS ACCOUNT NUMBER IN OUR BANK **")
        print()
        recall()
    else:
        am = int(input("ENTER AMOUNT :"))
        n.execute("select balance from amount where account_number=%s"%(ac))
        c=n.fetchone()
        ta=c[0] + am
        n.execute("update amount set balance=%s where account_number=%s",(ta,ac))
        n.execute("insert into dep values(%s,%s)"%(ac,am))
        mydb.commit()
        print()
        print("** YOUR GLOBAL BANK ACCOUNT ",ac," IS CREDITED BY RUPEES ",am," **")
        print()
        recall()
def withdraw():
    print()
    print("** WITHDRAW MONEY **")
    print()
    ac = int(input("ENTER ACCOUNT NUMBER :"))
    n=mydb.cursor()
    n.execute("select balance from amount where account_number=%s"%(ac))
    a=n.fetchall()
    if len(a)==0:
        print("** THERE IS NOT ANY ACCOUNT WITH THIS ACCOUNT NUMBER IN OUR BANK **")
        print()
        recall()
    else:
        am = int(input("ENTER AMOUNT :"))
        n.execute("select balance from amount where account_number=%s",(ac,))
        b=n.fetchone()
        ta=b[0]
        if am<=ta:
            tb=b[0]-am
            n.execute("update amount set balance=%s where account_number=%s",(tb,ac))
            n.execute("insert into withd values(%s,%s)"%(ac,am))
            mydb.commit()
            print()
            print("** YOUR GLOBAL BANK ACCOUNT ",ac," IS DEBITED BY RUPEES ",am," **")
            print()
            recall()
        else:
            print("Insufficient balance")
            print()
            recall()
def balance():
    print()
    print("** BALANCE ENQUIRY **")
    print()
    ac = int(input("ENTER ACCOUNT NUMBER :"))
    n=mydb.cursor()
    n.execute("select balance from amount where account_number=%s"%(ac))
    a=n.fetchall()
    if len(a)==0:
        print("There is not any account with this account number in our bank")
        recall()
    else:
        n.execute("select * from amount where account_number=%s",(ac,))
        b=n.fetchone()
        print()
        print(" BALANCE = ",b[2])
        print(" LOAN GIVEN = ",b[4])
        print(" LOAN TAKEN = ",b[3])
        print()
        recall()
def details():
    print()
    print("** COUSTOMER DETAILS **")
    print()
    ac = int(input("ENTER ACCOUNT NUMBER :"))
    n=mydb.cursor()
    n.execute("select balance from amount where account_number=%s"%(ac))
    a=n.fetchall()
    if len(a)==0:
        print("** THERE IS NOT ANY ACCOUNT WITH THIS ACCOUNT NUMBER IN OUR BANK **")
        recall()
    else:
        n.execute("select * from account where account_number=%s",(ac,))
        b=n.fetchone()
        print()
        print("NAME :",b[0])
        print("ACCOUNT NUMBER :",b[1])
        print("DATE OF BIRTH :",b[2])
        print("ADDRESS :",b[3])
        print("PHONE NUMBER :",b[4])
        print("OPENNING BALANCE :",b[5])
        print()
        recall()
def close():
    print()
    print("** CLOSE ACCOUNT **")
    print()
    ac = int(input("ENTER ACCOUNT NUMBER :"))
    a= "delete from account where account_number=%s"
    b= "delete from amount where account_number=%s"
    d= (ac,)
    n=mydb.cursor()
    n.execute("select balance from amount where account_number=%s"%(ac))
    x=n.fetchall()
    if len(x)==0:
        print("** THERE IS NOT ANY ACCOUNT WITH THIS ACCOUNT NUMBER IN OUR BANK **")
        print()
        recall()
    else:
        n.execute(a,d)
        n.execute(b,d)
        mydb.commit()
        print()
        print("** YOUR ACCOUNT IS CLOSED **")
        print()
        recall()
def loan():
    print()
    print("** GIVE AND TAKE LOAN **")
    print()
    print("1. GIVE LOAN","2. ADD INTEREST","3. PAY LOAN","4. LOAN DETAILS", sep='\n')
    c=input("ENTER YOUR CHOICE :")
    if(c=='1'):
        g=int(input("ENTER ACCOUNT NUMBER FROM WHICH YOU WANT TO GIVE LOAN :"))
        t=int(input("ENTER ACCOUNT NUMBER TO WHICH YOU WANT TO GIVE LOAN :"))
        n=mydb.cursor()
        n.execute("select balance from amount where account_number=%s"%(g))
        a=n.fetchall()
        if len(a)==0:
            print("** THERE IS NOT ANY ACCOUNT WITH THe ACCOUNT NUMBER YOU ENTERED FOR GIVING LOAN IN OUR BANK **")
            print()
            recall()
        else:
            n.execute("select balance from amount where account_number=%s"%(t))
            a=n.fetchall()
            if len(a)==0:
                print("** THERE IS NOT ANY ACCOUNT WITH THe ACCOUNT NUMBER YOU ENTERED FOR TAKING LOAN IN OUR BANK **")
                print()
                recall()
            else:
                am=int(input("ENTER AMOUNT :"))
                n.execute("select balance from amount where account_number=%s"%(g))
                b=n.fetchone()
                q=b[0]
                p=q-am
                if am<=q:
                    i=int(input("ENTER INTEREST RATE :"))
                    n.execute("update amount set balance=%s where account_number=%s",(p,g))
                    n.execute("select sum from loan where g_ac=%s and t_ac=%s"%(g,t))
                    x=n.fetchall()
                    if len(x)==0:
                        n.execute("insert into loan values(%s,%s,%s,%s)"%(g,t,i,am))
                        n.execute("select balance from amount where account_number=%s"%(t))
                        v=n.fetchone()
                        f=v[0]+am
                        n.execute("update amount set balance=%s where account_number=%s"%(f,t))
                        n.execute("update amount set loan_taken=%s where account_number=%s"%(am,t))
                        n.execute("update amount set loan_given=%s where account_number=%s"%(am,g))
                        print("** YOU GIVE RUPEES ",am," LOAN FROM ACCOUNT ",g," TO ACCOUNT ",t," **")
                        mydb.commit()
                        recall()
                    else:
                        print("nitish")
                        n.execute("select loan_given from amount where account_number=%s"%(g))
                        e=n.fetchone()
                        f=e[0]+am
                        n.execute("update amount set loan_given=%s where account_number=%s",(f,g))
                        n.execute("select loan_taken from amount where account_number=%s"%(t))
                        v=n.fetchone()
                        l=v[0]+am
                        n.execute("update amount set loan_taken=%s where account_number=%s",(l,t))
                        n.execute("select sum from loan where g_ac=%s and t_ac=%s"%(g,t))
                        s=n.fetchone()
                        q=s[0]+am
                        n.execute("update loan set sum=%s where g_ac=%s and t_ac=%s"%(q,g,t))
                        n.execute("update loan set interest=%s where g_ac=%s and t_ac=%s"%(i,g,t))
                        n.execute("insert into loant values(%s,%s,%s,%s)"%(g,t,i,am))
                        n.execute("select balance from amount where account_number=%s"%(t))
                        d=n.fetchone()
                        j=d[0]+am
                        n.execute("update amount set balance=%s where account_number=%s"%(j,t))
                        mydb.commit()
                        print()
                        print("** YOU GIVE RUPEES ",am," LOAN FROM ACCOUNT ",g," TO ACCOUNT ",t," **")
                        print()
                        recall()
                else:
                    print("** INSUFFICIENT BALANCE **")
                    print()
                    recall()
    elif(c=='3'):
        print()
        print("** PAY LOAN **")
        print()
        g=input("ENTER ACCOUNT NUMBER FROM WHICH LOAN IS GIVEN :")
        t=input("ENTER ACCOUNT NUMBER WHICH HAVE TO PAY LOAN :")
        n=mydb.cursor()
        n.execute("select balance from amount where account_number=%s"%(g))
        a=n.fetchall()
        if len(a)==0:
            print("** THERE IS NOT ANY ACCOUNT WITH THe ACCOUNT NUMBER YOU ENTERED FOR GIVING LOAN IN OUR BANK **")
            print()
            recall()
        else:
            n.execute("select balance from amount where account_number=%s"%(t))
            a=n.fetchall()
            if len(a)==0:
                print("** THERE IS NOT ANY ACCOUNT WITH THe ACCOUNT NUMBER YOU ENTERED FOR TAKING LOAN IN OUR BANK **")
                print()
                recall()
            else:
                am=int(input("ENTER AMOUNT TO BE PAID :"))
                n.execute("select balance from amount where account_number=%s"%(t))
                b=n.fetchone()
                ta=b[0]
                if am<=ta:
                    tb=b[0]-am
                    n.execute("update amount set balance=%s where account_number=%s",(tb,t))
                    n.execute("select loan_given from amount where account_number=%s"%(g))
                    b2=n.fetchone()
                    tb2=b2[0]-am
                    n.execute("update amount set loan_given=%s where account_number=%s",(tb2,g))
                    n.execute("select loan_taken from amount where account_number=%s"%(t))
                    b3=n.fetchone()
                    tb3=b3[0]-am
                    n.execute("update amount set loan_taken=%s where account_number=%s",(tb3,t))
                    n.execute("select sum from loan where g_ac=%s and t_ac=%s"%(g,t))
                    s=n.fetchone()
                    q=s[0]-am
                    n.execute("update loan set sum=%s where g_ac=%s and t_ac=%s"%(q,g,t))
                    n.execute("insert into loant2 values(%s,%s,%s)"%(g,t,am))
                    mydb.commit()
                    print()
                    print("** YOU GIVE RUPEES ",am," LOAN FROM ACCOUNT ",g," TO ACCOUNT ",t," **")
                    print()
                    recall()
                else:
                    print("** INSUFFICIENT BALANCE **")
                    print()
                    recall()
    elif(c=='2'):
        print()
        print("** ADD INTEREST **")
        print()
        j=input("ENTER ACCOUNT NUMBER FROM WHICH LOAN IS GIVEN :")
        k=input("ENTER ACCOUNT NUMBER WHICH TAKE LOAN :")
        p=mydb.cursor()
        p.execute("select interest from loan where g_ac=%s and t_ac=%s"%(j,k))
        a=p.fetchall()
        if len(a)==0:
            print("** THERE IS NOT ANY LOAN WITH THE ACCOUNT DETAILS YOU ENTERED IN OUR BANK **")
            print()
            recall()
        else:
            p.execute("select balance from amount where account_number=%s"%(k))
            a=p.fetchall()
            if len(a)==0:
                print("** THERE IS NOT ANY ACCOUNT WITH THe ACCOUNT NUMBER YOU ENTERED FOR TAKING LOAN IN OUR BANK **")
                print
                recall()
            else:
                p.execute("select interest from loan where g_ac=%s and t_ac=%s"%(j,k))
                u=p.fetchone()
                e=u[0]
                r=e/100
                p.execute("select sum from loan where g_ac=%s and t_ac=%s"%(j,k))
                b4=p.fetchone()
                tb4=b4[0]*r
                tc=tb4+b4[0]
                p.execute("update loan set sum=%s where g_ac=%s and t_ac=%s"%(tc,j,k))
                p.execute("select loan_taken from amount where account_number=%s"%(k))
                v=p.fetchone()
                th=v[0]+tb4
                p.execute("update amount set loan_taken=%s where account_number=%s",(th,k))
                p.execute("select loan_given from amount where account_number=%s"%(j))
                b5=p.fetchone()
                tb5=b5[0]+tb4
                p.execute("update amount set loan_given=%s where account_number=%s",(tb5,j))
                p.execute("insert into interest values(%s,%s,%s,%s)"%(j,k,r,tb4))
                mydb.commit()
                print()
                print("** INTEREST OF ",e,"% ADDED TO YOUR ACCOUNT ",k," FOR LAON OF RUPEES ",tb4," **")
                print()
                recall()
    elif(c=='4'):
        print()
        print("** LOAN DETAILS **")
        print()
        j=input("ENTER ACCOUNT NUMBER FROM WHICH LOAN IS GIVEN :")
        k=input("ENTER ACCOUNT NUMBER WHICH TAKE LOAN :")
        p=mydb.cursor()
        p.execute("select sum from loan where g_ac=%s and t_ac=%s"%(j,k))
        a=p.fetchall()
        if len(a)==0:
            print("** THERE IS NOT ANY LOAN WITH THE ACCOUNT DETAILS YOU ENTERED IN OUR BANK**")
            print()
            recall()
        else:
            p.execute("select sum from loan where g_ac=%s and t_ac=%s"%(j,k))
            b=p.fetchone()
            m=b[0]
            print("REMAINING LOAN AMOUNT = ",m)
            recall()
    else:
        print("** WRONG CHOICE **")
        loan()
def transfer():
    print()
    print("** TRANSACTION **")
    print()
    d=int(input("ENTER ACCOUNT TO BE DEBITED :"))
    c=int(input("ENTER ACCOUNT TO BE CREDITED :"))
    p=mydb.cursor()
    p.execute("select balance from amount where account_number=%s"%(d))
    a=p.fetchall()
    if len(a)==0:
        print("** THERE IS NOT ANY ACCOUNT WITH THE ACOOUNT NUMBER YOU ENTERED TO BE DEBITED IN OUR BANK **")
        print()
        recall()
    else:
        p.execute("select balance from amount where account_number=%s"%(c))
        a=p.fetchall()
        if len(a)==0:
            print("THERE IS NOT ANY ACCOUNT WITH THE ACOOUNT NUMBER YOU ENTERED TO BE DEBITED IN OUR BANK **")
            print()
            recall()
        else:
            am=int(input("ENTER AMOUNT TO BE TRANSFERED :"))
            p.execute("select balance from amount where account_number=%s"%(d))
            b=p.fetchone()
            ta=b[0]
            if am<=ta:
                tb=b[0]-am
                p.execute("update amount set balance=%s where account_number=%s",(tb,d))
                p.execute("insert into withd values(%s,%s)"%(d,am))
                p.execute("select balance from amount where account_number=%s"%(c))
                x=p.fetchone()
                tv=x[0]+am
                p.execute("update amount set balance=%s where account_number=%s",(tv,c))
                p.execute("insert into dep values(%s,%s)"%(c,am))
                p.execute("insert into transfer values(%s,%s,%s)"%(d,c,am))
                mydb.commit()
                print()
                print("** YOU TRANSFER RS ",am," FROM ACCOUNT ",d," TO ACCOUNT ",c," **")
                print()
                recall()
            else:
                print("Insufficient balance")
                print()
                recall()
            
def main():
    print()
    print("** MAIN **")
    print()
    print("1. OPEN NEW ACCOUNT","2. DEPOSIT MONEY","3. WITHDRAW MONEY","4. BALANCE ENQUIRY","5. ACCOUNT DETAILS","6. CLOSE YOUR ACCOUNT","7. LOAN","8. TRANSFER MONEY","9. EXIT", sep='\n')
    print()
    c=input("ENTER YOUR CHOICE :")
    if(c=='1'):
        openaccount()
    elif(c=='2'):
        deposit()
    elif(c=='3'):
        withdraw()
    elif(c=='4'):
        balance()
    elif(c=='5'):
        details()
    elif(c=='6'):
        close()
    elif(c=='7'):
        loan()
    elif(c=='8'):
        transfer()
    elif(c=='9'):
        print()
        print("***** THANK YOU *****")
        print("***** HAVE A NICE DAY *****")
    else:
        print()
        print("** WRONG CHOICE **")
        print()
        recall()
print(" ***** WELCOME TO GLOBAL BANK *****")
main()