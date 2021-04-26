from flask import *
from data import db_session
from data.user import User
from flask_wtf_classes import LoginForm, RegisterForm
from flask_login import LoginManager, \
    login_user, login_required, \
    logout_user, current_user
from slot_machine import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


# загрузка пользователя


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    print(" * Кто-то на главной странице")
    if request.method == 'GET':
        return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    print(" * Кто-то на странице регистрации")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print(" * Кто-то ввёл разные пароли")
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        dbs = db_session.create_session()
        if dbs.query(User).filter(User.mail == form.mail.data.lower()).first():
            print(" * Кто-то ввёл занятый емайл")
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой email уже занят")
        if dbs.query(User).filter(User.nickname == form.nickname.data).first():
            print(" * Кто-то ввёл занятый никнейм")
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой ник уже занят")
        user = User()
        user.nickname = form.nickname.data
        user.mail = form.mail.data.lower()
        user.set_password(form.password.data)
        user.money = 100
        dbs.add(user)
        dbs.commit()
        print(f" * Кто-то успешно зарегался с ником {user.nickname}")
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(f" * Кто-то логинится")
    form = LoginForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        iuser = dbs.query(User).filter(User.nickname == form.nickname.data).first()
        if not iuser:
            print(f" * Кто-то вёл несуществующего пользователя")
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message='Такого пользователя нет')
        elif not iuser.check_password(form.password.data):
            print(" * Кто-то ввёл неверный пароль")
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message='Пароль не подходит!')
        else:
            login_user(iuser, remember=form.remember_me.data)
            print(f" * Кто-то успешно вошел с ником {iuser.nickname}!")
            return redirect('/casino')

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    print(f" * Разлогинился {current_user.nickname}")
    logout_user()
    return redirect("/")


@app.route('/casino', methods=['GET', 'POST'])
@login_required
def casino():
    print(f' * {current_user.nickname} играет в казино')
    if request.method == 'POST':
        dbs = db_session.create_session()
        if current_user.money < 10:
            print(f" * у {current_user.nickname} кончились badcoin-ы")
            return render_template('casino.html',
                                   user=current_user.nickname,
                                   balance=current_user.money,
                                   slot=[0, 0, 0],
                                   message='Какая жалость, у вас кончились деньги... приходите завтра!')

        else:
            current_user.money -= 10
            result = spin()
            current_user.money += result[1]
            iuser = dbs.query(User).filter(User.nickname == current_user.nickname).first()
            iuser.money = current_user.money
            dbs.add(iuser)
            dbs.commit()
            if result[1] != 0:
                print(f' * {current_user.nickname} выиграл {result[1]} монет')
            else:
                print(f' * {current_user.nickname} проиграл')
            return render_template('casino.html',
                                   user=current_user.nickname,
                                   balance=current_user.money,
                                   slot=result[0],
                                   message=result[2])
    return render_template('casino.html',
                           user=current_user.nickname,
                           balance=current_user.money,
                           slot=[0, 0, 0],
                           message='')


def main_f():
    print(' * Запуск приложения...')
    db_session.global_init("db/main_db.db")
    app.run(port=8080, host="127.0.0.1")
    print(" * Сервер выключен")


if __name__ == '__main__':
    main_f()
