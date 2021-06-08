import os
import sqlite3
from sqlite3.dbapi2 import IntegrityError
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
###카트에 담긴 물건 바로 주문 
###
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "ABCD"
bootstrap = Bootstrap(app)
moment = Moment(app)
conn = sqlite3.connect('OEDB.db', check_same_thread=False)
cur = conn.cursor()

uid = -1

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signUp', methods=['GET','POST'])
def signUp():
    resultSet = []
    try:
        if request.method == 'POST':
            name = request.form['name']
            id = request.form['id']
            pw = request.form['pw']
            zip = request.form['zip']
            state = request.form['state']
            city = request.form['city']
            street = request.form['street']
            query = f"""
                    INSERT INTO User(id, pw, name) VALUES("{id}","{pw}","{name}")"""
            cur.execute(query)
            conn.commit()

            query = f"""
                    SELECT uid FROM User WHERE id = "{id}"
            
            """
            for row in cur.execute(query):
                resultSet.append(row)
            uid = resultSet[0][0]
            query = f"""
                    INSERT INTO Address VALUES("{uid}","{zip}","{state}","{city}","{street}")
                    """
            cur.execute(query)
            conn.commit()
            flash("Sign up Complete")
            return render_template('signUp.html',result= name)
    except IntegrityError:
        flash("ID is already taken")
        return render_template('signUp.html', result = "")
    return render_template('signUp.html', result = "")
    
@app.route('/signIn', methods=['GET','POST'])
def signIn():
    global uid 
    resultset = []
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        query = f"""
                SELECT uid from User WHERE id = '{id}' AND pw = '{pw}'"""
        
        for row in cur.execute(query):
            resultset.append(row)
        if len(resultset) < 1:
            return render_template('signIn.html',result = "You are not Registered!")
        else:
            
            uid = resultset[0][0]
            flash("login success!")
    return render_template('signIn.html',result = "")

@app.route('/signOut', methods=['GET','POST'])
def signOut():
    global uid
    uid = -1
    return render_template('signIn.html',result = "Successfully Logged Out!")

@app.route('/userInfo', methods=['GET','POST'])
def userInfo():
    global uid
    resultSet = []
    
    if uid == -1:
        return render_template('signIn.html')
    else:
        query = f"""
                SELECT U.name, U.id, U.pw, A.zip, A.state, A.city, A.street from User U, Address A 
                where U.uid = {uid} AND U.uid = A.uid
                """
        for row in cur.execute(query):
            resultSet.append(row)
        print(resultSet)
        if len(resultSet) > 0:
        
            return render_template('userInfo.html', result = resultSet[0])
    return render_template('userInfo.html', result= [])

@app.route('/searchUsers', methods=['GET','POST'])
def searchUsers(): # primary key checking
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        id = request.form['id']
        query = f"""
                SELECT * from User where id = "{id}" """
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('searchUsers.html', result = resultSet)            
    else:
        query = f"""
                SELECT * from User"""
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('searchUsers.html', result = resultSet)
    

    

@app.route('/updateUsers', methods=['GET','POST'])
def updateUsers():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        userId = request.form['userId']
        name = request.form['name']
        id = request.form['id']
        pw = request.form['pw'] 

        query = f"""
                UPDATE User SET name = "{name}", id = "{id}", pw = "{pw}"
                WHERE uid = {userId}"""
        cur.execute(query)
        conn.commit()
        flash("User Update Success!")
    return render_template('updateUsers.html')

@app.route('/deleteUsers', methods=['GET','POST'])
def deleteUsers():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        userId = request.form['userId']

        query = f"""
                DELETE FROM User
                WHERE uid = {userId}"""
        cur.execute(query)
        conn.commit()
        flash("Delete Complete!")
    return render_template('deleteUsers.html')

@app.route('/myPreference', methods=['GET','POST'])
def myPreference():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    else :
        query = f"""
                SELECT CategoryPreferencecol FROM CategoryPreference
                WHERE uid = {uid}"""
        for row in cur.execute(query):
            resultSet.append(row)
        
        return render_template('myPreference.html', result = resultSet)
    

@app.route('/addPreference', methods=['GET','POST'])
def addPreference():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        category = request.form["category"]
        query = f"""
                INSERT INTO CategoryPreference
                VALUES ({uid}, '{category}')"""
        
        cur.execute(query)
        conn.commit()
        flash("Category Insert Complete!")
        

    return render_template('addPreference.html')

@app.route('/deletePreference', methods=['GET','POST'])
def deletePreference():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        category = request.form["category"]
        query = f"""
                DELETE FROM CategoryPreference
                WHERE uid = {uid} AND CategoryPreferencecol = "{category}" """
        cur.execute(query)
        conn.commit()
        flash("Preference Delete Complete!")
    return render_template('deletePreference.html')
    # else:
    #     query = f"""
    #             SELECT CategoryPreferencecol FROM CategoryPreference
    #             WHERE uid = {uid}"""
    #     for row in cur.execute(query):
    #         resultSet.append(row)
    #     return render_template('deletePreference.html', result = resultSet)
    

