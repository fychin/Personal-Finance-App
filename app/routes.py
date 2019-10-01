from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Account
from app.forms import LoginForm, RegistrationForm, EditAccountForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    accounts = Account.query.all()
    return render_template('index.html', title='Home', accounts=accounts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect authenticated user to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Validate password on post
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # Handle after login redirection
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.commit()
        flash('{} is now a registered user'.format(user.username))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    accounts = Account.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, accounts=accounts)


@app.route('/account/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    account = Account.query.filter_by(id=id).first_or_404()
    form = EditAccountForm()
    form.id.data = account.id
    form.user_id.data = current_user.id
    if form.validate_on_submit():
        form.populate_obj(account)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.name.data = account.name
        form.balance.data = account.balance
    return render_template('edit_account.html', title='Edit Account',
    form=form)
