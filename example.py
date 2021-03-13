from flask import Flask
from data import db_session
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = "21"
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)

    user = User()
    user.surname = "Surn"
    user.name = "Na"
    user.age = "123"
    user.position = "cook"
    user.speciality = "aboltus"
    user.address = "55.5, 66.6"
    user.email = "mail@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)

    user = User()
    user.surname = "Sun"
    user.name = "Ame"
    user.age = "277"
    user.position = "assistant"
    user.speciality = "aboltus"
    user.address = "module_0"
    user.email = "mail@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)

    user = User()
    user.surname = "Urn"
    user.name = "Nam"
    user.age = "A12"
    user.position = "assistant"
    user.speciality = "aboltus"
    user.address = "module_777"
    user.email = "mail@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)

    db_sess.commit()

    app.run()


if __name__ == '__main__':
    main()
