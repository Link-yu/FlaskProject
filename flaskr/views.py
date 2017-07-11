from flaskr import app
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flaskr import app, db, lm, oid
from .models import User
#index view function suppressed for brevity
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('/index'))
    form = LoginForm()
    if form.validate_on_submit():
        seesion['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['name','email'])
    return render_template('login.html',
        title = 'Sigin In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'name':'yupaopao'}
    posts = [
        {
            'author': {'name':'john'},
            'body':'Beautiful day in Portland!'
        },
        {
            'author':{'name':'Susan'},
            'body':'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",title = 'Home', user = user, posts = posts)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login.Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        name = resp.name
        if name is None or name == "":
            name = resp.email.split('@')[0]
        user = User(name=name, email = resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = seesion['remember_me']
        seesion.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user