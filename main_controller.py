from flask import *

app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        return redirect('/registration')


@app.route('/registration')
def registration():
    return render_template("registration.html")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # form = LoginForm()
    # if form.validate_on_submit():
        # return redirect('/success')
    # return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

