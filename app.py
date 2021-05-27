import os
import sqlite3
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
   
@app.route('/signUp', methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        pw = request.form['pw']
        query = f"""
                INSERT INTO User(id, pw, name) VALUES('{id}','{pw}','{name}')"""
        cur.execute(query)
        conn.commit()
        return render_template('signUp.html',result= name)
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
                SELECT name, id, pw from User where uid = {uid}"""
        for row in cur.execute(query):
            resultSet.append(row)
        print(resultSet)
        if len(resultSet) > 0:
            
            return render_template('userInfo.html', result = resultSet[0])
    return render_template('userInfo.html', result= [])

@app.route('/searchUsers', methods=['GET','POST'])
def searchUsers():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    elif request.method == 'POST':
        id = request.form['id']
        query = f"""
                SELECT * from User where uid = {id}"""
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
                UPDATE User SET name = '{name}', id = '{id}', pw = '{pw}'
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
                WHERE uid = {userId} AND CategoryPreferencecol = '{category}'"""
        cur.execute(query)
        conn.commit()
        flash("Preference Delete Complete!")
    else:
        query = f"""
                SELECT CategoryPreferencecol FROM CategoryPreference
                WHERE uid = {uid}"""
        for row in cur.execute(query):
            resultSet.append(row)
        return render_template('deletePreference.html', result = resultSet)
    

@app.route('/searchCategory', methods=['GET','POST'])# 카테고리별로 나열
def searchCategory():
    global uid
    resultSet = []
    if uid == -1:
        return render_template('signIn.html')
    else:
        query = f"""
                SELECT * FROM ProductCategory
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
                SELECT * FROM Cart
                WHERE uid = {uid}
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
        query = f"""
                INSERT INTO Cart VALUES(uid = {uid}, pid = {pid})
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
        query = f"""
                UPDATE INTO Cart VALUES(uid = {uid}, pid = {pid})
                """
    return render_template('updateCart.html')

# YHK #####

@app.route('/addOrder', methods=['GET','POST'])
def addOrder():
    return render_template('addOrder.html')
    
@app.route('/addProducer', methods=['GET','POST'])
def addProducer():
    return render_template('addProducer.html')
    
@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    return render_template('addProduct.html')
    
@app.route('/addShipping', methods=['GET','POST'])
def addShipping():
    return render_template('addShipping.html')
    
@app.route('/deleteOrder', methods=['GET','POST'])
def deleteOrder():
    return render_template('deleteOrder.html')
    
@app.route('/deleteProducer', methods=['GET','POST'])
def deleteProducer():
    return render_template('deleteProducer.html')
    
@app.route('/deleteProduct', methods=['GET','POST'])
def deleteProduct():
    return render_template('deleteProduct.html')
    
@app.route('/deleteShipping', methods=['GET','POST'])
def deleteShipping():
    return render_template('deleteShipping.html')
    
@app.route('/searchOrder', methods=['GET','POST'])
def searchOrder():
    return render_template('searchOrder.html')
    
@app.route('/searchProducer', methods=['GET','POST'])
def searchProducer():
    return render_template('searchProducer.html')
    
@app.route('/searchProduct', methods=['GET','POST'])
def searchProduct():
    return render_template('searchProduct.html')
    
@app.route('/shippingHistory', methods=['GET','POST'])
def shippingHistory():
    return render_template('shippingHistory.html')
    
@app.route('/updateOrder', methods=['GET','POST'])
def updateOrder():
    return render_template('updateOrder.html')
    
@app.route('/updateProducer', methods=['GET','POST'])
def updateProducer():
    return render_template('updateProducer.html')
    
@app.route('/updateProduct', methods=['GET','POST'])
def updateProduct():
    return render_template('updateProduct.html')
    
@app.route('/updateShipping', methods=['GET','POST'])
def updateShipping():
    return render_template('updateShipping.html')
    
if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True)        