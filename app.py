import os
import sqlite3
from flask import Flask, render_template, session, render_template, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)
conn = sqlite3.connect('OEDB.db', check_same_thread=False)
cur = conn.cursor()
uid= -1

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def indexA():
    result_set = []
    if request.method == 'POST':
        price = int(request.form['price'])
        cur = conn.cursor()
        query = f"SELECT P.maker, P.model, PC.speed FROM Products P, PCs PC WHERE P.model = PC.model ORDER BY ABS(PC.price - {price}) LIMIT 1"
        for row in cur.execute(query):
            result_set.append(row)
        result = result_set[0]
        return render_template('indexA.html', result=result)
    return render_template('indexA.html', result=[])

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
   
@app.route('/signUp', methods=['POST'])
def signUp():
    result_set = []
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        pw = request.form['pw']
        query = f"""
                INSERT INTO USER(id, pw, name) VALUES('{}','{}','{}')"""
    return render_template('signUp.html')
    
@app.route('/signIn', methods=['GET','POST'])
def signIn():
    return render_template('signIn.html')

@app.route('/signOut', methods=['GET','POST'])
def signOut():
    return render_template('signOut.html')

@app.route('/userInfo', methods=['GET','POST'])
def userInfo():
    return render_template('userInfo.html')

@app.route('/searchUsers', methods=['GET','POST'])
def searchUsers():
    return render_template('searchUsers.html')

@app.route('/updateUsers', methods=['GET','POST'])
def updateUsers():
    return render_template('updateUsers.html')

@app.route('/deleteUsers', methods=['GET','POST'])
def deleteUsers():
    return render_template('deleteUsers.html')

@app.route('/myPreference', methods=['GET','POST'])
def myPreference():
    return render_template('myPreference.html')

@app.route('/addPreference', methods=['GET','POST'])
def addPreference():
    return render_template('addPreference.html')

@app.route('/deletePreference', methods=['GET','POST'])
def deletePreference():
    return render_template('deletePreference.html')

@app.route('/searchCategory', methods=['GET','POST'])# 카테고리별로 나열
def searchCategory():
    return render_template('searchCategory.html')

@app.route('/addCategory', methods=['GET','POST'])
def addCategory():
    return render_template('addCategory.html')

@app.route('/deleteCategory', methods=['GET','POST'])
def deleteCategory():
    return render_template('deleteCategory.html')

@app.route('/myCart', methods=['GET','POST'])
def myCart():
    return render_template('myCart.html')

@app.route('/addToCart', methods=['GET','POST'])
def addToCart():
    return render_template('addToCart.html')

@app.route('/updateCart', methods=['GET','POST'])
def updateCart():
    return render_template('updateCart.html')

# YHK #####