@app.route('/searchCategory', methods=['GET','POST'])# 카테고리별로 나열
def searchCategory():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    else:
        product = request.form["product"]
        query = f"""
                SELECT DISTINCT P.pid, name, category FROM ProductCategory P , Product D 
                WHERE P.pid = D.pid AND P.name = "{product}"
                """
        for row in cur.execute(query):
            resultSet.append(row)    
        return render_template('searchCategory.html', result = resultSet)

@app.route('/addCategory', methods=['GET','POST'])
def addCategory():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        pid = request.form['pid']
        category = request.form["category"]

        query = f"""
                INSERT INTO ProductCategory
                VALUES ({pid}, '{category}')
                """
        cur.execute(query)
        conn.commit()
        flash("Category addition Complete!")
    return render_template('addCategory.html')

@app.route('/deleteCategory', methods=['GET','POST'])
def deleteCategory():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        pid = request.form['pid']
        category = request.form["category"]
        query = f"""
                DELETE FROM ProductCategory
                WHERE (pid = {pid}, category = '{category}')
                """
        cur.execute(query)
        conn.commit()
        flash("Category Deletion Complete!")
    return render_template('deleteCategory.html')

@app.route('/myCart', methods=['GET','POST'])
def myCart():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    else:
        query = f"""
                SELECT DISTINCT C.pid, P.name, C.quantity, C.date FROM Cart C, Product P
                WHERE  P.pid = C.pid AND C.uid = {uid}
                """
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('myCart.html', result = resultSet)

@app.route('/addToCart', methods=['GET','POST'])
def addToCart():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':       
        pid = request.form["pid"]
        quantity = int(request.form["quantity"])
        query = f"""
                INSERT INTO Cart VALUES(pid = {pid}, quantity = {quantity})
                """
        cur.execute(query)
        conn.commit()
        flash("Cart Insertion Complete!")    
    return render_template('addToCart.html')

@app.route('/updateCart', methods=['GET','POST'])
def updateCart(): #quantity 추가
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        pid = request.form["pid"]
        quantity = int(request.form["quantity"])
        query = f"""
                UPDATE INTO Cart VALUES(uid = {uid}, pid = {pid}, quantity = {quantity})
                """
    return render_template('updateCart.html')

