# Импорты связанные с фреймворком Flask
from flask import Flask, render_template, redirect, url_for, g, request, flash
from flask_login import login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# Импорты связанные с os, sqlite3, time
import os
import sqlite3
import time

# Импорты связанные с файлами проекта 
from FDataBase import FDataBase
from UserLogin import UserLogin

# Конфигурация 
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'nvueinrvjienrvqi312uwnvo43veirn5'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

# Подключение к базе данных
def connect_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection

# Создание базы данных
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# Соеденение с базой данных если его еще нету
def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    
    return g.link_db



# Роуты и тд
# Главная страница 
@app.route('/')
def index():
    return render_template('index.html', menu=dbase.getMenu())

# Устанавливаем соеденение с базой данных перед запросом
dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

# Закрытие базы данных если оно было установленно 
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link.db'):
        g.link_db.close()


# Обработчик для страницы на которой находятся
@app.route('/tests', methods=['POST', 'GET'])
def tests():
    random_word = dbase.getRandomWord()
    if request.method == 'POST':
        user_translation = request.form['translation']
        correct_translation = request.form['correct_translation']
        if user_translation.strip().lower() == correct_translation.strip().lower():
            flash('Перевод правильный !', 'success')
        else:
            flash(f"Неправильно. Правильный перевод: {correct_translation}", 'error')

        return render_template('tests.html', word=random_word)
    
    return render_template('tests.html', word=random_word)

@app.route('/login')
def login():
    return render_template('login.html')

# Обработчик для регистрации 
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        # Проверка на длину usernamec
        if len(request.form['username']) < 4:
            flash('Длина вашего username должна быть больше 4 символов!', 'error')
            return render_template('registration.html')
        
        # Проверка на существование username в базе
        user_check = dbase.getUserUsername(request.form['username'])
        if user_check and user_check['count'] > 0:  # Проверяем, если вернулся результат и count > 0
            flash('Пользователь с таким username уже существует', 'error')
            return render_template('registration.html')
        
        # Проверка на длину email
        if len(request.form['email']) < 4:
            flash('Длина вашего email должна быть больше 4 символов', 'error')
            return render_template('registration.html')
        
        # Проверка на существование email в базе
        email_check = dbase.getUserEmail(request.form['email'])
        if email_check and email_check['count'] > 0:  # Проверка вернулся ли результат и count > 0
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('registration.html')
        
        # Проверка на длину пароля и равен ли password и confirm_password
        if len(request.form['password']) < 4 or request.form['password'] != request.form['confirm_password']:
            flash('Длина пароля меньше 4 символов либо пароли не совпадают', 'error')
            return render_template('registration.html')
        
        # Если все проверки пройдены
        hash = generate_password_hash(request.form['password'])
        res = dbase.addUser(request.form['username'], request.form['email'], hash)
        if res:
            flash('Вы успешно зарегистрированы! Пожалуйста, войдите в систему.', 'success')
            return redirect(url_for('login'))  # Редирект на страницу логина

    return render_template('registration.html')







if __name__ == "__main__":
    app.run(debug=True)