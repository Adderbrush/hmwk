from homeworksql import subjectget

def user_subject(user_value):
    data = subjectget(user_value)
    newdata = ['']
    y = 0
    for x in data:
        x = x[0]
        data[y] = x
        y = y + 1
    print(data)
    return data