# YHK #####
@app.route('/addOrder', methods=['GET','POST'])
def addOrder():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':       
        pid = int(request.form['pid'])
        quantity = int(request.form['quantity'])
        orderDate = str(request.form['orderDate'])
        zipCode = str(request.form['zipCode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])
        
        query = f"""
                INSERT INTO Shipping (uid, pid, quantity, orderDate, zipCode, state, city, street)
                VALUES ({uid},{pid},{quantity},'{orderDate}','{zipCode}','{state}','{city}','{street}');
                                """
        cur.execute(query)
        conn.commit()
        flash("Order Insertion Complete!")    
    return render_template('addOrder.html')


@app.route('/addProducer', methods=['GET','POST'])
def addProducer():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':       
        producerid = int(request.form['producerid'])
        country = str(request.form['country'])
        brand = str(request.form['brand'])

        query = f"""
                INSERT INTO Producer (producerid, country, brand)
                VALUES ({producerid},'{country}','{brand}');
                """
        cur.execute(query)
        conn.commit()
        flash("Producer Insertion Complete!")    
    return render_template('addProducer.html')
    
@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':       
        name = str(request.form['name'])
        price = int(request.form['price'])
        stock = int(request.form['stock'])
        pinfo = str(request.form['pinfo'])
        producerid = str(request.form['producerid'])

        query = f"""
                INSERT INTO Product (name, price, stock, pinfo, producerid)
                VALUES ('{name}',{price},{stock},'{pinfo}','{producerid}');
                """
        cur.execute(query)
        conn.commit()
        flash("Product Insertion Complete!") 
    return render_template('addProduct.html')
    
@app.route('/addShipping', methods=['GET','POST'])
def addShipping():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':       
        pid = int(request.form['pid'])
        quantity = int(request.form['quantity'])
        orderDate = str(request.form['orderDate'])
        zipCode = str(request.form['zipCode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])
        
        query = f"""
                INSERT INTO Shipping (uid, pid, quantity, orderDate, zipCode, state, city, street)
                VALUES ({uid},{pid},{quantity},'{orderDate}','{zipCode}','{state}','{city}','{street}');
                                """
        cur.execute(query)
        conn.commit()
        flash("Shipping Insertion Complete!")    
    return render_template('addShipping.html')
    
@app.route('/deleteOrder', methods=['GET','POST'])
def deleteOrder():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        orderid = int(request.form['orderid'])
        query = f"""
                DELETE FROM Shipping
                WHERE (orderid = {orderid});
                """
        cur.execute(query)
        conn.commit()
        flash("Order Deletion Complete!")
    return render_template('deleteOrder.html')
    
@app.route('/deleteProducer', methods=['GET','POST'])
def deleteProducer():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        producerid = int(request.form['producerid'])

        query = f"""
                DELETE FROM Producer
                WHERE producerid = {producerid}
                """
        cur.execute(query)
        flash("Producer Deletion Complete!")
    return render_template('deleteProducer.html')
    
@app.route('/deleteProduct', methods=['GET','POST'])
def deleteProduct():
    global uid
    if uid == -1:
        render_template("signIn.html")
    elif request.method == 'POST':
        pid = int(request.form['pid'])

        query = f"""
                DELETE FROM Product
                WHERE pid = {pid}
                """
        cur.execute(query)
        flash("Product Deletion Complete!")
    return render_template('deleteProduct.html')
    
@app.route('/deleteShipping', methods=['GET','POST'])
def deleteShipping():
    global uid
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        orderid = int(request.form['orderid'])
        query = f"""
                DELETE FROM Shipping
                WHERE (orderid = {orderid});
                """
        cur.execute(query)
        conn.commit()
        flash("Shipping Deletion Complete!")
    return render_template('deleteShipping.html')
    
@app.route('/searchOrder', methods=['GET','POST'])
def searchOrder():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    else:
        
        query = f"""
                SELECT * FROM Shipping
                WHERE uid = {uid}
                """
        for row in cur.execute(query):
            resultSet.append(row)    
        
    return render_template('searchOrder.html', result = resultSet)
    
@app.route('/searchProducer', methods=['GET','POST'])
def searchProducer():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        producerid = request.form['producerid']
        query = f"""
                SELECT * FROM Producer
                WHERE producerid = {producerid}
                """
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('searchProducer.html', result = resultSet)            
    else:
        query = f"""
                SELECT * FROM Producer
                """
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('searchProducer.html', result = resultSet)
    
@app.route('/searchProduct', methods=['GET','POST'])
def searchProduct():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        pid = request.form['pid']
        query = f"""
                SELECT * FROM Product
                WHERE pid = {pid}
                """
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('searchProduct.html', result = resultSet)            
    else:
        query = f"""
                SELECT * FROM Product
                """
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('searchProduct.html', result = resultSet)
    
@app.route('/shippingHistory', methods=['GET','POST'])
def shippingHistory():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    else:
        
        query = f"""
                SELECT * FROM Shipping
                WHERE uid = {uid}
                """
        for row in cur.execute(query):
            resultSet.append(row)    
        
    return render_template('shippingHistory.html', result = resultSet)
    
@app.route('/updateOrder', methods=['GET','POST'])
def updateOrder():
    global uid
    result_set = []
    if uid == -1:
        render_template("signIn.html")
    
    elif request.method == 'POST':
        orderid = int(request.form['orderid'])
        zipcode = str(request.form['zipcode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])

        query = f"""
                UPDATE Shipping 
                SET zipcode='{zipcode}', state='{state}', city='{city}',
                    street='{street}'
                WHERE uid = {uid} and orderid = {orderid}
                """
        cur.execute(query)
        flash("Successfully Updated Order Table!")
    return render_template('updateOrder.html')
    
@app.route('/updateProducer', methods=['GET','POST'])
def updateProducer():
    result_set = []
    global uid
    if uid == -1:
        render_template("signIn.html")
    
    elif request.method == 'POST':
        producerid = int(request.form['producerid'])
        country = str(request.form['country'])
        brand = str(request.form['brand'])

        query = f"""
                UPDATE Producer 
                SET country='{country}', brand='{brand}'
                WHERE producerid = {producerid}
                """
        cur.execute(query)
        flash("Successfully Update Producer Table!")
    return render_template('updateProducer.html')
    
@app.route('/updateProduct', methods=['GET','POST'])
def updateProduct():
    
    global uid
    result_set = []
    if uid == -1:
        render_template("signIn.html")
    
    elif request.method == 'POST':
        pid = int(request.form['pid'])
        name = str(request.form['name'])
        price = int(request.form['price'])
        stock = int(request.form['stock'])
        pinfo = str(request.form['pinfo'])

        query = f"""
                UPDATE Product 
                SET name='{name}', price='{price}', stock='{stock}', pinfo='{pinfo}'
                WHERE pid = {pid}
                """
        cur.execute(query)
        flash("Successfully Update Producer Table!")
    return render_template('updateProduct.html')
    
@app.route('/updateShipping', methods=['GET','POST'])
def updateShipping():
    global uid
    if request.method == 'POST':
        global uid
    if uid == -1:
        render_template("signIn.html")
    elif request.method == 'POST':
        orderid = int(request.form['orderid'])
        zipcode = str(request.form['zipcode'])
        state = str(request.form['state'])
        city = str(request.form['city'])
        street = str(request.form['street'])

        query = f"""
                UPDATE Shipping 
                SET zipcode='{zipcode}', state='{state}', city='{city}',
                    street='{street}'
                WHERE uid = {uid} and orderid = {orderid}
                """
        cur.execute(query)
        flash("Successfully Updated Shipping Table!")
    return render_template('updateShipping.html')
    
if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True)        