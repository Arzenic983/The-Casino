from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/geg')
def geg():
    return """
         <!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">                    
                        <title>Azino777</title>
                    </head>
                    <body>
                        <h1>Арабское казино<h1>
                    </body>
                    </html>
        """


@app.route('/sign_')
def sign():
    return """
         <!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">                    
                        <title>вход/регистрация</title>
                    </head>
                    <body>
                        <h1>Е___ый в рот этого казино...<h1>
                    </body>
                    </html>
        """


@app.route('/lottery')
def lottery():
    return


@app.route('/roulette')
def roulette():
    return


@app.route('/me')
def account():
    return


if __name__ == '__main__':
    app.run()
