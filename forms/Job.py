from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User

db_session.global_init('db/blogs.db')


class AddJobForm(FlaskForm):
    job = StringField('Название работы')
    db_sess = db_session.create_session()
    peoples = [f"{user.name} {user.surname}"
               for user in db_sess.query(User).all()]
    team_leader = SelectField('Тимлид', validators=[DataRequired()],
                              choices=peoples)
    work_size = IntegerField('Часов работы', validators=[DataRequired()])
    collaborators = StringField('Содеятели', validators=[DataRequired()])
    submit = SubmitField('Добавить работу')
