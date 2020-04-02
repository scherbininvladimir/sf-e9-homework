from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class CreateUserForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Повторите пароль')

class CreateEventForm(FlaskForm):
    title = StringField("Тема", validators=[DataRequired()])
    description = TextAreaField("Описание")
    start_time = DateTimeField("Время начала (ГГГГ-ММ-ДД ЧЧ:ММ:СС)", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_time = DateTimeField("Время окончания (ГГГГ-ММ-ДД ЧЧ:ММ:СС)", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
