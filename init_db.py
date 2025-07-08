from ext import app, db
from models import Article, Review, User, Category

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="123", role="admin")
    admin.create()