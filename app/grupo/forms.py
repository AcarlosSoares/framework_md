from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.models import Conta, Grupo

ordenarporConta_choices=[('conta_con.id_conta', 'Seq'), ('conta_con.ds_usuario_con', 'Nome da Conta')]
ordenarporGrupo_choices=[('grupo_gru.id_grupo', 'Seq'), ('grupo_gru.ds_nome_gru', 'Nome do Grupo')]
ordem_choices=[('ASC', 'Asc'), ('DESC', 'Desc')]

class ListaGrupoForm(FlaskForm):
  ordenarpor_tabela1 = SelectField('Ordenar Por', choices=ordenarporGrupo_choices)
  ordem_tabela1 = SelectField('ordem_tabela1', choices=ordem_choices)
  pesquisarpor_tabela1 = StringField('Filtrar Por')
  submit_enviar_tabela1 = SubmitField('Enviar')
  submit_limpar_tabela1 = SubmitField('Limpar')


class ListaContaForm(FlaskForm):
  hiden = StringField('')


class IncluiGrupoForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=2, max=20, message='Nome deve ter entre 3 e 20 caracteres!')])
  descricao = StringField('Descrição', validators=[DataRequired(message='Descrição deve ser prenchido!'), Length(min=2, max=80, message='Descrição deve ter entre 3 e 80 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_sigla(self, sigla):
      dado = Grupo.query.filter_by(nome=nome.data).first()
      if dado:
          raise ValidationError('Nome já registrada. Por favor, escolha uma nome diferente.')


class AlteraGrupoForm(FlaskForm):
  seq = StringField('Id')
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=2, max=20, message='Nome deve ter entre 3 e 20 caracteres!')])
  descricao = StringField('Descrição', validators=[DataRequired(message='Descrição deve ser prenchido!'), Length(min=2, max=80, message='Descrição deve ter entre 3 e 80 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Grupo.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')

