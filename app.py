import os
import sqlite3
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)
conn = sqlite3.connect('JHps5.db', check_same_thread=False)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def problemA():
    result_set = []
    if request.method == 'POST':
        price = int(request.form['price'])
        cur = conn.cursor()
        query = f"SELECT P.maker, P.model, PC.speed FROM Products P, PCs PC WHERE P.model = PC.model ORDER BY ABS(PC.price - {price}) LIMIT 1"
        for row in cur.execute(query):
            result_set.append(row)
        result = result_set[0]
        return render_template('problemA.html', result=result)
    return render_template('problemA.html', result=[])

@app.route('/b', methods=['GET', 'POST'])
def problemB():
    result_set = []
    if request.method == 'POST':
        speed = float(request.form['speed'])
        ram = int(request.form['ram'])
        hd = int(request.form['hd'])
        screen = int(request.form['screen'])

        cur = conn.cursor()
        query = f"""
                SELECT L.model, L.speed, L.ram, L.hd, L.screen, L.price, P.maker
                FROM Laptops L, Products P
                WHERE P.model = L.model AND L.speed >= {speed} AND L.ram >= {ram} AND L.hd >= {hd} AND L.screen >= {screen}"""
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('problemB.html', result=result_set)
    return render_template('problemB.html', result=[])


@app.route('/c', methods=['GET', 'POST'])
def peoblemC():
    result_set = []
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']

        cur = conn.cursor()
        query = f"""
                SELECT pc.model, p.maker, p.type, price, speed, ram, hd, NULL AS color
                FROM Products p NATURAL JOIN PCs pc WHERE maker = '{manufacturer}' 
                UNION 
                SELECT Printers.model,p.maker, p.type, price, color, Printers.type, NULL AS hd, NULL AS screen
                FROM Products p JOIN Printers 
                WHERE maker = '{manufacturer}' AND p.model = Printers.model    
                UNION
                SELECT laptop.model, p.maker,p.type, price, speed, ram, hd, screen
                FROM Products p NATURAL JOIN Laptops laptop WHERE maker = '{manufacturer}'

                """
        # SELECT pc.model, p.type, pc.price, pc.speed, pc.ram, pc.hd, NULL AS color
        #         FROM Products p,  PCs pc WHERE p.maker = '{manufacturer}' AND p.model = pc.model
        #         UNION 
        #         SELECT Printers.model, p.type, Printers.price, Printers.color, Printers.type, NULL AS hd, NULL AS screen
        #         FROM Products p, Printers 
        #         WHERE p.maker = '{manufacturer}' AND p.model = Printers.model    
        #         UNION
        #         SELECT p.model, p.type, l.price, l.speed, l.ram, l.hd, l.screen
        #         FROM Products p, Laptops l 
        #         WHERE p.maker = '{manufacturer} AND p.model = l.model'
        
        for row in cur.execute(query):
            result_set.append(row)
        
        return render_template('problemC.html', result=result_set)
    return render_template('problemC.html', result=[])

@app.route('/d', methods=['GET', 'POST'])
def problemD():
    result_set1 = []
    result_set2 = []
    if request.method == 'POST':
        budget = int(request.form['budget'])
        speed = float(request.form['speed'])

        cur = conn.cursor()
        query = f"""
                SELECT pc.model, pr.model , (pc.price + pr.price) AS total
                FROM Pcs pc, Printers pr
                WHERE (pc.price + pr.price) < {budget} AND pc.speed >= {speed}
                ORDER BY (pc.price + pr.price)"""
        for row in cur.execute(query):
            result_set1.append(row)
        
        query = f"""
                SELECT pc.model, pr.model, (pc.price + pr.price) AS total
                FROM Pcs pc, Printers pr
                WHERE (pc.price + pr.price) < {budget} AND pc.speed >= {speed} AND pr.color = 'True'
                ORDER BY (pc.price + pr.price)"""
        for row in cur.execute(query):
            result_set2.append(row)
        
        if result_set2[0][2] == result_set1[0][2]:
            result = result_set2[0]
        return render_template('problemD.html', result=result)
    return render_template('problemD.html', result=[])
    

@app.route('/e', methods=['GET', 'POST'])
def peoblemE():
    result_set = []
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']
        modelNum = int(request.form['modelNum'])
        speed = float(request.form['speed'])
        ram = int(request.form['ram'])
        hdSize = int(request.form['hdSize'])
        price = int(request.form['price'])

        cur = conn.cursor()
        # Check model number exists in the db
        query = f"""
                SELECT *
                FROM Products
                WHERE Products.model = {modelNum}"""
        for row in cur.execute(query):
            result_set.append(row)
        #If there is product has same model number display warning
        if len(result_set) > 0:
            return render_template('problemE.html', result = "Warning! Model Number Already Exists!")
        #IF not insert query
        else:  
            query = f"""INSERT INTO Products VALUES ('{manufacturer}',{modelNum},'PC')"""
            cur.execute(query)
            query = f"INSERT INTO PCs VALUES ({modelNum},{speed},{ram},{hdSize},{price})"
            cur.execute(query)
            conn.commit()
            return render_template('problemE.html', result="INSERT SUCCESS!")
    return render_template('problemE.html', result="")
   
if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True)        