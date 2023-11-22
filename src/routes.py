# Aqui vão as rotas e os links
from src import app
from flask import render_template, url_for, redirect, request, jsonify, flash
from flask_login import login_required, login_user, current_user, logout_user
from src.models import load_user, Posts, Like
from src.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost
from src import bcrypt
from src.models import User
from src import database
from datetime import datetime

import os
from werkzeug.utils import secure_filename

def format_post_date(timestamp):
    # Supondo que timestamp seja um objeto datetime
    return timestamp.strftime("%d/%m/%y")

app.jinja_env.globals.update(format_post_date=format_post_date)

# @app.route('/home')
@app.route('/home')
def homepage():
    # _formLogin = FormLogin()

    _formCreateNewAccount = FormCreateNewAccount()
    posts = Posts.query.all()

    # if _formLogin.validate_on_submit():
    #     email = _formLogin.email.data
    #     password = _formLogin.password.data
    #     user = User.query.filter_by(email=email).first()
    #
    #     if user:
    #         if bcrypt.check_password_hash(user.password, password):
    #             login_user(user, remember=True)
    #
    #             return redirect(url_for('profile', user_id=user.id))
    #     else:
    #         print('Falha na autenticação. Verifique seu e-mail e senha.')

    return render_template('home.html', posts=posts, form=_formCreateNewAccount)


@app.route('/cadastro', methods=['POST', 'GET'])
def createAccount():
    _formCreateNewAccount = FormCreateNewAccount()

    if _formCreateNewAccount.validate_on_submit():
        password = _formCreateNewAccount.password.data

        password_cr = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(password)
        # print(password_cr)

        newUser = User(
            username=_formCreateNewAccount.username.data,
            email=_formCreateNewAccount.email.data,
            password=password_cr
        )

        database.session.add(newUser)
        database.session.commit()

        login_user(newUser, remember=True)
        return redirect(url_for('profile', user_id=newUser.id))

    return render_template('cadastro.html', form=_formCreateNewAccount)


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/', methods=['POST', 'GET'])
def login():
    _formLogin = FormLogin()

    if _formLogin.validate_on_submit():
        email = _formLogin.email.data
        password = _formLogin.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=True)

                return redirect(url_for('profile', user_id=user.id))
        else:
            print('Falha na autenticação. Verifique seu e-mail e senha.')

    return render_template('login.html', form=_formLogin)


@app.route('/profile/<user_id>', methods = ['POST', 'GET'])  # /<batata>')
@login_required
def profile(user_id):  # , batata):
    # if request.method == 'POST':
    #     if 'logout' in request.form:
    #         logout_user()
    #         return redirect(url_for('homepage'))

    if int(user_id) == int(current_user.id):
        _formCreateNewPost = FormCreateNewPost()

        if _formCreateNewPost.validate_on_submit():
            photo_file = _formCreateNewPost.photo.data
            photo_name = secure_filename(photo_file.filename)

            photo_path = f'{os.path.abspath(os.path.dirname(__file__))}/{app.config["UPLOAD_FOLDER"]}/{photo_name}'
            photo_file.save(photo_path)

            _postText = _formCreateNewPost.text.data
            newPost = Posts(post_text=_postText, post_img=photo_name, user_id=int(current_user.id), creation_date=datetime.utcnow())
            database.session.add(newPost)
            database.session.commit()

        post_count = Posts.query.filter_by(user_id=current_user.id).count()

        return render_template('profile.html', user=current_user, form=_formCreateNewPost, post_count=post_count, format_post_date=format_post_date)
    else:
        _user = User.query.get(int(user_id))
        post_count = Posts.query.filter_by(user_id=_user.id).count()
        return render_template('profile.html', user=_user, form=None, post_count=post_count)  # , mesa=batata)


@app.route('/logout', methods=['POST']) # Rota POST para deslogar usuario
def logout():
    logout_user() # Função fornecida pelo Flask Login para fazer logout do usuario.
    return redirect(url_for('login')) # Retorna para homepage

@app.route('/like/<int:post_id>', methods=['POST']) # Rota estabelecida para dar like em um post (recebendo seu id) e fazendo req POST
@login_required # Usuario deve estar logado para poder dar like!
def like(post_id): # Passando o id do post que quer dar like
    post = Posts.query.get(post_id) # Pegando o Post do banco.
    if post: # Checa se o post existe, caso exista continua...
        like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first() # Verifica se o usuario ja deu like
        if like:
            # O usuário já deu like, então remova o like
            database.session.delete(like)
            database.session.commit()
        else:
            # O usuário ainda não deu like, então crie um novo like
            new_like = Like(user_id=current_user.id, post_id=post.id)
            database.session.add(new_like)
            database.session.commit()

            # Retorna para a HomePage.
    return redirect(url_for('homepage'))


@app.route('/delete_post/<int:post_id>', methods=['POST']) # Rota para realizar o 'POST' de deletar um 'post'
@login_required # Necessario usuario estar logado
def delete_post(post_id):   # Função passando o id do post que quer deletar
    post = Posts.query.get_or_404(post_id)  # Achando o post ou retornando erro.

    # Verifique se o usuário atual é o criador do post
    if current_user.id == post.user_id:
        database.session.delete(post)   # Deletando do banco de dados
        database.session.commit()   # Commitando a mudança
        flash('Post excluído com sucesso!', 'success') # Utilizando flash para mostrar mensagem de sucesso no delete
    else:
        flash('Você não tem permissão para excluir este post.', 'danger')

    return redirect(url_for('profile', user_id=current_user.id)) # Redireciona para a pagina de perfil do usuario.