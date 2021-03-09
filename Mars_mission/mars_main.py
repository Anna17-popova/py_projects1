from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    text = 'Заготовка'
    return render_template('base.html', title=text)


@app.route('/training/<prof>')
def training(prof):
    url = url_for('static', filename='img/ship.jpg')
    print(url)
    return render_template('professions.html', prof=prof, img=url)


if __name__ == '__main__':
    app.run(port=8070, host='127.0.0.1')
