from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, make_response)
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, text
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.models import Setor, Usuario
from app.setor.forms import ListaForm, IncluiForm, AlteraForm, ListaUsuarioSetorForm
import os

setor = Blueprint('setor', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@setor.route('/setor/acessarSetor', methods=['GET', 'POST'])
@login_required
def acessarSetor():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('setor.acessarSetor'))

  form = ListaForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'setor_set.id_setor'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('setor.acessarSetor'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Setor.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Setor.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Setor.query.paginate(page=page, per_page=8)
    return render_template('lista_setor.html', title='Lista de Setores', dados=dados, form=form)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))


@setor.route('/setor/incluir', methods=['GET', 'POST'])
@login_required
def incluir():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('setor.acessarSetor'))

  form = IncluiForm()

  if request.method == 'GET':
    return render_template('inclui_setor.html', title='Incluir Setor', form=form)

  if not form.validate_on_submit():
    return render_template('inclui_setor.html', title='Incluir Setor', form=form)

  if form.validate_on_submit():
    try:
      dado = Setor(cod_empresa=form.cod_empresa.data,
        cod_diretoria=form.cod_diretoria.data,
        cod_setor=form.cod_setor.data,
        sigla=form.sigla.data,
        nome=form.nome.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('setor.acessarSetor'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('setor.acessarSetor'))


@setor.route("/setor/excluir/<int:id_data>", methods=['GET', 'POST'])
@login_required
def excluir(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('setor.acessarSetor'))

  try:
    dado = Setor.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('setor.acessarSetor'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('setor.acessarSetor'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('setor.acessarSetor'))


@setor.route('/setor/alterar/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterar(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('setor.acessarSetor'))

  form = AlteraForm()

  if request.method == 'GET':
    try:
      dado = Setor.query.get(id_data)
      form.cod_empresa.data = dado.cod_empresa
      form.cod_diretoria.data = dado.cod_diretoria
      form.cod_setor.data = dado.cod_setor
      form.sigla.data = dado.sigla
      form.nome.data = dado.nome
      return render_template('altera_setor.html', title='Alterar Setor', form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('setor.acessarSetor'))

  if not form.validate_on_submit():
    return render_template('altera_setor.html', title='Alterar Setor', form=form)

  if form.validate_on_submit():
    try:
      dado = Setor.query.get(id_data)
      dado.cod_empresa = form.cod_empresa.data
      dado.cod_diretoria = form.cod_diretoria.data
      dado.cod_setor = form.cod_setor.data
      dado.sigla = form.sigla.data
      dado.nome = form.nome.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('setor.acessarSetor'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('setor.acessarSetor'))


@setor.route('/setor/imprimir', methods=['GET'])
@login_required
def imprimir():

  from app.principal.relatorios import imprimir_reportlab

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Setor.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Setor.query.order_by(order_column).all()
    else:
      dados = Setor.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('setor.acessarSetor'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE SETORES'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['SIGLA', 'row.sigla', 100, 180],
    ['NOME', 'row.nome', 200, 400]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response

# # #    TABELA 2    # # # # # # # # # # # # # # # # # # #
@setor.route('/setor/acessarUsuario/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def acessarUsuario(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))

  form = ListaUsuarioSetorForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'usuario_usu.id_usuario'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))

  title1='Lista de Usuários Por Setor'
  title2='Lista de Usuários'

  try:
    print(id_super)
    por_page1 = 5
    page1 = request.form.get('page1', 1, type=int)
    dados1 = Usuario.query.filter_by(setor_id=id_super).paginate(page=page1, per_page=por_page1)

    por_page2 = 5
    page2 = request.form.get('page2', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados2 = Usuario.query.order_by(order_column).filter(filter_column).paginate(page=page2, per_page=por_page2)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados2 = Usuario.query.order_by(order_column).paginate(page=page2, per_page=por_page2)
    else:
      dados2 = Usuario.query.paginate(page=page2, per_page=por_page2)

    return render_template('lista_usuario_setor.html', title1=title1, title2=title2, id_super=id_super, nome_super=nome_super, dados1=dados1, dados2=dados2, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))


@setor.route('/setor/adicionarSetor/<int:id_data>/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def adicionarSetor(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))

  try:

    dado = Usuario.query.get(id_data)

    if dado.has_role(id_super):
      flash('Registro já cadastrado!', 'danger')
      return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))

    if dado:
      dado.setor_id = id_super
      db.session.commit()
      flash('Registro foi adicionado ao setor com sucesso!', 'success')
      return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na adiçao do usuário!', 'danger')
      return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))
  except IntegrityError:
    db.session.rollback()
    flash('Registro já cadastrado! ', 'danger')
    return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))


@setor.route("/setor/excluirUsuarioSetor/<int:id_data>/<int:id_super>/<string:nome_super>", methods=['GET', 'POST'])
@login_required
def excluirUsuarioSetor(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))

  try:

    dado = Usuario.query.get(id_data)

    if dado:
      dado.setor_id = None
      db.session.commit()
      flash('Registro foi excluido do setor com sucesso!', 'success')
      return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('setor.acessarUsuario', id_super=id_super, nome_super=nome_super))


@setor.route('/setor/imprimir2/<int:id_super>/<string:nome_super>', methods=['GET'])
@login_required
def imprimir2(id_super, nome_super):

  from app.principal.relatorios import imprimir_reportlab

  # LÊ BASE DE DADOS
  try:
    dados = Usuario.query.filter_by(setor_id=id_super)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('setor.acessarUsuario' , id_super=id_super, nome_super=nome_super))

  if dados:
    # # # PARÂMETROS DO RELATÓRIO
    titulo = 'LISTA DE USUÁRIOS POR SETOR'
    subtitulo = 'Setor: ' + nome_super
    lista = [
      ['ID', 'row.id', 50, 80],
      ['NOME', 'row.nomecompleto', 100, 300],
    ]
    response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  else:
    response = None

  return response
