#coding = utf-8

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
