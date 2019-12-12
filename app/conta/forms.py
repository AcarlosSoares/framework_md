from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from app.models.models import Conta, Usuario, Setor


ordenarpor_choices=[('conta_con.id_conta', 'Seq'), ('conta_con.ds_usuario_con', 'Usuario'), \
 ('usuario_usu_1.ds_nome_completo_usu', 'Nome'),  ('usuario_usu_1.ds_nome_guerra_usu', 'Nome de Guerra'), \
 ('usuario_usu_1.ds_matricula_usu', 'Matrícula')]
ordem_choices=[('ASC', 'Asc'), ('DESC', 'Desc')]


class ListaContaUsuarioForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarpor_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')


class IncluiContaUsuarioForm(FlaskForm):
  nomeusuario = StringField('Usuário', validators=[DataRequired(message='Usuário deve ser prenchido!'),
   Length(min=3, max=20, message='Usuário deve ter entre 3 e 20 caracteres!')])
  email = StringField('Email', validators=[DataRequired(message='Email deve ser prenchido!')])
  senha = PasswordField('Senha', validators=[DataRequired(message='Senha deve ser prenchido!')])
  confirmasenha = PasswordField('Confirma Senha', validators=[DataRequired(message='Senha deve ser prenchido!'), EqualTo('senha')])
  nomecompleto = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=80, message='Nome deve ter entre 3 e 80 caracteres!')])
  nomeguerra = StringField('Nome de Guerra', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=20, message='Nome deve ter entre 3 e 20 caracteres!')])
  datanascimento = DateField('Data de Nascimento', validators=[DataRequired(message='Data deve ser prenchida!')], format=('%Y-%m-%d'))
  matricula = StringField('Matrícula', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=5, max=11, message='Nome deve ter entre 5 e 11 caracteres!')])
  cpf = StringField('CPF', validators=[DataRequired(message='CPF deve ser prenchido!'),
   Length(min=11, max=11, message='CPF deve ter 11 caracteres!')])
  foto = FileField('Foto', validators=[FileAllowed(['jpg', 'png'])])
  setor_id = SelectField('Setor', coerce=int, validators=[DataRequired(message='Setor deve ser prenchido!')])
  submit = SubmitField('Enviar')

  def validate_nomeusuario(self, nomeusuario):
      dado = Conta.query.filter_by(usuario=nomeusuario.data).first()
      if dado:
        raise ValidationError('Usuário já registrado. Por favor, escolha um nome diferente.')

  def __init__(self):
    super(IncluiContaUsuarioForm, self).__init__()
    self.setor_id.choices = [(k.id, k.nome) for k in Setor.query.all()]


class AlteraContaUsuarioForm(FlaskForm):
  nomeusuario = StringField('Usuário', validators=[DataRequired(message='Usuário deve ser prenchido!'),
   Length(min=3, max=20, message='Usuário deve ter entre 3 e 20 caracteres!')])
  email = StringField('Email', validators=[DataRequired(message='Email deve ser prenchido!')])
  senha = PasswordField('Senha', validators=[DataRequired(message='Senha deve ser prenchido!')])
  confirmasenha = PasswordField('Confirma Senha', validators=[DataRequired(message='Senha deve ser prenchido!'), EqualTo('senha')])
  nomecompleto = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=80, message='Nome deve ter entre 3 e 80 caracteres!')])
  nomeguerra = StringField('Nome de Guerra', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=20, message='Nome deve ter entre 3 e 20 caracteres!')])
  datanascimento = DateField('Data de Nascimento', validators=[DataRequired(message='Data deve ser prenchida!')], format=('%Y-%m-%d'))
  matricula = StringField('Matrícula', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=5, max=11, message='Nome deve ter entre 5 e 11 caracteres!')])
  cpf = StringField('CPF', validators=[DataRequired(message='CPF deve ser prenchido!'),
   Length(min=11, max=11, message='CPF deve ter 11 caracteres!')])
  foto = FileField('Foto', validators=[FileAllowed(['jpg', 'png'])])
  setor_id = SelectField('Setor', coerce=int, validators=[DataRequired(message='Setor deve ser prenchido!')])
  submit = SubmitField('Enviar')

  # def validate_nomeusuario(self, nomeusuario):
  #     dado = Conta.query.filter_by(usuario=nomeusuario.data).first()
  #     if dado:
  #       raise ValidationError('Usuário já registrado. Por favor, escolha um nome diferente.')

  def __init__(self):
    super(AlteraContaUsuarioForm, self).__init__()
    self.setor_id.choices = [(k.id, k.nome) for k in Setor.query.all()]


class ListaGrupoForm(FlaskForm):
  hiden = StringField('')
