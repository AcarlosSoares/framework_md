from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, flash
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


conta_grupo = db.Table('conta_grupo_cgr',
  db.Column('id_conta_cgr', db.Integer, db.ForeignKey('conta_con.id_conta'), primary_key=True),
  db.Column('id_grupo_cgr', db.Integer, db.ForeignKey('grupo_gru.id_grupo'), primary_key=True)
)


@login_manager.user_loader
def load_user(conta_id):
  try:
    return Conta.query.get(int(conta_id))
  except Exception as e:
    flash('Ocorreu uma falha no acesso ao banco de dados! ' + str(e), 'danger')


class Grupo(db.Model):

  __tablename__ = 'grupo_gru'

  id = db.Column("id_grupo", db.Integer, primary_key=True)
  nome = db.Column("ds_nome_gru", db.String(20), nullable=False, unique=True)
  descricao = db.Column("ds_descricao_gru", db.String(80))
  contas = db.relationship('Conta', secondary=conta_grupo)

  def has_role(self, nome):
    for conta in self.contas:
      if conta.usuario == nome:
        return True
    return False


class Conta(db.Model, UserMixin):

    __tablename__ = 'conta_con'

    id = db.Column("id_conta", db.Integer, primary_key=True)
    usuario = db.Column("ds_usuario_con", db.String(20), unique=True, nullable=False)
    email = db.Column("ds_email_con", db.String(120), unique=True, nullable=False)
    senha = db.Column("ds_senha_con", db.String(60), nullable=False)
    usuarios = db.relationship('Usuario', backref='conta', uselist=False, lazy='joined')
    grupos = db.relationship('Grupo', secondary=conta_grupo)

    def __init__(self, usuario="", senha="", email=""):
      try:
        default = Grupo.query.filter_by(nome="Administrador").one()
        self.roles.append(default)
        self.usuario = usuario
        self.senha = senha
        self.email = email
      except:
        self.usuario = usuario
        self.senha = senha
        self.email = email

    def __repr__(self):
      return f"Conta('{self.usuario}', '{self.email}')"

    def get_reset_token(self, expires_sec=1800):
      s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
      return s.dumps({'conta_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
      s = Serializer(current_app.config['SECRET_KEY'])
      try:
        conta_id = s.loads(token)['conta_id']
      except:
        return None
      return Conta.query.get(conta_id)

    def has_role(self, nome):
      for grupo in self.grupos:
        if grupo.nome == nome:
          return True
      return False


class Usuario(db.Model):

  __tablename__ = 'usuario_usu'

  id = db.Column("id_usuario", db.Integer, primary_key=True)
  nomecompleto = db.Column("ds_nome_completo_usu", db.String(60))
  nomeguerra = db.Column("ds_nome_guerra_usu", db.String(45))
  datanascimento = db.Column("ds_data_nasc_usu", db.DateTime, default=datetime.utcnow)
  matricula = db.Column("ds_matricula_usu", db.String(50))
  cpf = db.Column("ds_cpf_usu", db.String(50))
  foto = db.Column("ds_foto_usu", db.String(20), default='default.jpg')
  setor_id = db.Column(db.Integer, db.ForeignKey('setor_set.id_setor'), unique=True)
  conta_id = db.Column(db.Integer, db.ForeignKey('conta_con.id_conta'), unique=True)


class Setor(db.Model):

  __tablename__ = 'setor_set'

  id = db.Column("id_setor", db.Integer, primary_key=True)
  cod_empresa = db.Column("cd_empresa_set", db.String(4))
  cod_diretoria = db.Column("cd_diretoria_set", db.String(4))
  cod_setor = db.Column("cd_setor_set", db.String(4))
  sigla = db.Column("ds_sigla_set", db.String(10))
  nome = db.Column("ds_nome_set", db.String(45))
  usuarios_do_setor = db.relationship('Usuario', backref='setor', lazy=True)

