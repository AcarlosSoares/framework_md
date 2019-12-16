from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc, text
from app import db
from app.models.models import Conta, Grupo
from app.grupo.forms import ListaContaForm, ListaGrupoForm, IncluiGrupoForm, AlteraGrupoForm
import os

grupo = Blueprint('grupo', __name__, template_folder=os.path.join(os.path.dirname(__file__), \
 'templates'))


@grupo.route('/index6', methods=['GET'])
@login_required
def index():
  try:
    return render_template('grupo.html', title='Modulo 6')
  except TemplateNotFound:
    abort(404)


# # #    TABELA 1    # # # # # # # # # # # # # # # # # # #
@grupo.route('/grupo/acessarGrupo', methods=['GET', 'POST'])
@login_required
def acessarGrupo():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarGrupo'))

  form = ListaGrupoForm()

  title='Lista de Grupos'

  data1 = request.form.get('ordenarpor_tabela1')
  data2 = request.form.get('ordem_tabela1')
  data3 = request.form.get('pesquisarpor_tabela1')

  try:
    imprimir = request.form.get('imprimir')
    if imprimir:
      response = imprimir1()
      return response
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))

  limpar = request.form.get('submit_limpar_tabela1')
  if limpar:
    form.ordenarpor_tabela1.data = 'grupo_gru.id_grupo'
    form.ordenarpor_tabela1.data = 'ASC'
    form.ordenarpor_tabela1.data = None
    return redirect(url_for('grupo.acessarGrupo'))

  try:
    por_page = 8
    page = request.form.get('page', 1, type=int)
    if data1 and data2 and data3:
      order_column = text(data1 + ' ' + data2)
      filter_column = text(data1 + ' LIKE ' + "'%" + data3 + "%'")
      dados = Grupo.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=por_page)
    elif data1 and data2:
      order_column = text(data1 + ' ' + data2)
      dados = Grupo.query.order_by(order_column).paginate(page=page, per_page=por_page)
    else:
      dados = Grupo.query.paginate(page=page, per_page=por_page)

    if dados:
      return render_template('lista_grupo_grupo.html', title=title, dados=dados, form=form)
    else:
      flash('Falha no acesso ao banco de dados!', 'danger')
      return redirect(url_for('grupo.acessarGrupo'))

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))


