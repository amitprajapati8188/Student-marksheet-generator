import mysql.connector
from tabulate import tabulate  # Install using: pip install tabulate
# Database Connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="sms",
        charset="utf8mb4"
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# MODULE FOR NEW ADMISSION
def newStudent():
    createTable = """CREATE TABLE IF NOT EXISTS STUDENT(
                     SROLL_NO VARCHAR(5),
                     SNAME VARCHAR(30),
                     FNAME VARCHAR(30),
                     MNAME VARCHAR(30),
                     PHONE VARCHAR(12),
                     ADDRESS VARCHAR(100),
                     SCLASS VARCHAR(5),
                     SSECTION VARCHAR(5),
                     SADMISSION_NO VARCHAR(10) PRIMARY KEY)"""
    mycursor.execute(createTable)
    
    sroll_no = input("ENTER ROLL_NO: ")
    sname = input("ENTER STUDENT'S NAME: ")
    fname = input("ENTER FATHER'S NAME: ")
    mname = input("ENTER MOTHER'S NAME: ")
    phone = input("ENTER CONTACT NO.: ")
    address = input("ENTER ADDRESS: ")
    sclass = input("ENTER CLASS: ")
    ssection = input("ENTER SECTION: ")
    sadmission_no = input("ENTER ADMISSION_NO: ")
    
    sql = """INSERT INTO STUDENT (SROLL_NO, SNAME, FNAME, MNAME, PHONE, ADDRESS, SCLASS, SSECTION, SADMISSION_NO)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = (sroll_no, sname, fname, mname, phone, address, sclass, ssection, sadmission_no)
    
    try:
        mycursor.execute(sql, values)
        mydb.commit()
        print("Student added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# MODULE TO DISPLAY STUDENT'S DATA

def displayStudent():
    mycursor.execute("SELECT * FROM STUDENT")
    data = mycursor.fetchall()
    
    if data:
        headers = ["Roll No", "Name", "Father's Name", "Mother's Name", "Phone", "Address", "Class", "Section", "Admission No"]
        table = tabulate(data, headers=headers, tablefmt="grid")
        print("\nStudent Records:")
        print(table)
    else:
        print("No student records found.")

# MODULE TO UPDATE STUDENT'S RECORD
def updateStudent():
    admission_no = input("ENTER ADMISSION NO: ")
    sql = "SELECT * FROM STUDENT WHERE SADMISSION_NO= %s"
    mycursor.execute(sql, (admission_no,))
    data = mycursor.fetchall()
    
    if data:
        print("PRESS 1 TO UPDATE NAME")
        print("PRESS 2 TO UPDATE CLASS")
        print("PRESS 3 TO UPDATE ROLL NO")
        choice = int(input("Enter Your Choice: "))
        
        if choice == 1:
            name = input("ENTER NEW NAME: ")
            sql = "UPDATE STUDENT SET SNAME= %s WHERE SADMISSION_NO= %s"
            mycursor.execute(sql, (name, admission_no))
        elif choice == 2:
            std = input("ENTER NEW CLASS: ")
            sql = "UPDATE STUDENT SET SCLASS= %s WHERE SADMISSION_NO= %s"
            mycursor.execute(sql, (std, admission_no))
        elif choice == 3:
            roll_no = input("ENTER NEW ROLL NO: ")
            sql = "UPDATE STUDENT SET SROLL_NO= %s WHERE SADMISSION_NO= %s"
            mycursor.execute(sql, (roll_no, admission_no))
        else:
            print("Invalid choice!")
            return
        
        mydb.commit()
        print("Record updated successfully!")
    else:
        print("Record Not Found, Please Try Again!")

# MODULE TO ENTER MARKS OF STUDENT
def marksStudent():
    createTable = """CREATE TABLE IF NOT EXISTS MARKS(
                     SADMISSION_NO VARCHAR(10) PRIMARY KEY,
                     HINDI INT, ENGLISH INT, MATH INT, SCIENCE INT,
                     SOCIAL INT, COMPUTER INT, TOTAL INT, AVERAGE DECIMAL(5,2))"""
    mycursor.execute(createTable)
    
    admission_no = input("ENTER ADMISSION NO: ")
    hindi = int(input("ENTER MARKS FOR HINDI: "))
    english = int(input("ENTER MARKS FOR ENGLISH: "))
    math = int(input("ENTER MARKS FOR MATH: "))
    science = int(input("ENTER MARKS FOR SCIENCE: "))
    social = int(input("ENTER MARKS FOR SOCIAL STUDIES: "))
    computer = int(input("ENTER MARKS FOR COMPUTER: "))
    
    total = hindi + english + math + science + social + computer
    average = total / 6
    
    sql = """INSERT INTO MARKS (SADMISSION_NO, HINDI, ENGLISH, MATH, SCIENCE, SOCIAL, COMPUTER, TOTAL, AVERAGE)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = (admission_no, hindi, english, math, science, social, computer, total, average)
    
    try:
        mycursor.execute(sql, values)
        mydb.commit()
        
        data = [(admission_no, hindi, english, math, science, social, computer, total, average)]
        headers = ["Admission No", "Hindi", "English", "Math", "Science", "Social", "Computer", "Total", "Average"]
        table = tabulate(data, headers=headers, tablefmt="grid")
        
        print("\nMarks Entered Successfully!")
        print(table)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# MODULE TO GENERATE REPORT CARD FOR ALL STUDENTS


