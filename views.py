from app import app
from app import db
from models import *
from forms import *

from flask import Flask, render_template, redirect, url_for, session, request
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc

from datetime import date


@app.route('/')
def index():
    if current_user.is_authenticated and current_user.account_type != 5:
        session.clear()
        logout_user()
        return redirect(url_for('index'))
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
            if carrinho is None:
                carrinho = Carrinho(current_user.id,0.0)
                db.session.add(carrinho)
                db.session.commit()
            carrinho.LimpaCarrinho()
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template("login.html",form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=="POST":
        nome=request.form.get('nome')
        username=request.form.get('username')
        password=request.form.get('password')
        acctype=5
        db.session.add(User(nome,username,password,acctype))
        db.session.commit()
        user = User.query.filter_by(username=request.form.get('username')).first()
        login_user(user)
        return redirect(url_for('index'))
    return render_template("signup.html")

@app.route('/carrinho', methods=['GET','POST'])
@login_required
def carrinho():
    if request.method == 'POST':
        carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
        venda = Venda(current_user.id, str(date.today()), carrinho.total)
        db.session.add(venda)
        items = ItemCarrinho.query.filter_by(idCarrinho=carrinho.id).all()
        venda = Venda.query.order_by(desc("id")).filter_by(idUser=current_user.id).first()
        for item in items:
            itemvenda = ItemVenda(item.idProduto, venda.id, item.preco, item.quantidade)
            db.session.add(itemvenda)
        db.session.commit()
        carrinho.LimpaCarrinho()
        redirect(url_for('carrinho'))

    carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
    if carrinho is None:
        carrinho = Carrinho(current_user.id,0.0)
        db.session.add(carrinho)
        db.session.commit()
    items = ItemCarrinho.query.filter_by(idCarrinho=carrinho.id).all()
    for item in items:
        produto = Produto.query.filter_by(id=item.idProduto).first()
        item.nome = produto.nome
    carrinho.UpdateTotal()
    return render_template("carrinho.html", items=items, carrinho=carrinho)

@app.route('/loja0', methods=['GET','POST'])
def loja0():
    if request.method == 'POST':
        idProduto = int(request.form.get('id'))
        produto = Produto.query.filter_by(id=idProduto).first()
        carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
        item = ItemCarrinho.query.filter_by(idProduto=produto.id).first()
        if item is None:
            item = ItemCarrinho(produto.id,carrinho.id,produto.preco,1)
            db.session.add(item)
            db.session.commit()
        else:
            item.quantidade = item.quantidade + 1
            db.session.commit()
    gabinetes = Produto.query.filter_by(categoria="Gabinete").all()
    return render_template("loja0.html", gabinetes=gabinetes)

@app.route('/loja1', methods=['GET','POST'])
def loja1():
    if request.method == 'POST':
        idProduto = int(request.form.get('id'))
        produto = Produto.query.filter_by(id=idProduto).first()
        carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
        item = ItemCarrinho.query.filter_by(idProduto=produto.id).first()
        if item is None:
            item = ItemCarrinho(produto.id,carrinho.id,produto.preco,1)
            db.session.add(item)
            db.session.commit()
        else:
            item.quantidade = item.quantidade + 1
            db.session.commit()
    monitores = Produto.query.filter_by(categoria="Monitor").all()
    return render_template("loja1.html", monitores=monitores)

@app.route('/loja2', methods=['GET','POST'])
def loja2():
    if request.method == 'POST':
        idProduto = int(request.form.get('id'))
        produto = Produto.query.filter_by(id=idProduto).first()
        carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
        item = ItemCarrinho.query.filter_by(idProduto=produto.id).first()
        if item is None:
            item = ItemCarrinho(produto.id,carrinho.id,produto.preco,1)
            db.session.add(item)
            db.session.commit()
        else:
            item.quantidade = item.quantidade + 1
            db.session.commit()
    teclados = Produto.query.filter_by(categoria="Teclado").all()
    return render_template("loja2.html", teclados=teclados)

@app.route('/loja3', methods=['GET','POST'])
def loja3():
    if request.method == 'POST':
        idProduto = int(request.form.get('id'))
        produto = Produto.query.filter_by(id=idProduto).first()
        carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
        item = ItemCarrinho.query.filter_by(idProduto=produto.id).first()
        if item is None:
            item = ItemCarrinho(produto.id,carrinho.id,produto.preco,1)
            db.session.add(item)
            db.session.commit()
        else:
            item.quantidade = item.quantidade + 1
            db.session.commit()
    mouses = Produto.query.filter_by(categoria="Mouse").all()
    return render_template("loja3.html", mouses=mouses)

@app.route('/adm', methods=['GET','POST'])
def adm_index():
    '''Se o usuário não estiver autenticado leva para área de login,
    caso ele esteja leva para a home.'''

    if current_user.is_authenticated:
        if current_user.account_type == 5:
            session.clear()
            logout_user()
            return redirect(url_for('adm_index'))
        numeroProdutos = Produto.query.count()
        return render_template("adm_index.html", numeroProdutos=numeroProdutos)

    form = LoginForm()

    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('adm_index'))
        return redirect(url_for('adm_index'))
    else:
        return render_template("adm_login.html", form=form)

@app.route('/adm_produto')
@login_required
def adm_produto():
    if current_user.account_type != 1:
        return redirect(url_for('adm_index'))

    produtos = Produto.query.all()
    return render_template("adm_produto.html", produtos=produtos)

@app.route('/adm_produto_add', methods=['GET','POST'])
@login_required
def adm_produto_add():
    if current_user.account_type != 1:
        return redirect(url_for('adm_index'))

    form = ProdutoForm()
    if request.method == 'POST':
        preco = float(form.preco.data.replace(".","").replace(",","."))
        produto = Produto(form.nome.data, preco, form.estoque.data, form.categoria.data, form.descricao.data,"")
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('adm_produto'))
    else:
        return render_template("adm_produto_add.html", form=form)

@app.route('/adm_relatorio', methods=['GET','POST'])
@login_required
def adm_relatorio():
    if request.method == 'POST':
        print(request.form.get('id'))
        idVenda = int(request.form.get('id'))
        itens = ItemVenda.query.filter_by(idVenda=idVenda).all()
        for item in itens:
            produto = Produto.query.filter_by(id=item.idProduto).first()
            item.nome = produto.nome
        return render_template("adm_relatorio_detalhes.html",itens=itens)
    vendas = Venda.query.all()
    return render_template("adm_relatorio.html",vendas=vendas)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    '''Limpa a sessão do usuário e redireciona para a área de login.'''
    if current_user.account_type == 5:
        session.clear()
        logout_user()
        return redirect(url_for('index'))
    else:
        session.clear()
        logout_user()
        return redirect(url_for('adm_index'))

@app.route('/limpar')
@login_required
def limpar():
    '''Limpa o carrinho do usuário'''
    carrinho = Carrinho.query.filter_by(idUser=current_user.id).first()
    if carrinho is None:
        carrinho = Carrinho(current_user.id,0.0)
        db.session.add(carrinho)
        db.session.commit()
    carrinho.LimpaCarrinho()
    return redirect(url_for('carrinho'))