from ext import db, login_manager
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class Article(db.Model, BaseModel):
    __tablename__ = "articles"

    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(), nullable=False)  
    heading = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    Subheading1 = db.Column(db.String(), nullable=False)
    text1 = db.Column(db.String(), nullable=False)
    Subheading2 = db.Column(db.String(), nullable=False)
    text2 = db.Column(db.String(), nullable=False)    
    Subheading3 = db.Column(db.String(), nullable=False)
    text3 = db.Column(db.String(), nullable=False)    
    Subheading4 = db.Column(db.String(), nullable=False)
    text4 = db.Column(db.String(), nullable=False)    
    Subheading5= db.Column(db.String(), nullable=False)
    text5 = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), default="defaul_photo.jpg")

class Category(db.Model, BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(), nullable=False)
    Description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    Link = db.Column(db.String(), nullable=False)


class Review(db.Model, BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    movie_id = db.Column(ForeignKey("articles.id"))

class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)