def reportCardAllStudent():
    # Joining MARKS and STUDENT tables to fetch the name of the student
    sql = """SELECT S.SNAME AS 'Student Name', M.HINDI, M.ENGLISH, M.MATH, M.SCIENCE, 
                    M.SOCIAL, M.COMPUTER, M.TOTAL, M.AVERAGE 
             FROM MARKS M
             INNER JOIN STUDENT S 
             ON M.SADMISSION_NO = S.SADMISSION_NO"""
    
    mycursor.execute(sql)
    data = mycursor.fetchall()
    
    if data:
        headers = ["Student Name", "Hindi", "English", "Math", "Science", "Social", "Computer", "Total", "Percentage"]
        table = tabulate(data, headers=headers, tablefmt="template")
        print("\nAll Students' Report Cards:")
        print(table)
    else:
        print("No records found.")

# MODULE TO GENERATE REPORT CARD FOR ONE STUDENT
def reportCardOneStudent():
    admission_no = input("ENTER ADMISSION NO: ")
    sql = "SELECT * FROM MARKS WHERE SADMISSION_NO= %s"
    mycursor.execute(sql, (admission_no,))
    data = mycursor.fetchall()
    
    if data:
        headers = ["Admission No", "Hindi", "English", "Math", "Science", "Social", "Computer", "Total", "Average"]
        table = tabulate(data, headers=headers, tablefmt="grid")
        print(f"\nReport Card for Admission No {admission_no}:")
        print(table)
    else:
        print("Record Not Found, Please Try Again!")

# HELP FUNCTION
def helpMe():
    print("Visit the official website of Vidyalaya to download the manual.")

# MAIN MENU LOOP
while True:
    print("____________________________________________________________")
    print("| Enter 1 - Add Student                                    |")
    print("| Enter 2 - Display Student's Data                         |")
    print("| Enter 3 - Update Student's Data                          |")
    print("| Enter 4 - Add Student's Marks                            |")
    print("| Enter 5 - Generate All Students' Report Card             |")
    print("| Enter 6 - Generate Student Wise Report Card              |")
    print("| Enter 7 - Exit                                           |")
    print("| Enter 0 - Help                                           |")
    print("|__________________________________________________________|")
    
    choice = input("PLEASE ENTER YOUR CHOICE: ")
    
    if choice == "1":
        newStudent()
    elif choice == "2":
        displayStudent()
    elif choice == "3":
        updateStudent()
    elif choice == "4":
        marksStudent()
    elif choice == "5":
        reportCardAllStudent()
    elif choice == "6":
        reportCardOneStudent()
    elif choice == "7":
        break
    elif choice == "0":
        helpMe()
    else:
        print("Invalid input, please try again!")

# Closing connections
mycursor.close()
mydb.close()