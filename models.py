from ext import db, login_manager
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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

user_article_library = db.Table('user_article_library',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'))
)

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
    Subheading5= db.Column(db.String(),  default="")
    text5 = db.Column(db.String(),  default="")
    image = db.Column(db.String(), default="defaul_photo.jpg")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    


class Category(db.Model, BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(), nullable=False)
    Description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    Link = db.Column(db.String(), nullable=False)



class Feedback(db.Model, BaseModel):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    headline = db.Column(db.String(), nullable=False)
    message = db.Column(db.Text(), nullable=False)


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String())
    role = db.Column(db.String())
    profile_pic = db.Column(db.String(), default="logo.jpg")

    saved_articles = db.relationship(
    'Article',
    secondary=user_article_library,
    backref='saved_by_users'
    )

    def __init__(self, username, password, profile_pic="logo.jpg", role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.profile_pic = profile_pic
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)