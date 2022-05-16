import curses
import time
from datetime import date
from curses.textpad import Textbox, rectangle
import mysql.connector

from tabulate import tabulate

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="debanjan"
)

mycursor = mydb.cursor()
mycursor.execute("use student")
today = date.today()
d1 = today.strftime("%Y/%m/%d")


def database_creation():
    sql = "CREATE DATABASE IF NOT EXISTS student" # creats database if not exist
    mycursor.execute(sql)
    mycursor.execute("use student")
    sql_stu_data='''
                CREATE TABLE IF NOT EXISTS student_data
                (sid integer primary key,
                name char(20),
                dob date,
                phone integer,
                city char(15),
                class integer);
                '''
    sql_stu_mark='''
                CREATE TABLE IF NOT EXISTS student_marks
                (tid integer primary key,
                sid integer,
                pyear integer,
                class integer,
                sroll integer,
                tmarks integer);
                '''
    sql_stu_fee='''
                CREATE TABLE IF NOT EXISTS fees(
                txid integer primary key AUTO_INCREMENT,
                sid integer NOT NULL,
                amount integer ,
                pay_date date,
                MoP char(50),
                FOREIGN KEY (sid) REFERENCES student_data (sid));
                '''
    mycursor.execute(sql_stu_data) # creats student data table if not exist
    mycursor.execute(sql_stu_mark) # creats student marks table if not exist
    mycursor.execute(sql_stu_fee)  # creats fees table if not exist


def student_data():
    mycursor.execute("select * from student_data ORDER BY sid")
    result = mycursor.fetchall()
    return result


def student_marks():
    mycursor.execute("SELECT * FROM student_marks ORDER BY tid")
    result = mycursor.fetchall()
    return result


def student_fees():
    mycursor.execute("SELECT * FROM fees ORDER BY txid")
    result = mycursor.fetchall()
    return result


def add_student(val):
    x = tuple(val)
    sql = "INSERT INTO student_data (sid,name,dob,phone,city,class) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, x)
    mydb.commit()


def add_student_marks(val):
    x = tuple(val)
    sql = "INSERT INTO student_marks (tid,sid,pyear,class,sroll,tmarks) VALUES (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, x)
    mydb.commit()


def add_fees(val):
    x = tuple(val)
    sql = "INSERT INTO fees (sid,amount,pay_date,MoP) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, x)
    mydb.commit()


menu = ['Show Student', 'Show Marks', 'Show Fees', 'Add Student', 'Give Marks', 'Take fees', 'Clear', 'Exit']
l1 = ['Student id', 'Name', 'DoB (YYYY-MM-DD)', 'Phone', 'City', 'Class']
l2 = ["Marks id", "Student id", "Passing Year", "Class", "Roll", "Total Marks"]
l3 = ["Student id", "Amount", "Payment date (YYYY-MM-DD)", "Mode of payment (online/offline/check)"]
head1 = ["ID", "Name", "Date of birth", "Number", "City", "Class"]
head2 = ["Marks ID", "Student ID", "Passing Year", "Class", "Roll No.", "Total marks"]
head3 = ["Payment ID", "Student ID", "Amount", "Payment date", "Mode of payment"]


def print_menu(stdscr, selected_row_idx):
    # stdscr.clear()
    h, w = stdscr.getmaxyx()
    text = "Student Management System"
    x = w // 2 - len(text) // 2
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(2, x, text, curses.A_BOLD)
    stdscr.attroff(curses.color_pair(2))
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = 5 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(text) // 2
    y = h // 2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def print_val(stdscr, text, heads):
    data=[]
    stdscr.clear()
    for x in text:
        data.append(x)
    tabl = (tabulate(data, headers=heads))
    stdscr.addstr(15, 2, tabl)
    # y = 15
    # for j in text:
    #     for i in j:
    #         stdscr.addstr(y, 2, str(j))
    #     y += 1


def adding_details(stdscr, lis):
    tempo_list = []
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(2)
    stdscr.attron(GREEN_AND_BLACK)
    for i in lis:
        final_text = "Enter the " + i + " (hit Ctrl-G to send)"
        stdscr.addstr(0, 0, final_text)
        win = curses.newwin(1, 21, 2, 1)
        box = Textbox(win)
        rectangle(stdscr, 1, 0, 3, 23)
        stdscr.refresh()
        box.edit()
        val = box.gather().replace("\n", "")
        tempo_list.append(val)
    stdscr.attroff(GREEN_AND_BLACK)
    return tempo_list


def show_details(stdscr, text):
    stdscr.clear()
    y = 15
    for j in text:
        for i in j:
            stdscr.addstr(y, 2, str(j))
        y += 1
    win = curses.newwin(1, 21, 2, 1)
    rectangle(stdscr, 1, 0, 3, 23)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0

    print_menu(stdscr, current_row)
    
    database_creation()

    while 1:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # if user selected last row, exit the program

            if current_row == 0:
                stdscr.clear()
                myresult = student_data()
                print_val(stdscr, myresult, head1)
                stdscr.refresh()

            elif current_row == 1:
                stdscr.clear()
                myresult = student_marks()
                print_val(stdscr, myresult, head2)
                stdscr.refresh()
            elif current_row == 2:
                stdscr.clear()
                myresult = student_fees()
                print_val(stdscr, myresult, head3)
                stdscr.refresh()
            elif current_row == 3:
                stdscr.clear()
                x = adding_details(stdscr, l1)
                add_student(x)
                stdscr.clear()
                stdscr.refresh()
            elif current_row == 4:
                stdscr.clear()
                x = adding_details(stdscr, l2)
                add_student_marks(x)
                stdscr.clear()
                stdscr.refresh()
            elif current_row == 5:
                stdscr.clear()
                x = adding_details(stdscr, l3)
                add_fees(x)
                stdscr.clear()
                stdscr.refresh()
            elif current_row == 6:
                stdscr.clear()
                stdscr.refresh()

            elif current_row == len(menu) - 1:
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)
print(len(menu))
