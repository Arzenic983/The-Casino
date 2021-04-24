from flask import *
from data import db_session
from data.user import User
from flask_wtf_classes import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        dbs = db_session.create_session()
        if dbs.query(User).filter(User.mail == form.mail.data.lower()).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой email уже занят")
        if dbs.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой ник уже занят")
        user = User(
            nickname=form.nickname.data,
            mail=form.mail.data.lower(),
        )
        user.set_password(form.password.data)
        user.money = 100
        dbs.add(user)
        dbs.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        dbs = db_session.create_session()
        if not dbs.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message='Такого пользователя нет')
        checking_pass = dbs.query(User).filter(User.nickname == form.nickname.data).first()
        if not checking_pass.check_password(form.password.data):
            return render_template('login.html', title='Авторизация',
                                   form=form,
                                   message='Пароль не подходит!')
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success')
def success():
    return "registration successful!"


def main_f():
    db_session.global_init("db/main_db.db")
    app.run(port=808, host="127.0.0.1")


if __name__ == '__main__':
    main_f()

