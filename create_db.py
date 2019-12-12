from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost:3306/db_framework'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Suppress deprecation warning
db = SQLAlchemy(app)


conta_grupo = db.Table('conta_grupo_cgr',
  db.Column('id_conta_cgr', db.Integer, db.ForeignKey('conta_con.id_conta'), primary_key=True),
  db.Column('id_grupo_cgr', db.Integer, db.ForeignKey('grupo_gru.id_grupo'), primary_key=True)
)


class Grupo(db.Model):

  __tablename__ = 'grupo_gru'

  id = db.Column("id_grupo", db.Integer, primary_key=True)
  nome = db.Column("ds_nome_gru", db.String(20), nullable=False, unique=True)
  descricao = db.Column("ds_descricao_gru", db.String(80))
  contas = db.relationship('Conta', secondary=conta_grupo)


class Conta(db.Model):

    __tablename__ = 'conta_con'

    id = db.Column("id_conta", db.Integer, primary_key=True)
    usuario = db.Column("ds_usuario_con", db.String(20), unique=True, nullable=False)
    email = db.Column("ds_email_con", db.String(120), unique=True, nullable=False)
    senha = db.Column("ds_senha_con", db.String(60), nullable=False)
    usuarios = db.relationship('Usuario', backref='conta', uselist=False, lazy='joined')
    grupos = db.relationship('Grupo', secondary=conta_grupo)


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


db.drop_all()
db.create_all()
print("DB Criado!!!")
