# coding = utf-8

from sqlch import app, session
from sqlch.models import MyTable
from flask import render_template, request
from werkzeug.routing import RequestRedirect


@app.route('/')
def index():
    print("Show index")
    records = session.query(MyTable).all()
    return render_template('index.html', data=records)

@app.route('/reg/', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        name = request.form['user']
        value = request.form['value']
        rec = MyTable(name, value)
        session.add(rec)
        session.commit()
        return RequestRedirect('/')
    return render_template('reg.html')

@app.route('/test/')
def test():
    return render_template('test.html')

from .forms import LoginForm
@app.route('/login/', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if request.method == 'POST' and oginForm.validate_on_submit():
        print('Enter post...')
        openid = loginForm.openid.data
        print('openid is:' + openid)
        if openid == 'kk':
            print('set error info')
            errs= ('Invalid input, KK is forbidden',)
            print('errs length %r' %(len(errs)))
            loginForm.openid.errors = errs
            print('Error data:')
            print(len(loginForm.openid.errors))

            for err in loginForm.openid.errors:
                print('err:' + err)
            print('try to render template')
            return render_template('login.html', form=loginForm)
        remember = loginForm.remember_me.data
        return render_template('showdata.html', data=(openid, remember))
    print('render the default login form')
    return render_template('login.html', form=loginForm)
        
