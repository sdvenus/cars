
from loginform import LoginForm
from formsignup import RegistrationForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.name.data
            last_name =  form.last_name.data
            email = form.email.data
            password = form.password.data
            print(email, password)
            existing_user = User.query.filter_by(email=email).first()
            # If user already exists show error message and don't save to database
            if existing_user:
                flash('User already exists', 'User-exists')
                return redirect(url_for('auth.signup'))
            user = User(first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            print(user)
            print(password)
            db.session.add(user)
            db.session.commit()
            print(f'Thank you for joining us! {first_name} {last_name}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = LoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            logged_user = User(email=email, password=password) 
            print(logged_user)
            if logged_user:
                if logged_user.check_password(password):
                    print(logged_user)
                    login_user(logged_user)
                    print('You were successful in your initiation. Congratulations, and welcome to Ben Enterprises', 'auth-success')
                    return redirect(url_for('site.profile'))
                else:
                    flash('Incorrect password.', 'auth-failed')
            else:
                flash('No user found with this email address.', 'auth-failed')

    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))