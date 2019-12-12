from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, make_response
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, text
from app import db, bcrypt
from app.auth.utils import save_picture
from app.models.models import Conta, Usuario, Grupo
from app.conta.forms import ListaContaUsuarioForm, IncluiContaUsuarioForm, AlteraContaUsuarioForm, \
 ListaGrupoForm
import os

conta = Blueprint('conta', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@conta.route('/', methods=['GET'])
@login_required
def index():
  try:
    return render_template('conta.html', title='Modulo 7')
  except TemplateNotFound:
    abort(404)


@conta.route('/conta/acessar', methods=['GET', 'POST'])
@login_required
def acessar():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessar'))

  form = ListaContaUsuarioForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'conta_con.id_conta'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('conta.acessar'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Conta.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Conta.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Conta.query.paginate(page=page, per_page=8)

    return render_template('lista_conta_conta.html', title='Lista de Contas', dados=dados, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))


@conta.route('/conta/incluir', methods=['GET', 'POST'])
@login_required
def incluir():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessar'))

  form = IncluiContaUsuarioForm()

  if request.method == 'GET':
    return render_template('inclui_conta.html', title='Incluir Conta', form=form)

  if not form.validate_on_submit():
    return render_template('inclui_conta.html', title='Incluir Conta', form=form)

  if form.validate_on_submit():
    try:

      if form.foto.data:
        picture_file = save_picture(form.foto.data)
      else:
        picture_file = "default.jpg"

      hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')

      dado = Conta(usuario=form.nomeusuario.data,
       email=form.email.data,
       senha=hashed_senha)

      db.session.add(dado)

      dado1 = Usuario(nomecompleto=form.nomecompleto.data,
        nomeguerra=form.nomeguerra.data,
        datanascimento=form.datanascimento.data,
        matricula=form.matricula.data,
        cpf=form.cpf.data,
        foto = picture_file,
        setor_id=form.setor_id.data,
        conta=dado)

      db.session.add(dado1)
      db.session.commit()

      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('conta.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('conta.acessar'))


@conta.route("/conta/excluir/<int:id_data>", methods=['POST'])
@login_required
def excluir(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessar'))

  try:
    dado = Conta.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('conta.acessar'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('conta.acessar'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.acessar'))


@conta.route('/conta/alterar/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterar(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessar'))

  form = AlteraContaUsuarioForm()

  if request.method == 'GET':
    try:
      dado = Conta.query.get(id_data)
      if (dado):
        form.nomeusuario.data = dado.usuario
        form.email.data = dado.email
        form.senha.data = dado.senha
      if (dado.usuarios):
        form.nomecompleto.data = dado.usuarios.nomecompleto
        form.nomeguerra.data = dado.usuarios.nomeguerra
        form.datanascimento.data = dado.usuarios.datanascimento
        form.matricula.data = dado.usuarios.matricula
        form.cpf.data = dado.usuarios.cpf
        form.foto.data = dado.usuarios.foto
        if dado.usuarios.setor_id:
          form.setor_id.process_data(dado.usuarios.setor_id)

      if dado.usuarios.foto:
        foto = url_for('static', filename='profile_pics/' + dado.usuarios.foto)
      else:
        foto = url_for('static', filename='profile_pics/' + 'default.jpg')

      return render_template('altera_conta.html', title='Alterar Conta', form=form, foto=foto)

    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('conta.acessar'))

  if not form.validate_on_submit():
    return render_template('altera_conta.html', title='Alterar Conta', form=form)

  if form.validate_on_submit():

    if form.foto.data:
      picture_file = save_picture(form.foto.data)
    else:
      picture_file = "default.jpg"

    try:
      hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
      dado = Conta.query.get(id_data)
      dado.usuario = form.nomeusuario.data
      dado.email = form.email.data
      dado.senha = hashed_senha
      dado.usuarios.nomecompleto = form.nomecompleto.data
      dado.usuarios.nomeguerra = form.nomeguerra.data
      dado.usuarios.datanascimento = form.datanascimento.data
      dado.usuarios.matricula = form.matricula.data
      dado.usuarios.cpf = form.cpf.data
      dado.usuarios.foto = picture_file
      dado.usuarios.setor_id = form.setor_id.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('conta.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('conta.acessar'))


@conta.route('/conta/imprimir', methods=['GET'])
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
      dados = Conta.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Conta.query.order_by(order_column).all()
    else:
      dados = Conta.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.acessar'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE CONTAS DE USUÁRIO'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.usuario', 100, 300],
    ['NOME DE GUERRA', 'row.usuarios.nomeguerra', 320, 440],
    ['MATRÍCULA', 'row.usuarios.matricula', 460, 540]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response


# # #    TABELA 2    # # # # # # # # # # # # # # # # # # #
@conta.route('/conta/acessarGrupo/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def acessarGrupo(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))

  form = ListaGrupoForm()

  title1='Lista de Grupos Por Conta'
  title2='Lista de Grupos'

  try:
    por_page1 = 5
    page1 = request.form.get('page1', 1, type=int)
    # print('{} {}'.format('Pagina: ', page1))
    dados1 = Grupo.query.filter(Grupo.contas.any(id=id_super)).paginate(page=page1, \
     per_page=por_page1)

    por_page2 = 5
    page2 = request.form.get('page2', 1, type=int)
    dados2 = Grupo.query.paginate(page=page2, per_page=por_page2)

    return render_template('lista_grupo_conta.html', title1=title1, title2=title2, id_super=id_super, \
     nome_super=nome_super, dados1=dados1, dados2=dados2, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('auth.logout'))


@conta.route('/conta/adicionarGrupo/<int:id_data>/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def adicionarGrupo(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))

  try:
    dado = Conta.query.get(id_super)
    dado1 = Grupo.query.get(id_data)

    if dado.has_role(dado1.nome):
      flash('Registro já cadastrado!', 'danger')
      return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))

    dado1.contas.append(dado)
    db.session.commit()
    flash('Registro foi incluído com sucesso!', 'success')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))
  except IntegrityError:
    db.session.rollback()
    flash('Registro já cadastrado! ', 'danger')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))


@conta.route("/conta/excluirGrupoConta/<int:id_data>/<int:id_super>/<string:nome_super>", methods=['POST'])
@login_required
def excluirGrupoConta(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))

  try:
    dado = Conta.query.get(id_super)
    dado1 = Grupo.query.get(id_data)
    if dado:
      # exclui somente da tabela de associação
      dado1.contas.remove(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.acessarGrupo', id_super=id_super, nome_super=nome_super))


@conta.route('/conta/imprimir2/<int:id_super>/<string:nome_super>', methods=['GET'])
@login_required
def imprimir2(id_super, nome_super):

  from app.principal.relatorios import imprimir_reportlab

  # LÊ BASE DE DADOS
  try:
    dados = Grupo.query.filter(Grupo.contas).all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.acessarGrupo' , id_super=id_super, nome_super=nome_super))

  if dados:
    # # # PARÂMETROS DO RELATÓRIO
    titulo = 'LISTA DE GRUPOS POR CONTA'
    subtitulo = 'Conta: ' + nome_super
    lista = [
      ['ID', 'row.id', 50, 80],
      ['NOME', 'row.nome', 100, 300],
    ]
    response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  else:
    response = None

  return response
