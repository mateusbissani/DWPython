# Aqui vai a estrutura do nosso banco de dados (classes e tals)
from src import database
from datetime import datetime
from src import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.Relationship("Posts", backref='user', lazy=True)


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow()) # Data de criação do post.
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def user_likes(self, user):
        # Verifica se o usuário deu like neste post.
        like = Like.query.filter_by(user_id=user.id, post_id=self.id).first()
        return like is not None # Retorna true se um Like for encontrado ou false se nenhum Like for encontrado.

class Like(database.Model): # Classe de Like do banco de dados
    __table_args__ = {'extend_existing': True} # Config para atualizar a tabela.
    id = database.Column(database.Integer, primary_key=True) # Id para identificar o Like
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False) # A id do usuario que deu Like
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False) # O id do post que foi dado Like