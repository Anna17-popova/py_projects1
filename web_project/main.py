import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api
from web_project.data import db_session, UserRecource, ProductRecource
from web_project.data.authorization import LoginForm
from web_project.data.products import Product
from web_project.data.register import RegisterForm
from web_project.data.users import User
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
api = Api(app)
run_with_ngrok(app)
db_session.global_init("db/data.db")
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_FOLDER = './static/img/'
ALLOWED_EXTENSIONS = ['pdf','jpg', 'jpeg']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api.add_resource(UserRecource.UsersListResource, '/api/users')
api.add_resource(UserRecource.UsersResource, '/api/users/<int:user_id>')
api.add_resource(ProductRecource.ProductsListResource, '/api/products')
api.add_resource(ProductRecource.ProductsResource, '/api/products/<int:product_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('authorization.html',
                               message="Неправильное имя или пароль",
                               form=form)
    return render_template('authorization.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Такой пользователь уже есть")
        if form.password.data == form.password_again.data:
            user = User(surname=form.surname.data, name=form.name.data, age=int(form.age.data),
                        sity=form.sity.data, email=form.email.data)
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect("/")
        return render_template('register.html', form=form, message='Пароли не совпадают')
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/catalog')
def catalog():
    mylist = []
    db_sess = db_session.create_session()
    text = 'Catalog'
    for product in db_sess.query(Product).all():
        a = [product.name, product.price, product.image, product.text, product.id]
        mylist.append(a)
    return render_template('catalog.html', title=text, mylist=mylist)

@app.route('/add_basket/<id>')
def add_basket(id):
    if not current_user.is_authenticated:
        return redirect("/authorization")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user.basket:
        if id not in user.basket:
            user.basket += ',' + str(id)
    else:
        user.basket = str(id)
    db_sess.commit()
    return redirect("/catalog")


@app.route('/product/<int:id>')
def product(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    mylist = [product.name, product.price, product.image, product.text, product.id]
    return render_template('prod.html', mylist=mylist)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/delivery')
def delivery():
    title='Delivery'
    return render_template('delivery.html', title=title)


@app.route('/contact')
def contact():
    title = 'contact'
    return render_template('contact.html', titl=title)


@app.route('/basket')
def basket():
    title = 'basket'
    mylist = []
    db_sess = db_session.create_session()
    if not current_user.basket:
        message = 'Ваша корзина пуста'
        return render_template('basket.html', title=title, message=message)
    list_of_numbers = list(map(int, current_user.basket.split(',')))
    for i in list_of_numbers:
        product = db_sess.query(Product).filter(Product.id == i).first()
        a = [product.name, product.price, product.image, product.text, product.id]
        mylist.append(a)
    return render_template('basket.html', title=title, mylist=mylist)


@app.route('/del_from_basket/<int:id>')
def del_from_basket(id):
    db_sess = db_session.create_session()
    list_of_numbers = list(map(int, current_user.basket.split(',')))
    for i in range(len(list_of_numbers)):
        if list_of_numbers[i] == id:
            del list_of_numbers[i]
            break
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.basket = ','.join(str(x) for x in list_of_numbers)
    db_sess.commit()
    db_sess.close()
    return redirect("/basket")


@app.route('/lk')
def lk():
    title = lk
    return render_template("lk.html", title=title)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.image = path
            db_sess.commit()
            db_sess.close()
        return redirect('/change_date')
    return redirect('/change_date')


@app.route('/change_date', methods=['GET', 'POST'])
@login_required
def change_date():
    form = RegisterForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id==current_user.id).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.age.data = user.age
            form.sity.data = user.sity
            form.email.data = user.email
        else:
            abort(404)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id==current_user.id).first()
    if user:
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.sity = form.sity.data
        user.email = form.email.data
        db_sess.commit()
        db_sess.close()
        return render_template('change_date.html', form=form)
    else:
        abort(404)
    return render_template('change_date.html', form=form)


@app.route('/user_delete', methods=['GET', 'POST'])
@login_required
def user_delete():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user:
        db_sess.delete(user)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    app.run()