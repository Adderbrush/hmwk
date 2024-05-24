from flask import Flask, render_template, redirect, url_for, request
from homeworksql import add, retrieve, submit, users, useradd, subjectget, managesubject, usernames
from user_subjects import user_subject
app = Flask(__name__,template_folder='templates', static_folder='static')
username = ''
cookie_name = 'currentuser'
global filter
filter = """ORDER BY due ASC, subject ASC;"""
data = ''

def login_required(func):
    def secure_function():
        user_value = request.cookies.get(cookie_name)
        if user_value != None:
            return redirect(url_for('login'))
    return func()

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/homework', methods=['GET', 'POST'])
@login_required
def homework():
    filter = request.form.get('filter')
    if filter == "0":
        filter = """ORDER BY due DESC, subject ASC;"""
    elif filter == "1":
        filter = """ORDER BY subject ASC, due DESC;"""
    elif filter == None:
        filter = """ORDER BY due ASC, subject ASC;"""
    user_value = request.cookies.get(cookie_name)
    data = retrieve(filter, user_value)
    user = usernames(user_value)
    user = user[0]
    return render_template('homework.html', data=data, page="homework") 

@app.route('/add', methods=['GET','POST'])
@login_required
def addition():
    global newdata
    if request.method == 'POST':
        task = request.form.get('task')
        subject = request.form.get('subject')
        date = request.form.get('due')
        user_value = request.cookies.get(cookie_name)
        add(task, subject, date, user_value)
        return redirect(url_for('homework'))
    user_value = request.cookies.get(cookie_name)
    newdata = user_subject(user_value)
    return render_template('add.html', data=newdata, page="add")

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    button_value = request.form.get('submit')
    submit(button_value)
    return redirect(url_for('homework'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    global error
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userdata = users()
        for user in userdata:
            if username == user[0]:
                error = 'User already exists'
                return redirect(url_for('login'))
        useradd(username, password)
        return redirect(url_for('login'))
    return render_template('create.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    global username
    error = None
    userdata = users()
    if request.method == 'POST':
        for user in userdata:
            username = request.form['username']
            if username == user[0] and request.form['password'] == user[1]:
                resp = redirect(url_for('home'))
                resp.set_cookie(cookie_name, str(user[2]))
                return resp
        error = 'Incorrect, please try again.'
    return render_template('login.html', error=error)

@app.route('/subject/<name>', methods=['GET', 'POST'])
@login_required
def subjectview(name):
    user_value = request.cookies.get(cookie_name)
    newdata = user_subject(user_value)
    if str(name) in newdata:
        filter = "AND subject == '"+str(name)+"'"
        print(filter)
        data = retrieve(filter, user_value)
        print(data)
        return render_template('subject.html', data=data, subject=name)
    else:
        return redirect(url_for('subjects'))
    
@app.route('/subject', methods=['GET', 'POST'])
@login_required
def subjects():
    error = None
    user_value = request.cookies.get(cookie_name)
    data = subjectget(user_value)
    if request.method == 'POST':
        newsubject = request.form['subject']
        for x in data:
            if x[0] == newsubject:
                error = 'Subject already exists'
                print("yo")
        if error == None:
            managesubject('add', newsubject, user_value)
            data = subjectget(user_value)
    return render_template('subjectmanage.html', data=data, error=error, page="subject")

@app.route('/deletesubject', methods=['GET', 'POST'])
def subjectdelete():
    user_value = request.cookies.get(cookie_name)
    button_value = request.form.get('delete')
    managesubject('delete', button_value, user_value)
    return redirect(url_for('subjects'))
        


if __name__ == '__main__':
    app.run(debug=True)


