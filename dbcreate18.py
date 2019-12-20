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

 # c = Conta.query.all()
 # u = Usuario.query.all() -> [<Usuario 1>, <Usuario 2>, <Usuario 3>]
 # s = Setor.query.all()
 # print(s[0].sigla) -> ETICE
 # print(s[0].usuarios_do_setor) -> []
 # print(s[2].usuarios_do_setor) -> [<Usuario 1>, <Usuario 2>]
 # print(s[2].usuarios_do_setor[0].nomecompleto) -> Antonio Carlos
 # print(s[2].usuarios_do_setor[1].nomecompleto) -> Francisca Maria
 # print(u[0].nomecompleto) -> Antonio Carlos
 # print(u[0].setor) -> <Setor 3>
 # print(u[0].setor.sigla) -> GESAC
 # Usuario.query.filter(Usuario.setor.id==3)
 # dados = Usuario.query.filter(Usuario.setor.any(id=3)).all()
 # db.session.query(Usuario).filter(Usuario.id == 2)

 # result = db.session.query(Usuario).filter(Usuario.id == 2)
# for row in result:
#   print ("ID:", row.id, "Name: ",row.nomecompleto) -> ID: 2 Name:  Francisca Maria

# result = db.session.query(Usuario).filter(Usuario.setor.id == 3)
 # for row in result:
 #   print ("ID:", row.id, "Name: ",row.nomecompleto) -> ID: 2 Name:  Francisca Maria

# u1 = Usuario.query.filter(Usuario.id==3) ??? Não retorna todos só retorna o primeiro, porque?

# u = Usuario.query.filter_by(setor_id=3).first() -> <Usuario 1>
# u = Usuario.query.filter(Usuario.setor_id==3).all() ??? Não retorna todos só retorna o primeiro, porque?

# u = Usuario.query.filter(Usuario.setor_id==2)
# print(u[0].nomecompleto) -> Antonio Carlos

# p = Usuario.query.filter_by(setor_id=3) ??? Não retorna todos só retorna o primeiro, porque?
# p[0] -> <Usuario 2>
# for i in u:
#   print(i.nomecompleto)

# query = db.session.query(Usuario).filter(Usuario.matricula.like('199')).order_by(Usuario.id)

