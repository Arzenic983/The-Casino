from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')