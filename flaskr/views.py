from flaskr import app
from flask import render_template, flash, redirect
from .forms import LoginForm

#index view function suppressed for brevity
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' +str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sigin In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/')
@app.route('/index')
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
