import os
import sqlite3
from flask import Flask, render_template, _app_ctx_stack, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from initialData import initialData

#Basic Setting
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
moment = Moment(app)
DATABASE = 'sjps5.db'
conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

#inital Database Setting
initialData()

#Database connection control functions
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(DATABASE)
    return top.sqlite_db


@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

# Routers
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pc')
@app.route('/pc', methods=['POST'])
def pc():
    if request.method == 'POST':
        k = get_db().execute(
            '''SELECT maker, A.model, speed,price FROM PCs as A, Products as P
            where A.model = P.model order by ABS(A.price - ?) ASC''',
            [int(request.form['price'])])
        return render_template('pcPrice.html', data=k.fetchall())
    else:
        return render_template('pcPrice.html')


@app.route('/laptop')
@app.route('/laptop', methods=['POST'])
def labtop():
    if request.method == 'POST':
        print([request.form['speed'], request.form['ram'], request.form['hd'], request.form['screen']])
        k = get_db().execute(
            '''SELECT maker, A.model, speed, ram, hd, screen, price FROM Laptops as A, Products as P
            where A.model = P.model and speed > ? and ram > ? and hd > ? and screen > ?''',
            [int(request.form['speed']), int(request.form['ram']), int(request.form['hd']),
             int(request.form['screen'])])
        return render_template('laptop.html', data=k.fetchall())
    else:
        return render_template('laptop.html')


@app.route('/product')
@app.route('/product', methods=['POST'])
def product():
    if request.method == 'POST':
        k = get_db().execute(
            ''' SELECT maker, P.model, P.type, speed, ram, hd, Null, price, Null, Null FROM  Products as P, PCs as A
                where A.model = P.model and maker = ? UNION
                SELECT maker, P.model, P.type, speed, ram, hd, screen, price, Null, Null FROM Products as P, Laptops as B
                where B.model = P.model and maker = ? UNION
                SELECT maker, P.model, P.type, Null, Null, Null, Null, price, color, C.type
                FROM Products as P, Printers as Cwhere C.model = P.model and maker = ?''',
            [request.form['maker'], request.form['maker'], request.form['maker']])
        return render_template('product.html', data=k.fetchall())
    else:
        return render_template('product.html')


@app.route('/multi')
@app.route('/multi', methods=['POST'])
def multi():
    if request.method == 'POST':
        print([request.form['budget']])
        k = get_db().execute('''SELECT A.model, A.speed, A.ram, A.hd, A.price, B.model, B.color, B.type, B.price FROM PCs as A, Printers as B
            where (A.price+B.price) < ? and A.speed > ? order by (A.price + B.price) ASC, B.color DESC limit 1 ''',
                             [int(request.form['budget']), int(request.form['speed'])])
        return render_template('multi.html', data=k.fetchall())
    else:
        return render_template('multi.html')


@app.route('/newPc')
@app.route('/newPc', methods=['POST'])
def newPC():
    connection = get_db()
    cursor = connection.cursor()
    if request.method == 'POST':
        k = connection.execute(
            '''SELECT COUNT(*) FROM Products as P where model = ?''',
            [request.form['model']])
        if int(k.fetchall()[0][0]) > 0:
            return render_template('newPc.html', message="Warning: the model already exist")
        else:
            cursor.execute(
                '''INSERT INTO Products (maker, model, type) VALUES(?,?,?)''',
                [request.form['maker'], request.form['model'], 'PC'])
            cursor.execute(
                '''INSERT INTO PCs (model, speed, ram, hd, price) VALUES(?,?,?,?,?)''',
                [request.form['model'], request.form['speed'], request.form['ram'], request.form['hd'],
                 request.form['price']])
            connection.commit()
            cursor.close()
            return render_template('newPc.html', message="Successfully Inserted")
    else:
        return render_template('newPc.html')

#Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#Debug Mode
if __name__ == '__main__':
    app.run(debug=True)  # Debug mode will reload files when changed.
    # app.run(host='0.0.0.0')  # To make the server listen on all public IPs.
