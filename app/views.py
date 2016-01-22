#!/usr/bin/env python
import sys
import os
from app import app, manager, savvy_collection, db, client
from app.Forms.rego import regoForm
from app.Forms.login import loginForm
from app.Forms.recover import recoverForm
from app.Forms.account import employerForm, candidateForm
from app.Models.User import User
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash
from flask.ext.login import login_user, logout_user, login_required, current_user

# Define the template directory
tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'

# Setup the template enviroment
env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)

###############################################################################
# Login Manager
###############################################################################
@manager.user_loader
def load_user(username):
    if username != None:
        user = savvy_collection.find_one({ "username": username })
        if not user:
            return None
    else:
        return None
    return User(user)

###############################################################################
# Supporting function
###############################################################################
@app.errorhandler(404)
def not_found(error):
    return render('404.html', 404)

def render(page, form=None, error=None):
    if error:
        return render_template(page,
                               user_logged_in = current_user.is_authenticated,
                               user = current_user.get_id()), error
    else:
        return render_template(page,
                               user_logged_in = current_user.is_authenticated,
                               user = current_user.get_id(),
                               form = form)

###############################################################################
# VIEWS/PAGES
###############################################################################
@app.route('/')
def home():
    return render('home.html')

@app.route('/test/<x>')
@login_required
def test(x):
    return render('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    # Case: user submits form
    form = loginForm(request.form)
    if request.method == 'POST' and form.validate():
        if request.form.get('next') != None and request.form.get('next') != 'None':
            return redirect(request.form.get('next'))
        else:
            return redirect(url_for('home'))

    # Case: user needs to log in
    return render('login.html', form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#testing link http://127.0.0.1:5000/activate/weizteoh/b740538122a3bbcbece1467773034373
@app.route('/activate/<username>/<token>')
def activate(username, token):
    if User.validate_rego_token(username, token):
        login_user(User(username))
        return redirect(url_for('account', account = username))
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    form = regoForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('account'))

    return render('register.html', form)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    username = current_user.get_id()['username']
    user = savvy_collection.find_one({ "username": username })
    if user:
        form = None
        if user.get('category', '').lower() == 'employer':
            form = employerForm(username, request.form)
        elif user.get('category', '').lower() == 'candidate':
            form = candidateForm(username, request.form)

        if request.method == 'GET':
            form.prepopulate(user)

        if request.method == 'POST':
            if form.validate(user):
                flash('Successfully updated your profile', 'success')
            else:
                flash('Failed to update your profile', 'error')

        return render('account.html', form)
    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    form = recoverForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('login'))
    return render('recover.html', form=form)
