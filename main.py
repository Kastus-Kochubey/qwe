import datetime as dt
from data import db_session, jobs_api
from data.news import News
from data.users import User
from data.jobs import Job
import sqlalchemy
from flask import url_for, request, Flask, render_template, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
import requests
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField
from flask import redirect
from flask_wtf import FlaskForm

from forms.Job import AddJobForm
from forms.User import LoginForm
from forms.User import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Job(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data
        )

        # user = db_sess.query(User).filter(User.email == form.email.data).first()
        # if user and user.check_password(form.password.data):
        #     login_user(user, remember=form.remember_me.data)
        #     return redirect("/")
        # return render_template('login.html',
        #                        message="Неправильный логин или пароль",
        #                        form=form)
    return render_template('add_job.html', title='Авторизация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/blogs.db')
    app.register_blueprint(jobs_api.blueprint)
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
#
# @app.route('/')
# def index():
#     params = ['title', 'team_lead', 'duration', 'collaborators', 'is_finished']
#     log = [dict(zip(params, [job.job,
#                              *(f'{i.name} {i.surname}' for i in db_sess.query(User).filter(User.id == job.team_leader)),
#                              ((job.end_date or dt.datetime.now()) - job.start_date).total_seconds() // 3600,
#                              job.collaborators,
#                              job.is_finished]))
#            for job in db_sess.query(Job).all()]
#     # print(log)
#     return render_template('work_log.html', log=log)
