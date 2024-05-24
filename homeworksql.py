import sqlite3
from datetime import datetime

conn = sqlite3.connect('homeworkdata.db')
curser = conn.cursor()
#curser.execute("DROP TABLE subjects;")
# query = (
#       """
#                  CREATE TABLE homeworks (
#                  homeworkid INTEGER PRIMARY KEY,
#                  name text, 
#                  subject text,
#                  due date,
#                  userid INTEGER
#                  )
#                  ;
#                  """)



# query = (
#     """
#                 CREATE TABLE users ( 
#                 userid INTEGER PRIMARY KEY,
#                 name text,
#                 password text
#                 );""")
# curser.execute(query)


# query = (
#     """
#                  CREATE TABLE subjects (
#                  subjectid INTEGER PRIMARY KEY,
#                  userid INTEGER,
#                  subjectname text
#                  );
#                  """)
# curser.execute(query)
#curser.execute("INSERT INTO users (name, password) VALUES (?, ?);", ("Lucian", "Pass123"))
#data = curser.fetchall()
#print(data)
#curser.execute("SELECT userid FROM users WHERE name = 'Lucian'")

curser.execute("DELETE FROM homeworks")
conn.commit()
curser.close()


def users():
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    query = """SELECT name, password, userid FROM users  """
    curser.execute(query)
    data = curser.fetchall()
    conn.commit()
    conn.close()
    return data

def usernames(user):
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    curser.execute("SELECT name FROM users WHERE userid = ? ", (user))
    data = curser.fetchall()
    conn.commit()
    conn.close()
    return data
def useradd(username, password):
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    curser.execute("INSERT INTO users (name, password) VALUES (?,?)", (username, password))
    conn.commit()
    conn.close()

def add(name, subject, due, user):
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    due = datetime.strptime(due, "%Y-%m-%d").strftime("%d/%m/%Y")
    curser.execute("INSERT INTO homeworks (name, subject, due, userid) VALUES (?,?,?,?);", (name, subject, due, user))
    curser.execute("SELECT subjectid FROM subjects WHERE subjectname = ?",(subject,))
    data = curser.fetchall()
    if len(data) == 0:
        curser.execute("INSERT INTO subjects (subjectname, userid) VALUES (?,?)", (subject, user))
    conn.commit()
    conn.close()

def subjectget(user):
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    curser.execute("SELECT subjectname, subjectid FROM subjects WHERE userid = ?", (user))
    conn.commit()
    data = curser.fetchall()
    return data

def retrieve(filter, user):
    global data
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    #query = "DELETE FROM homeworks"
    filter = str(filter)
    query = "SELECT homeworkid, name, subject, due FROM homeworks WHERE userid = '"+user+"' "+filter
    print(query)
    curser.execute(query)
    data = curser.fetchall()
    conn.close()
    return data

def submit(task):
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    curser.execute(" DELETE FROM homeworks  WHERE homeworkid = ?", (task))
    conn.commit()
    conn.close()

def managesubject(op, subject,user):
    conn = sqlite3.connect('homeworkdata.db')
    curser = conn.cursor()
    if op == 'delete':
        curser.execute(" DELETE FROM subjects WHERE subjectid = (?) AND userid = (?)", (subject, user))
    elif op == 'add':
        curser.execute(" INSERT INTO subjects (subjectname, userid) VALUES (?,?)", (subject, user))
    conn.commit()


