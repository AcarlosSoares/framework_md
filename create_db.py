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
  setor_id = db.Column(db.Integer, db.ForeignKey('setor_set.id_setor'), unique=False)
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


db.drop_all()
db.create_all()
print("DB Criado!!!")

g1 = Grupo(nome="Administradores", descricao="Grupo de Administradores")
g2 = Grupo(nome="Diretores", descricao="Grupo de Diretores")
g3 = Grupo(nome="Gerentes", descricao="Grupo de Gerentes")
g4 = Grupo(nome="Operadores", descricao="Grupo de Operadores")
db.session.add(g1)
db.session.add(g2)
db.session.add(g3)
db.session.add(g4)
db.session.commit()

s1 = Setor(cod_empresa="74", cod_diretoria="00", cod_setor="00", sigla="ETICE", nome="Empresa de TI do Ceara")
s2 = Setor(cod_empresa="74", cod_diretoria="01", cod_setor="00", sigla="DIOPE", nome="Diretoria de Operaçoes")
s3 = Setor(cod_empresa="74", cod_diretoria="01", cod_setor="01", sigla="GESAC", nome="Gerencia de Atendimento")
s4 = Setor(cod_empresa="74", cod_diretoria="02", cod_setor="00", sigla="DIREN", nome="Diretoria de Relacionamentos")
db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.add(s4)
db.session.commit()

# Cadastra Conta
conta1 = Conta(usuario="ACarlos", email="acls.soares@gmail.com", senha="$12$rWMjGE6LhXBDtuqSRzw3LubNgj/SZ/A0zLLaGgtYdDrFO8lbvJWcy")
conta2 = Conta(usuario="Francisca", email="kita@hotmail.com", senha="$12$rWMjGE6LhXBDtuqSRzw3LubNgj/SZ/A0zLLaGgtYdDrFO8lbvJWcy")
conta3 = Conta(usuario="Pedro", email="pedro@hotmail.com", senha="$12$rWMjGE6LhXBDtuqSRzw3LubNgj/SZ/A0zLLaGgtYdDrFO8lbvJWcy")
conta1.grupos.append(g3)
conta2.grupos.append(g3)
conta3.grupos.append(g4)
db.session.add(conta1)
db.session.add(conta2)
db.session.add(conta3)

# Cadastra Usuario
usuario1 = Usuario(nomecompleto="Antonio Carlos", nomeguerra="ACarlos", datanascimento="1961-10-26 00:00:00", matricula="19917", cpf="20366060344", foto="default.jpg", conta=conta1, setor=s3)
usuario2 = Usuario(nomecompleto="Francisca Maria", nomeguerra="Francisca", datanascimento="1961-09-23 00:00:00", matricula="18715", cpf="11111111111", foto="default.jpg", conta=conta2, setor=s3)
usuario3 = Usuario(nomecompleto="Pedro Cabral", nomeguerra="Pedro", datanascimento="1961-09-23 00:00:00", matricula="18715", cpf="11111111111", foto="default.jpg", conta=conta3, setor=s4)
db.session.add(usuario1)
db.session.add(usuario2)
db.session.add(usuario3)

db.session.commit()

print("DB Populado!!!")
