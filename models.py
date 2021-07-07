from app import app, db, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(16), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    account_type = db.Column(db.Integer)

    def __init__(self, name, username, password, account_type):
        self.name = name
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.account_type = account_type

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(16))
    total = db.Column(db.Float)

    def __init__(self, idUser, data,total):
        self.idUser = idUser
        self.data = data
        self.total = total

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    idVenda = db.Column(db.Integer, db.ForeignKey('venda.id'))
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def __init__(self, idProduto, idVenda, preco, quantidade):
        self.idProduto = idProduto
        self.idVenda = idVenda
        self.preco = preco
        self.quantidade = quantidade

class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.Float)

    def __init__(self, idUser, total):
        self.idUser = idUser
        self.total = total

    def UpdateTotal(self):
        itensById = ItemCarrinho.query.filter_by(idCarrinho=self.id)
        self.total = 0.0
        for item in itensById:
            print(item.preco,type(item.preco))
            print(item.quantidade,type(item.quantidade))
            print(float(float(item.preco) * float(item.quantidade)))
            self.total = self.total + (float(item.preco) * float(item.quantidade))
            print(self.total)
            print("")
        db.session.commit()

    def LimpaCarrinho(self):
        itensById = ItemCarrinho.query.filter_by(idCarrinho=self.id)
        for item in itensById:
            db.session.delete(item)
        self.total = 0.0
        db.session.commit()

class ItemCarrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, db.ForeignKey('produto.id'))
    idCarrinho = db.Column(db.Integer, db.ForeignKey('carrinho.id'))
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def __init__(self, idProduto, idCarrinho, preco, quantidade):
        self.idProduto = idProduto
        self.idCarrinho = idCarrinho
        self.preco = preco
        self.quantidade = quantidade

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(64), nullable=False)
    descricao = db.Column(db.String(264))
    url = db.Column(db.String(264))

    def __init__(self, nome, preco, estoque, categoria, descricao, url):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.categoria = categoria
        self.descricao = descricao
        self.url=url

if __name__=='__main__':
    db.create_all()
    db.session.add(User('Rodrigo Corga','rodrigocorga','123456',1))
    db.session.commit()