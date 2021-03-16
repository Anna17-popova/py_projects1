from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    #app.run()
    user = User()
    user.surname = 'Scott'
    user.name = 'Ridley'
    user.age = 21
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    user1 = User()
    user1.surname = 'Scott'
    user1.name = 'Mark'
    user1.age = 18
    user1.position = 'navigator'
    user1.speciality = 'engineer'
    user1.address = 'module_2'
    user1.email = 'mark_chief@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user1)
    db_sess.commit()
    user2 = User()
    user2.surname = 'Smith'
    user2.name = 'Ellis'
    user2.age = 18
    user2.position = 'doctor'
    user2.speciality = 'doctor'
    user2.address = 'module_3'
    user2.email = 'ellis_smith@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user2)
    db_sess.commit()
    user3 = User()
    user3.surname = 'Smith'
    user3.name = 'Jane'
    user3.age = 20
    user3.position = 'scientist'
    user3.speciality = 'scientist'
    user3.address = 'module_4'
    user3.email = 'jane_smith@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user3)
    db_sess.commit()


if __name__ == '__main__':
    main()
