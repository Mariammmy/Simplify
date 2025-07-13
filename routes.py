from flask import render_template, redirect, flash, url_for
from ext import app, db, login_manager
from forms import RegisterForm, AddForm, LoginForm, CategoryForm, FeedbackForm
from os import path
from models import Article, User, Category, Feedback
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps
from sqlalchemy.sql.expression import func


login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You must be logged in to access this page", "warning")
    return redirect(url_for('login'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            flash("You don't have permission to access this page", "danger")
            return redirect("/")  

        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    article_list = Article.query.order_by(func.random()).limit(6).all()
    return render_template("index.html", article_list=article_list)

@app.route("/sign-up", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
@app.route("/registeruser", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        image = form.profile_image.data
        image.save(f"static/images/{image.filename}")
        new_user = User(username=form.username.data, password=form.password.data, profile_pic=image.filename)
        new_user.create()
        login_user(new_user)
        flash("Signed up successfully", "success")
        return redirect("/")
    return render_template("reg.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.username.data == User.username).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect("/")
        else:
            form.username.errors.append("Invalid username or password")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route('/profile')
@login_required
def profile():
    user = current_user 
    return render_template('profile.html', user=user)

@app.route('/admin_panel')
@login_required
@admin_required
def admin_panel():
    user = current_user 
    return render_template("admin/admin.html", user=user)

@app.route('/users')
@login_required
@admin_required
def users():
    user_list = User.query.all()
    return render_template("admin/users.html", user_list=user_list)

@app.route('/feedbacks')
@login_required
@admin_required
def feedbacks():
    feedbacks = Feedback.query.all()
    return render_template("admin/feedbacks.html", feedbacks=feedbacks)

@app.route('/category')
def categories():
    category_list = Category.query.all()

    return render_template("categories.html", category_list = category_list)

@app.route('/category/add_category', methods=["GET", "POST"])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(Name=form.name.data, Description=form.description.data, Link=form.link.data)
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_category.image = image.filename
        Category.create(new_category)

        return redirect("/category")
    return render_template("add_category.html", form=form)

@app.route('/category/<category_name>/delete/<int:category_id>')
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    Category.delete(category)

    return redirect("/category")


@app.route("/category/<category_name>/edit_category/<int:category_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_category(category_id, category_name):
    category = Category.query.get(category_id)
    form = CategoryForm(name=category.Name, description=category.Description, link=category.Link)
    
    if form.validate_on_submit():
        category.Name = form.name.data
        category.Description = form.description.data
        category.Link = form.link.data
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        category.image = image.filename

        image = form.image.data
        if image and image.filename: 
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            category.image = image.filename  

        db.session.commit()
        return redirect("/")
    return render_template("add_category.html", form=form, category=category_name)


@app.route('/category/<category_name>')
def category_page(category_name):
    category_list = Category.query.filter_by(Name=category_name).all()
    article_list = Article.query.filter_by(category=category_name).all()
    return render_template('category.html', article_list=article_list, category_list=category_list)

@app.route("/category/<category_name>/<int:article_id>")
def article_details(article_id, category_name):
    article = Article.query.get(article_id)

    return render_template("article.html", article=article)

@app.route("/category/<category_name>/add-course", methods=["GET", "POST"]) 
@login_required
@admin_required
def add_course(category_name):
    form = AddForm()
    if form.validate_on_submit():
        new_article = Article(heading=form.heading.data, summary=form.summary.data, category=form.category.data, description=form.description.data,
                              Subheading1=form.subheading1.data, Subheading2=form.subheading2.data,
                              Subheading3=form.subheading3.data, Subheading4 = form.subheading4.data, Subheading5 = form.subheading5.data, 
                              text1 = form.text1.data, text2 = form.text2.data, text3 = form.text3.data, text4 = form.text4.data, text5 = form.text5.data)
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_article.image = image.filename
        Article.create(new_article)

        return redirect("/")
    return render_template("add.html", form=form, category=category_name)

@app.route("/category/<category_name>/delete_article/<int:article_id>")
@login_required
@admin_required
def delete_article(article_id, category_name):
    article = Article.query.get(article_id)
    Article.delete(article)

    return redirect("/")

@app.route("/category/<category_name>/edit_article/<int:article_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_article(article_id, category_name):
    article = Article.query.get(article_id)
    form = AddForm(heading=article.heading, summary=article.summary, category=article.category, description=article.description, subheading1=article.Subheading1, subheading2=article.Subheading2, subheading3=article.Subheading3,
                    subheading4 = article.Subheading4, subheading5 = article.Subheading5, text1 = article.text1, text2 = article.text2,
                    text3 = article.text3, text4 = article.text4, text5 = article.text5)
    
    if form.validate_on_submit():
        article.name = form.name.data
        article.release_year = form.release_year.data

        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        article.image = image.filename

        image = form.image.data
        if image and image.filename: 
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            article.image = image.filename 

        db.session.commit()
        return redirect("/")
    return render_template("add.html", form=form, category=category_name)

@app.route("/feedback", methods=['POST', 'GET'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback( user_id=current_user.id, headline = form.headline.data, message = form.message.data)
        Feedback.create(new_feedback)
        flash ("Feedback sent successfully!", "success")
        return redirect("/")
    return render_template("feedback.html", form=form)

@app.route("/save_article/<int:article_id>")
@login_required
def save_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article not in current_user.saved_articles:
        current_user.saved_articles.append(article)
        db.session.commit()
        flash("Saved to your library", "success")
    else:
        flash("Already saved", "info")
    return redirect(url_for('article_details', category_name=article.category, article_id=article.id))

@app.route("/unsave_article/<int:article_id>")
@login_required
def unsave_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article in current_user.saved_articles:
        current_user.saved_articles.remove(article)
        db.session.commit()
        flash("Article removed from your library", "success")
    return redirect("/library")

@app.route("/delete_user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found", "warning")
        return redirect("/admin")
    if user.id == current_user.id:
        flash("You can't delete yourself", "danger")
        return redirect("/users")
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully", "success")
    return redirect("/users") 

    
@app.route("/library")
@login_required
def library():
    articles = current_user.saved_articles
    return render_template("library.html", articles=articles)