@app.route('/addOrder', methods=['GET','POST'])
def addOrder():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        pid = int(request.form['pid'])
        quantity = int(request.form['quantity'])
        orderDate = str(request.form['orderDate'])
        zipCode = str(request.form['zipCode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])

        query = f"""
                INSERT INTO Shipping (uid, pid, quantity, orderDate, zipCode, state, city, street)
                VALUES ({uid},{pid},{quantity},{orderDate},{zipCode},{state},{city},{street});
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('addOrder.html', result_set)
    return render_template('addOrder.html')
    
@app.route('/addProducer', methods=['GET','POST'])
def addProducer():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        producerid = int(request.form['producerid'])
        country = str(request.form['country'])
        brand = str(request.form['brand'])

        query = f"""
                INSERT INTO Producer (producerid, country, brand)
                VALUES ({producerid},{country},{brand});
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('addProducer.html', result_set)
    return render_template('addProducer.html')
    
@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        name = int(request.form['name'])
        price = int(request.form['price'])
        stock = int(request.form['stock'])
        pinfo = str(request.form['pinfo'])
        producerid = str(request.form['producerid'])

        query = f"""
                INSERT INTO Product (pid, name, price, stock, pinfo, producerid)
                VALUES ({name},{price},{stock},{pinfo},{producerid});
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('addProduct.html', result_set)
    return render_template('addProduct.html')
    
@app.route('/addShipping', methods=['GET','POST'])
def addShipping():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        pid = int(request.form['pid'])
        quantity = int(request.form['quantity'])
        orderDate = str(request.form['orderDate'])
        zipCode = str(request.form['zipCode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])

        query = f"""
                INSERT INTO Shipping (uid, pid, quantity, orderDate, zipCode, state, city, street)
                VALUES ({uid},{pid},{quantity},{orderDate},{zipCode},{state},{city},{street});
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('addShipping.html', result_set)
    return render_template('addShipping.html')
    
@app.route('/deleteOrder', methods=['GET','POST'])
def deleteOrder():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        orderid = int(request.form['orderid'])

        query = f"""
                DELETE FROM Order
                WHERE orderid = {orderid}
                """
        cur.execute(query)

        query = "SELECT * FROM Order"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('deleteOrder.html', result_set)
    return render_template('deleteOrder.html')
    
@app.route('/deleteProducer', methods=['GET','POST'])
def deleteProducer():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        producerid = int(request.form['producerid'])

        query = f"""
                DELETE FROM Producer
                WHERE producerid = {producerid}
                """
        cur.execute(query)

        query = "SELECT * FROM Producer"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('deleteProducer.html', result_set)
    return render_template('deleteProducer.html')
    
@app.route('/deleteProduct', methods=['GET','POST'])
def deleteProduct():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        pid = int(request.form['pid'])

        query = f"""
                DELETE FROM Product
                WHERE pid = {pid}
                """
        cur.execute(query)

        query = "SELECT * FROM Product"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('deleteProduct.html', result_set)
    return render_template('deleteProduct.html')
    
@app.route('/deleteShipping', methods=['GET','POST'])
def deleteShipping():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        shippingid = int(request.form['shippingid'])

        query = f"""
                DELETE FROM Shipping
                WHERE orderid = {shippingid}
                """
        cur.execute(query)

        query = "SELECT * FROM Shipping"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('deleteShipping.html', result_set)
    return render_template('deleteShipping.html')
    
@app.route('/searchOrder', methods=['GET','POST'])
def searchOrder():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        orderid = int(request.form['orderid'])

        query = f"""
                SELECT * FROM Shipping
                WHERE orderid = {orderid} AND uid = {uid}
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('searchOrder.html', result_set)
    return render_template('searchOrder.html')
    
@app.route('/searchProducer', methods=['GET','POST'])
def searchProducer():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        producerid = int(request.form['producerid'])

        query = f"""
                SELECT * FROM Producer
                WHERE producerid = {producerid}
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('searchProducer.html', result_set)
    return render_template('searchProducer.html')
    
@app.route('/searchProduct', methods=['GET','POST'])
def searchProduct():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        pid = int(request.form['pid'])

        query = f"""
                SELECT * FROM Product
                WHERE pid = {pid}
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('searchProduct.html', result_set)
    return render_template('searchProduct.html')
    
@app.route('/shippingHistory', methods=['GET','POST'])
def shippingHistory():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        query = f"""
                SELECT * FROM Shipping
                WHERE uid = {uid}
                """
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('shippingHistory.html', result_set)
    return render_template('shippingHistory.html')
    
@app.route('/updateOrder', methods=['GET','POST'])
def updateOrder():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        orderid = int(request.form['orderid'])
        zipcode = str(request.form['zipcode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])

        query = f"""
                UPDATE Shipping 
                SET zipcode={zipcode}, state={state}, city={city},
                    street={street}
                WHERE uid = {uid} and orderid = {orderid}
                """
        cur.execute(query)
        
        query = "SELECT * FROM Shipping WHERE uid = {uid}"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('updateOrder.html', result_set)
    return render_template('updateOrder.html')
    
@app.route('/updateProducer', methods=['GET','POST'])
def updateProducer():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        producerid = int(request.form['producerid'])
        country = str(request.form['country'])
        brand = str(request.form['brand'])

        query = f"""
                UPDATE Producer 
                SET country={country}, brand={brand}
                WHERE producerid = {producerid}
                """
        cur.execute(query)
        
        query = "SELECT * FROM Producer WHERE producerid = {producerid}"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('updateProducer.html', result_set)
    return render_template('updateProducer.html')
    
@app.route('/updateProduct', methods=['GET','POST'])
def updateProduct():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        producerid = int(request.form['producerid'])
        name = str(request.form['name'])
        price = int(request.form['price'])
        stock = int(request.form['stock'])
        pid = int(request.form['pid'])
        pinfo = str(request.form['pinfo'])

        query = f"""
                UPDATE Product 
                SET name={name}, price={price}, stock={stock}, pinfo={pinfo}
                ,producerid={producerid}
                WHERE pid = {pid}
                """
        cur.execute(query)
        
        query = "SELECT * FROM Producer WHERE producerid = {producerid}"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('updateProduct.html', result_set)
    return render_template('updateProduct.html')
    
@app.route('/updateShipping', methods=['GET','POST'])
def updateShipping():
    global uid
    if uid == -1:
        render_template("signIn.html")
    result_set = []
    if request.method == 'POST':
        shippingid = int(request.form['shippingid'])
        zipcode = str(request.form['zipcode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])

        query = f"""
                UPDATE Shipping 
                SET zipcode={zipcode}, state={state}, city={city},
                    street={street}
                WHERE uid = {uid} and orderid = {shippingid}
                """
        cur.execute(query)
        
        query = "SELECT * FROM Shipping WHERE uid = {uid}"
        for row in cur.execute(query):
            result_set.append(row)
        return render_template('updateShipping.html', result_set)
    return render_template('updateShipping.html')
    
if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True)        