@grupo.route('/grupo/incluirGrupo', methods=['GET', 'POST'])
@login_required
def incluirGrupo():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarGrupo'))

  form = IncluiGrupoForm()

  if request.method == 'GET':
    return render_template('inclui_grupo.html', title='Incluir Grupo', form=form)

  if not form.validate_on_submit():
    return render_template('inclui_grupo.html', title='Incluir Grupo', form=form)

  if form.validate_on_submit():
    try:
      dado = Grupo(nome=form.nome.data, descricao=form.descricao.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('grupo.acessarGrupo'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('grupo.acessarGrupo'))


@grupo.route("/grupo/excluirGrupo/<int:id_data>", methods=['GET', 'POST'])
@login_required
def excluirGrupo(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarGrupo'))

  try:
    dado = Grupo.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('grupo.acessarGrupo'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('grupo.acessarGrupo'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('grupo.acessarGrupo'))


@grupo.route('/grupo/alterarGrupo/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterarGrupo(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarGrupo'))

  form = AlteraGrupoForm()

  if request.method == 'GET':
    try:
      dado = Grupo.query.get(id_data)
      form.seq.data = id_data
      form.nome.data = dado.nome
      form.descricao.data = dado.descricao
      return render_template('altera_grupo.html', title='Alterar Grupo', form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('grupo.acessarGrupo'))

  if not form.validate_on_submit():
    return render_template('altera_grupo.html', title='Alterar Grupo', form=form)

  if form.validate_on_submit():
    try:
      dado = Grupo.query.get(id_data)
      dado.nome = form.nome.data
      dado.descricao = form.descricao.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('grupo.acessarGrupo'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('grupo.acessarGrupo'))


@grupo.route('/grupo/imprimir', methods=['GET'])
@login_required
def imprimir():

  from app.principal.relatorios import imprimir_reportlab

  data1 = request.form.get('ordenarpor_tabela1')
  data2 = request.form.get('ordem_tabela1')
  data3 = request.form.get('pesquisarpor_tabela1')

  # LÊ BASE DE DADOS
  try:
    if data1 and data2 and data3:
      order_column = text(data1 + ' ' + data2)
      filter_column = text(data1 + ' LIKE ' + "'%" + data3 + "%'")
      dados = Grupo.query.order_by(order_column).filter(filter_column).all()
    elif data1 and data2:
      order_column = text(data1 + ' ' + data2)
      dados = Grupo.query.order_by(order_column).all()
    else:
      dados = Grupo.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('grupo.acessarGrupo'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE GRUPOS'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response


# # #    TABELA 2    # # # # # # # # # # # # # # # # # # #
@grupo.route('/grupo/acessarConta/<int:id_super>/<string:nome_super>', \
 methods=['GET', 'POST'])
@login_required
def acessarConta(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))

  form = ListaContaForm()

  title1='Lista de Contas Por Grupo'
  title2='Lista de Grupos'

  try:
    imprimir = request.form.get('imprimir2')
    if imprimir:
      response = imprimir2(id_super, nome_super)
      return response
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))

  try:
    por_page1 = 5
    page1 = request.form.get('page1', 1, type=int)
    # print('{} {}'.format('Pagina: ', page1))
    dados1 = Conta.query.filter(Conta.grupos.any(id=id_super)).paginate(page=page1, \
     per_page=por_page1)

    por_page2 = 5
    page2 = request.form.get('page2', 1, type=int)
    dados2 = Conta.query.paginate(page=page2, per_page=por_page2)

    return render_template('lista_conta_grupo.html', title1=title1, title2=title2, \
     id_super=id_super, nome_super=nome_super, dados1=dados1, dados2=dados2, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))


@grupo.route('/grupo/adicionarConta/<int:id_data>/<int:id_super>/<string:nome_super>', \
 methods=['GET', 'POST'])
@login_required
def adicionarConta(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))

  try:
    dado = Grupo.query.get(id_super)
    dado1 = Conta.query.get(id_data)

    if dado.has_role(dado1.usuario):
      flash('Registro já cadastrado!', 'danger')
      return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))

    dado1.grupos.append(dado)
    db.session.commit()
    flash('Registro foi incluído com sucesso!', 'success')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))
  except IntegrityError:
    db.session.rollback()
    flash('Registro já cadastrado! ', 'danger')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))


@grupo.route("/grupo/excluirContaPorGrupo/<int:id_data>/<int:id_super>/<string:nome_super>", \
 methods=['GET', 'POST'])
@login_required
def excluirContaPorGrupo(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))

  try:
    dado = Grupo.query.get(id_super)
    dado1 = Conta.query.get(id_data)
    if dado:
      # exclui somente da tabela de associação
      dado1.grupos.remove(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))


@grupo.route('/grupo/imprimir2/<int:id_super>/<string:nome_super>', methods=['GET'])
@login_required
def imprimir2(id_super, nome_super):

  from app.principal.relatorios import imprimir_reportlab

  # LÊ BASE DE DADOS
  try:
    dados = Conta.query.filter(Conta.grupos).all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('grupo.acessarConta', id_super=id_super, nome_super=nome_super))

  if dados:
    # # # PARÂMETROS DO RELATÓRIO
    titulo = 'LISTA DE CONTAS POR GRUPO'
    subtitulo = 'Grupo: ' + nome_super
    lista = [
      ['ID', 'row.id', 50, 80],
      ['NOME', 'row.usuario', 100, 200]
    ]
    response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  else:
    response = None

  return response
