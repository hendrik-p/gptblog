from flask import Flask, render_template, url_for, flash, redirect
from flask_login import login_manager, login_required, login_user, current_user, logout_user, LoginManager
from flaskext.markdown import Markdown

from gptblog.config import Config
from gptblog.models import User, BlogPost, Visit, db
from gptblog.forms import BlogPostForm, LoginForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Markdown(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_user():
    current_username = None
    if current_user.is_authenticated:
        current_username = current_user.username
    return dict(current_user=current_username)

@app.route('/')
def home():
    visit = Visit().query.first()
    if not current_user.is_authenticated:
        visit.views += 1
        db.session.commit()
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/post/<int:id>')
def post(id):
    post = BlogPost.query.get_or_404(id)
    if not current_user.is_authenticated:
        post.views += 1
    db.session.commit()
    return render_template('post.html', post=post)

@app.route('/editor', methods=['GET', 'POST'])
@login_required
def editor():
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            teaser=form.teaser.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('editor.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    posts = BlogPost.query.all()
    visit = Visit.query.first()
    total_views = visit.views + sum(post.views for post in posts)
    return render_template('dashboard.html', total_views=total_views, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successfull', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

