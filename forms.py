from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, NoneOf


class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco = StringField('Preco', validators=[DataRequired()])
    estoque = IntegerField('Estoque', validators=[DataRequired()])
    categoria = StringField('Categoria', validators=[DataRequired()])
    descricao = StringField('Descricao')
