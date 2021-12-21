from os import abort
from flask import Flask, render_template, request
import psycopg2
from psycopg2 import OperationalError
from werkzeug.utils import redirect


def create_connection(db_name, db_user, db_password, db_host, db_port):
    # Функция, осуществляющая подключение к базе данных
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print('Connected to database')
    except OperationalError:
        print('an operating error has occurred')
    return connection


create_connection('database1', 'postgres', 'xlr22856', '127.0.0.1', '5433')


def being_in_db(stud):
    connection = create_connection('database1', 'postgres', 'xlr22856', '127.0.0.1', '5433')
    cursor = connection.cursor()
    # cursor -объект делающий запросы в бд и получающий их результаты
    cursor.execute('SELECT * FROM table1')
    result = cursor.fetchall()
    # fetchall возвращает список кортежей.Последовательная строка где каждая строка представляет собой последовательность элементов в столбцах.
    if len(result) == 0:
        return False
    # если записи нет, то возвращает фолс
    summ = []
    for user in result:
        user = list(user)
        summ1 = []
        for val in user:
            summ1.append(val.strip())
        summ.append(summ1)
    for st in summ:
        if ' '.join(st) == stud:
            # пробел между каждой записью
            return True
    return False


def recording_in_db(name, surname, phone_number):
    connection = create_connection('database1', 'postgres', 'xlr22856', '127.0.0.1', '5433')
    insert_query = (
        f"INSERT INTO table1 (name, surname, phone_number) VALUES ('{name}', '{surname}', '{phone_number}')")
    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()


def list_of_users():
    connection = create_connection('database1', 'postgres', 'xlr22856', '127.0.0.1', '5433')
    cursor = connection.cursor()
    result = None
    cursor.execute("SELECT * FROM table1")
    result = cursor.fetchall()
    total = []
    for user in result:
        user = list(user)
        total1 = []
        for val in user:
            total1.append(val.strip())
        total.append(total1)
        user_list = []
    for val in total:
        user_list.append(
            {'username': val[0] + val[1], 'name': val[0], 'surname': val[1], 'phone_number': val[2]})
    return user_list

    create_connection('database1', 'postgres', 'xlr22856', '127.0.0.1', '5433')


app = Flask(__name__)


@app.route('/', methods=["get"])
def index():
    return render_template('index.html')


@app.route('/')
def index1():
    return redirect('http://127.0.0.1:5000/users')


@app.route('/name/<name>', methods=['get'])
def name_page(name):
    return render_template('index.html', username=name)


@app.route('/users/', methods=['get', 'post'])
def users():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        phone_number = request.form.get('phone_number')
        if not being_in_db(f'{name} {surname} {phone_number}'):
            recording_in_db(name, surname, phone_number)
    return render_template('new.html', table1=list_of_users())


@app.route('/users')
def user():
    tt = ''
    for i in list_of_users():
        t = '<a href="http://127.0.0.1:5000/users/%s"> %s %s</a><br>' % (
            i['username'], i['name'], i['surname'], i['phone_number'],)
        tt += t
    return tt


@app.route('/users/<username>')
def look(username):
    users = ''
    flag = []
    for i in list_of_users():
        if username != ['username']:
            flag.append(False)
        else:
            flag.append(True)
    if any(flag) == False:
        abort(404)
    for i in list_of_users():
        if username == i['username']:
            users = i
    return f'<h2>UserName:{users["username"]} </h2> <br>' \
           f'<h2>Name:{users["name"]} </h2> <br>' \
           f'<h2> Surname:{users["surname"]} </h2> <br>' \
           f'<h2>Phone_number:{users["phone_number"]} </h2> <br>' \

if __name__ == '__main__':
    app.run(debug=True)
