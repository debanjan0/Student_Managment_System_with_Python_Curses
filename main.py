import curses
from curses.textpad import Textbox, rectangle
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=<password>     # write your mysql password
)

mycursor = mydb.cursor()
mycursor.execute("use student")




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
    # val = (iid, name, dob, no, city, clas)
    mycursor.execute(sql, x)
    mydb.commit()


menu = ['Show Student', 'Show Marks', 'Show Fees', 'Add Student', 'Clear', 'Exit']
l2 = ['sid', 'name', 'dob (YYYY-MM-DD)', 'phone', 'city', 'class']


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


def print_val(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    y = 15
    for j in text:
        for i in j:
            stdscr.addstr(y, 2, str(j))
        y += 1


def hi(stdscr):
    tempo_list = []
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(2)
    stdscr.attron(GREEN_AND_BLACK)
    for i in l2:
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
    add_student(tempo_list)


def main(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0

    print_menu(stdscr, current_row)

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
                print_val(stdscr, myresult)
                stdscr.refresh()

            elif current_row == 1:
                stdscr.clear()
                myresult = student_marks()
                print_val(stdscr, myresult)
                stdscr.refresh()
            elif current_row == 2:
                stdscr.clear()
                myresult = student_fees()
                print_val(stdscr, myresult)
                stdscr.refresh()
            elif current_row == 3:
                stdscr.clear()
                hi(stdscr)
                stdscr.clear()
                stdscr.refresh()
            elif current_row == 4:
                stdscr.clear()
                stdscr.refresh()
            elif current_row == len(menu) - 1:
                break

        print_menu(stdscr, current_row)


curses.wrapper(main)
print(len(menu))
