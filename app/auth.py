from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from python_usernames import is_safe_username
from app.models import Users
from app import db
from app.forms import LoginForm, RegistrationForm


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()

        if not user:
            flash(u'Usuário não cadastrado', 'danger')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash(u'A senha está incorreta', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)

        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    if form.validate_on_submit():
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        email_exists = Users.query.filter_by(email=email).first()
        username_exists = Users.query.filter_by(username=username).first()
        safe_username = is_safe_username(username, blacklist=None)

        def email_validate(email):
            try:
                validate_email(email)
                return True
            except EmailNotValidError:
                return False

        if email_exists:
            flash('E-mail já cadastrado')
            return redirect(url_for('auth.signup'))

        if not email_validate(email):
            flash('E-mail inválido')
            return redirect(url_for('auth.signup'))

        if username_exists:
            flash('Nome de usuário já cadastrado')
            return redirect(url_for('auth.signup'))

        if not safe_username:
            flash('Nome de usuário inválido')
            return redirect(url_for('auth.signup'))

        if len(username) < 3 or len(username) > 32:
            flash('O nome de usuário deve conter entre 3 e 32 caracteres')
            return redirect(url_for('auth.signup'))

        new_user = Users(
            name=name,
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(new_user)
        db.session.commit()

        flash(u'Perfil criado com sucesso 😊', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
