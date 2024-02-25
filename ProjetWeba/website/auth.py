from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Connection réussi!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('mot de passe incorrect, réessayer.', category='error')
        else:
            flash('ce mail n\'existe pas.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Ce mail exist déja.', category='error')
        elif len(email) < 4:
            flash('mail doit etre plus long.', category='error')
        elif len(first_name) < 2:
            flash('le prenom doit être plus long.', category='error')
        elif password1 != password2:
            flash('les mots de passe ne correspondent pas', category='error')
        elif len(password1) < 7:
            flash('mot de passe doit être plus long', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Votre compte a été créé!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

