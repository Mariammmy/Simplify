from ext import app

if __name__ == "__main__":
    from routes import home, register, profile, add_course, login, logout, category_page, article_details, delete_article, categories, admin_panel, users, feedbacks, delete_category, add_category, delete_user, unsave_article
    app.run(debug=True)
