from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models.models import Conta, Usuario, Grupo
from app.auth.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from app.auth.utils import save_picture, send_reset_email
import os

auth = Blueprint('auth', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@auth.route("/login", methods=['GET', 'POST'])
def login():

  if current_user.is_authenticated:
    return redirect(url_for('principal.inicio'))

  form = LoginForm()

  if form.validate_on_submit():
    try:
      conta = Conta.query.filter_by(email=form.email.data).first()
      if conta and bcrypt.check_password_hash(conta.senha, form.senha.data):
        login_user(conta, remember=form.remember.data) # The "remember me" functionality allows users to remain logged in even after closing the browser window.
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('principal.inicio'))
      else:
        flash('Ocorreu uma falha no acesso. Verifique seu email e senha.', 'danger')
    except Exception as e:
      flash('Ocorreu uma falha! ' + str(e), 'danger')

  return render_template('login.html', title='Login', form=form)


@auth.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('principal.inicio'))


@auth.route("/register", methods=['GET', 'POST'])
def register():

  # if current_user.is_authenticated:
  #   return redirect(url_for('main.home'))

  populateGrupo()  # Cadastra o grupo "Administradores" caso ainda não exista

  form = RegistrationForm()

  if form.validate_on_submit():

    hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')

    try:
      # Cadastra Conta
      conta = Conta(usuario=form.usuario.data,
        email=form.email.data,
        senha=hashed_senha)

      db.session.add(conta)

      # Cadastra Usuario
      usuario = Usuario(nomecompleto="",
        nomeguerra="",
        datanascimento="1900-01-01 00:00:00",
        matricula="",
        cpf="",
        foto="default.jpg",
        conta=conta)

      db.session.add(usuario)

      # Cadastra Grupo
      grupo = Grupo.query.filter_by(nome="Administradores").first()
      if not grupo:
        grupo = Grupo()
        grupo.nome="Administradores"
        grupo.descricao="Grupo de Administradores da Aplicação"
        db.session.add(grupo)

      # Cadastra Conta e Grupo na tabela de associação
      conta.grupos.append(grupo)

      db.session.commit()

      flash('Sua conta foi criada! Agora você está habilitado para acessar o aplicativo.', 'success')
      return redirect(url_for('auth.login'))

    except Exception as e:
      flash('Ocorreu uma falha! ' + str(e), 'danger')
      return redirect(url_for('auth.login'))

  return render_template('register.html', title='Register', form=form)


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():

  form = UpdateAccountForm()

  if form.validate_on_submit():

    try:
      if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.usuarios.foto = picture_file

      current_user.usuario = form.usuario.data
      current_user.email = form.email.data

      db.session.commit()

      flash('Sua conta foi atualizada!', 'success')
      return redirect(url_for('auth.account'))

    except Exception as e:
      flash('Ocorreu uma falha! ' + str(e), 'danger')
      return redirect(url_for('auth.account'))

  elif request.method == 'GET':

    form.usuario.data = current_user.usuario
    form.email.data = current_user.email

  if current_user.usuarios.foto:
    foto = url_for('static', filename='profile_pics/' + current_user.usuarios.foto)
  else:
    foto = url_for('static', filename='profile_pics/' + 'default.jpg')

  return render_template('account.html', title='Account', foto=foto, form=form)


@auth.route("/reset_senha", methods=['GET', 'POST'])
def reset_senha():

  if current_user.is_authenticated:
    return redirect(url_for('main.home'))

  form = RequestResetForm()

  if form.validate_on_submit():
    conta = Conta.query.filter_by(email=form.email.data).first()
    send_reset_email(conta)
    flash('Um email foi enviado com instruções para renovar sua senha.', 'info')
    return redirect(url_for('auth.login'))

  return render_template('reset_request.html', title='Solicite nova senha', form=form)


@auth.route("/reset_token/<token>", methods=['GET', 'POST'])
def reset_token(token):

  if current_user.is_authenticated:
    return redirect(url_for('main.home'))

  try:
    conta = Conta.verify_reset_token(token)

    if conta is None:
      flash('Este token está inválido ou expirado!', 'warning')
      return redirect(url_for('auth.reset_senha'))

  except Exception as e:
    flash('Ocorreu uma falha! ' + str(e), 'danger')
    return redirect(url_for('auth.reset_senha'))

  form = ResetPasswordForm()

  if form.validate_on_submit():

    try:
      hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
      conta.senha = hashed_senha
      db.session.commit()
      flash('Sua senha foi atualizada! Você já pode acessar o aplicativo', 'success')
      return redirect(url_for('auth.login'))
    except Exception as e:
      flash('Ocorreu uma falha! ' + str(e), 'danger')
      return redirect(url_for('auth.reset_senha'))

  return render_template('reset_token.html', title='Reset Password', form=form)


def populateGrupo():

  try:
    grupo = Grupo.query.filter_by(nome="Administradores").first()
    if not grupo:
      grupo = Grupo()
      grupo.nome="Administradores"
      grupo.descricao="Grupo de Administradores da Aplicação"
      db.session.add(grupo)
      db.session.commit()
  except Exception as e:
    flash('Ocorreu uma falha! ' + str(e), 'danger')
    return redirect(url_for('auth.register'))

