from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from src.models import User
from wtforms.widgets import TextArea


class FormLogin(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    btn = SubmitField('Login')


class FormCreateNewAccount(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 25)])
    checkPassword = PasswordField('Confirme sua Senha', validators=[DataRequired(), Length(6, 25), EqualTo('password')])
    btn = SubmitField('Criar Conta')

    def validate_email(self, email):
        email_of_user = User.query.filter_by(email=email.data).first()
        if email_of_user:
            return ValidationError('~ email já existe ~')


class FormCreateNewPost(FlaskForm):
        text = StringField('Publicação', widget=TextArea(), validators=[DataRequired()])
        photo = FileField('Imagem', validators=[DataRequired()])
        btn = SubmitField('Publicar')
class LikeForm(FlaskForm): # Formulario para realizar Like
    like = SubmitField('Like')
