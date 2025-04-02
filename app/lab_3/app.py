from datetime import timedelta

from flask import render_template, Flask, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from .models import User
from .forms import LoginForm
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in User.users else None

@app.route('/')
def index():
    if current_user.is_authenticated:
        user_visits = session.get(current_user.id, 0) + 1
        session[current_user.id] = user_visits
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.validate(form.username.data, form.password.data):
            user = User(form.username.data)
            login_user(user, remember=form.remember.data)
            flash('Вы успешно вошли!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secrets.html')

@app.context_processor
def inject_user():
    return {'current_user': current_user}


if __name__ == '__main__':
    app.run(debug=True)

