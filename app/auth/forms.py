from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models.models import Conta, Usuario


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email'),
        Email(message='Endereço do email inválido!')])
    senha = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembre-me')
    submit = SubmitField('Enviar')


class RegistrationForm(FlaskForm):
    usuario = StringField('Usuário', validators=[
        DataRequired(message='Informe o seu usuário!'),
        Length(min=2, max=20)])
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email!'),
        Email(message='Endereço do email inválido!')])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Informe a sua senha!')])
    confirm_senha = PasswordField('Confirme sua senha', validators=[
        DataRequired(message='Confirme a sua senha!'),
        EqualTo('senha')])
    submit = SubmitField('Enviar')

    def validate_usuario(self, usuario):
        conta = Conta.query.filter_by(usuario=usuario.data).first()
        if conta:
            raise ValidationError('Usuário já registrado. Por favor, escolha um usuário diferente.')

    def validate_email(self, email):
        conta = Conta.query.filter_by(email=email.data).first()
        if conta:
            raise ValidationError('Email já registrado. Por favor, escolha um email diferente.')


class UpdateAccountForm(FlaskForm):
    usuario = StringField('Usuário',validators=[
        DataRequired(message='Informe o seu usuário!'),
        Length(min=2, max=20,
        message='Usuário deve ter entre 3 e 20 caracteres!')])
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email!'),
        Email(message='Endereço do email inválido!')])
    picture = FileField('Atualize a foto da sua conta', validators=[FileAllowed(['jpg', 'png'])])
    senha = PasswordField('Nova Senha', validators=[
        DataRequired(message='Informe a sua nova senha!')])
    confirm_senha = PasswordField('Confirme sua nova senha', validators=[
        DataRequired(message='Confirme a sua nova senha!'),
        EqualTo('senha')])
    submit = SubmitField('Atualizar')

    def validate_usuario(self, usuario):
        if usuario.data != current_user.usuario:
            conta = Conta.query.filter_by(usuario=usuario.data).first()
            if conta:
                raise ValidationError('Usuário já registrado. Por favor, escolha um usuário diferente.')

    def validate_email(self, email):
        if email.data != current_user.email:
            conta = Conta.query.filter_by(email=email.data).first()
            if conta:
                raise ValidationError('Email já registrado. Por favor, escolha um email diferente.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email!'),
        Email(message='Endereço do email inválido!')])
    submit = SubmitField('Enviar')

    def validate_email(self, email):
        conta = Conta.query.filter_by(email=email.data).first()
        if conta is None:
            raise ValidationError('Não existe uma conta registrada com este email. Voce deve primeiro se registrar.')


class ResetPasswordForm(FlaskForm):
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Informe a sua senha!')])
    confirm_senha = PasswordField('Confirme a sua senha', validators=[
        DataRequired(message='Confirme a sua senha!'),
        EqualTo('senha')])
    submit = SubmitField('Enviar')
