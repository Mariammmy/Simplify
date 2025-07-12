from ext import app, db
from models import Article, Review, User, Category

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="123", role="admin")
    admin.create()

    STEM = Category(Name = "STEM", image="STEM.jpg", link="/category/STEM",
        Description = "Explore science, technology, engineering, and math with practical insights and creative problem-solving.")
    STEM.create()

    Literature = Category(Name = "Literature", image="English-Literature.jpg", link="/category/Literature",
        Description = "Dive into storytelling, analysis, and the power of words—from classics to contemporary.")
    Literature.create()