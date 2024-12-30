import mysql.connector as my
import random

valid_email=False
valid_password=False
valid_con=False
logged=False

con = my.connect(host = "localhost",user = "root",password ="",database="banking_system")
cur=con.cursor()
users_table = "create table users (name varchar(200), account_number varchar(200) primary key,dob date,city varchar(200),password varchar(100),Initial_Balance int CHECK (Initial_Balance>=2000),Contact_number varchar(200),email_id varchar(200),address varchar(200))"
login_table = "create table login (name varchar(200),password varchar(100))"
transaction_table="create table transaction(account_number int unique,Initial_Balance int,credit_amount int,debit_amount int)"
# cur.execute(users_table)
# cur.execute(login_table)
# cur.execute(transaction_table)

def validate_email(email):

    if email.count('@') != 1:
        return False

    local_part, domain_part = email.split('@')

    if not local_part or not domain_part:
        return False

    if '.' not in domain_part:
        return False

    if domain_part.startswith('.') or domain_part.endswith('.'):
        return False

    valid_local_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._%+-"
    valid_domain_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-"

    for char in local_part:
        if char not in valid_local_chars:
            return False

    for char in domain_part:
        if char not in valid_domain_chars:
            return False
    domain_parts = domain_part.split('.')
    if len(domain_parts) < 2:
        return False

    return True


def validate_password(password):

    if len(password) < 8 or len(password) > 20:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    special_characters = "!@#$%^&*()-_+=<>?/"

    for char in password:
        if char.isdigit():
            has_digit = True
        elif char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char in special_characters:
            has_special = True

    if not (has_upper and has_lower and has_digit and has_special):
        return False

    return True

def validate_contact_number(number):
    number = number.strip()

    if not number.isdigit():
        return False

    if len(number) != 10:
        return False

    if not (number.startswith("7") or number.startswith("8") or number.startswith("9")):
        return False

    return True



def user():
    global valid_email, valid_con, valid_password
    name=input("Enter your name:")
    cur.execute("select account_number from users")
    exist_acc=cur.fetchall()
    account_number=random.randint(1000000000, 9999999999)
    for account_number in exist_acc:
        account_number = random.randint(1000000000, 9999999999)
    dob=input("Enter your dob:(YYYY-MM-DD):")
    city=input("Enter your city:")
    password=""
    while valid_password is False:
        pwd = input("enter your Password:")
        if validate_password(pwd) is True:
            password= pwd
            valid_password = True
        else:
            print("Invalid Password \n Password must be between 8 and 20 characters and must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")

    initial_bal=int(input("Enter your initial balance:"))

    contact_number=""
    while valid_con is False:
        c_no = input("enter your contact number:")
        if validate_contact_number(c_no) is True:
            contact_number= c_no
            valid_con = True
        else:
            print("Invalid Contact Number")

    email_id=""
    while valid_email is False:
        email=input("enter your EmailID:")
        if validate_email(email) is True:
            email_id=email
            valid_email=True
        else:
            print("Invalid Email")


    address=input("Enter your address:")
    insert_table="INSERT INTO USERS(name,account_number,dob,city,password,Initial_Balance,Contact_number,email_id,address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(name,account_number,dob,city,password,initial_bal,contact_number,email_id,address)
    cur.execute(insert_table,val)

    login_insert = "insert into login (name, password) values(%s,%s)"
    val1 = (name, password)
    cur.execute(login_insert, val1)

    credit_amount=0
    debit_amount=0
    transaction_insert = "insert into transaction (account_number,Initial_Balance,credit_amount,debit_amount) values(%s,%s,%s,%s)"
    val2 = (account_number,initial_bal,credit_amount,debit_amount)
    cur.execute(transaction_insert, val2)
    con.commit()

def login():
    global logged
    username=input("Enter name:").lower()
    val_pass=""
    cmd="select * from login where name=%s"
    val=(username,)
    cur.execute(cmd,val)
    all_users=cur.fetchall()
    while logged is False:
        pwd = input("Enter password:")
        for users in all_users:
            if users[1]!=pwd:
                print("Invalid password")
            else:
                val_pass=pwd
                logged=True
    print("LogIn Successful")
    user_cmd = "select account_number from users where name=%s and password=%s"
    val1 = (username,val_pass)
    cur.execute(user_cmd, val1)
    acct_num=cur.fetchone()
    show_transaction(acct_num[0])

def show_balance(acct_num):
    print("Your Balance is:")
    query="select initial_balance from transaction where account_number=%s"
    acc=(acct_num,)
    cur.execute(query,acc)
    all_data=cur.fetchone()
    print(all_data[0])

def show_transaction(acct_num):
    print("1.Balance")
    print("2.Credit")
    print("3.Debit")

    user_input=int(input("Your choice:"))
    if user_input==1:
        show_balance(acct_num)
    elif user_input==2:
        credit(acct_num)
    elif user_input==3:
        debit(acct_num)
    else:
        print("INVALID CHOICE")
def credit(acct_num):
    user_credit = int(input("enter amount"))
    query = "select credit_amount,initial_balance from transaction where account_number=%s"
    acc = (acct_num,)
    cur.execute(query, acc)
    all_data = cur.fetchone()
    sql = "UPDATE transaction SET credit_amount = %s,initial_balance=%s WHERE account_number=%s"
    total_credit=all_data[0]+user_credit
    balance=all_data[1]+user_credit
    val=(total_credit,balance,acct_num)
    cur.execute(sql,val)
    con.commit()
    print(f"Your balance {balance}.")
    # print(all_data[0])
def debit(acct_num):
    user_debit = int(input("enter amount"))
    query = "select debit_amount,initial_balance from transaction where account_number=%s"
    acc = (acct_num,)
    cur.execute(query, acc)
    all_data = cur.fetchone()
    sql = "UPDATE transaction SET debit_amount = %s,initial_balance=%s WHERE account_number=%s"
    total_debit = all_data[0] + user_debit
    balance = all_data[1] - user_debit
    val = (total_debit, balance, acct_num)
    cur.execute(sql, val)
    con.commit()
    print(f"Your balance {balance}.")



def main():
    print("BANKING SYSTEM.")
    print("1.NEW USER.")
    print("2.LOGIN.")
    print("3.SHOW BALANCE.")
    choice=int(input("enter choice:"))
    if choice==1:
        user()
    elif choice==2:
        login()
    elif choice==3:
        print("Login First!")
    else:
        print("INVALID CHOICE")

main()

