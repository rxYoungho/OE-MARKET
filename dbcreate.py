"""
Youngho Kim
110710626

youngho.kim@stonybrook.edu
"""
import os
import sqlite3

print(os.path.abspath(os.path.dirname(__file__)))

conn = sqlite3.connect('OEDB.db')

cur = conn.cursor()

# Create tables
cur.execute('''DROP TABLE IF EXISTS Address''')
cur.execute('''CREATE TABLE Address (
                uid integer NOT NULL ,
                zip varchar(45) NOT NULL,
                state varchar(45) NOT NULL,
                city varchar(45) NOT NULL,
                street varchar(45) NOT NULL,
                FOREIGN KEY(uid) REFERENCES User(uid) ON DELETE CASCADE
            )''') 

cur.execute('''DROP TABLE IF EXISTS Cart''')
cur.execute('''CREATE TABLE Cart (
                uid integer NOT NULL,
                pid integer NOT NULL,
                date datetime NOT NULL,
                FOREIGN KEY(uid) REFERENCES User(uid) ON DELETE CASCADE,
                FOREIGN KEY(pid) REFERENCES Product(pid) ON DELETE CASCADE
            )''')
            
cur.execute('''DROP TABLE IF EXISTS CategoryPreference''')
cur.execute('''CREATE TABLE CategoryPreference (
                uid integer NOT NULL,
                CategoryPreferencecol varchar(45) DEFAULT NULL,
                PRIMARY KEY (uid,CategoryPreferencecol),
                FOREIGN KEY(uid) REFERENCES User(uid) ON DELETE CASCADE
            )''')

cur.execute('''DROP TABLE IF EXISTS Producer''')
cur.execute('''CREATE TABLE Producer (
                producerid integer NOT NULL,
                country varchar(45) DEFAULT NULL,
                brand varchar(45) DEFAULT NULL,
                PRIMARY KEY (producerid)
            )''')

cur.execute('''DROP TABLE IF EXISTS Product''')
cur.execute('''CREATE TABLE Product (
                pid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                name varchar(45) NOT NULL,
                price integer NOT NULL,
                stock integer NOT NULL,
                pinfo varchar(200) DEFAULT NULL,
                producerid integer,
                FOREIGN KEY (producerid) REFERENCE Producer(producerid)
            )''')

cur.execute('''DROP TABLE IF EXISTS ProductCategory''')
cur.execute('''CREATE TABLE ProductCategory (
                pid integer NOT NULL,
                category varchar(45) NOT NULL,
                PRIMARY KEY (pid, category),
                FOREIGN KEY(pid) REFERENCES Product(pid) ON DELETE CASCADE
            )''') 

cur.execute('''DROP TABLE IF EXISTS Purchase''')
cur.execute('''CREATE TABLE Purchase (
                purchaseid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                uid integer NOT NULL,
                pid integer NOT NULL,
                quantity integer NOT NULL,
                date datetime NOT NULL,
                zipcode varchar(45) DEFAULT NULL,
                state varchar(45) DEFAULT NULL,
                city varchar(45) DEFAULT NULL,
                street varchar(45) DEFAULT NULL,
                
                FOREIGN KEY(uid) REFERENCES User(uid) ON DELETE CASCADE,
                FOREIGN KEY(pid) REFERENCES Product(pid) ON DELETE CASCADE
            )''') 

cur.execute('''DROP TABLE IF EXISTS Selling''')
cur.execute('''CREATE TABLE Selling (
                sid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                pid integer NOT NULL,
                Date datetime NOT NULL,
                FOREIGN KEY(pid) REFERENCES Product(pid) ON DELETE CASCADE
            )''') 

cur.execute('''DROP TABLE IF EXISTS Shipping''')
cur.execute('''CREATE TABLE Shipping (
                orderid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                uid integer NOT NULL,
                pid integer NOT NULL,
                quantity integer NOT NULL,
                orderDate datetime NOT NULL,
                zipcode varchar(45) NOT NULL,
                state varchar(45) NOT NULL,
                city varchar(45) NOT NULL,
                street varchar(45) NOT NULL,
                FOREIGN KEY(uid) REFERENCES User(uid) ON DELETE CASCADE,
                FOREIGN KEY(pid) REFERENCES Product(pid) ON DELETE CASCADE
    
            )''') 

cur.execute('''DROP TABLE IF EXISTS User''')
cur.execute('''CREATE TABLE User (
                uid integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                id varchar(45) NOT NULL,
                pw varchar(45) NOT NULL,
                name varchar(45) NOT NULL
                
            )''') 
               

# # Insert rows of data for Products
# cur.execute("INSERT INTO Products VALUES ('Samsung', '1001', 'PC')")
# cur.execute("INSERT INTO Products VALUES ('Samsung', '1002', 'Printer')")
# cur.execute("INSERT INTO Products VALUES ('ASUS', '1003', 'Laptop')")
# cur.execute("INSERT INTO Products VALUES ('Apple', '1004', 'Laptop')")
# cur.execute("INSERT INTO Products VALUES ('LG', '1005', 'PC')")
# cur.execute("INSERT INTO Products VALUES ('LG', '1006', 'PC')")
# cur.execute("INSERT INTO Products VALUES ('Apple', '1007', 'Printer')")
# cur.execute("INSERT INTO Products VALUES ('ASUS', '1008', 'Laptop')")
# cur.execute("INSERT INTO Products VALUES ('Samsung', '1009', 'Laptop')")
# cur.execute("INSERT INTO Products VALUES ('LG', '1010', 'PC')")
# cur.execute("INSERT INTO Products VALUES ('Samsung', '1011', 'PC')")
# cur.execute("INSERT INTO Products VALUES ('Samsung', '1012', 'Printer')")
# cur.execute("INSERT INTO Products VALUES ('ASUS', '1013', 'Laptop')")
# cur.execute("INSERT INTO Products VALUES ('Apple', '1014', 'Laptop')")
# cur.execute("INSERT INTO Products VALUES ('LG', '1015', 'PC')")
# cur.execute("INSERT INTO Products VALUES ('LG', '1016', 'Printer')")
# # Insert rows of data for PCs
# cur.execute("INSERT INTO PCs VALUES ( '1001', 2.0, 8, 1000, 898000 )")
# cur.execute("INSERT INTO PCs VALUES ( '1005', 1.4, 8, 550, 798000 )")
# cur.execute("INSERT INTO PCs VALUES ( '1006', 2.0, 16, 1000, 1028000 )")
# cur.execute("INSERT INTO PCs VALUES ( '1010', 2.0, 32, 1000, 2000000 )")
# cur.execute("INSERT INTO PCs VALUES ( '1011', 1.4, 8, 1000, 1728000 )")
# cur.execute("INSERT INTO PCs VALUES ( '1015', 2.0, 8, 1000, 1680000 )")
# # Insert rows of data for Laptops
# cur.execute("INSERT INTO Laptops VALUES ( '1003', 1.4, 8, 550, 11, 490000 )")
# cur.execute("INSERT INTO Laptops VALUES ( '1004', 1.4, 8, 1000, 15, 870000 )")
# cur.execute("INSERT INTO Laptops VALUES ( '1008', 1.4, 8, 1000, 13, 990000 )")
# cur.execute("INSERT INTO Laptops VALUES ( '1009', 1.4, 8, 550, 11, 640000 )")
# cur.execute("INSERT INTO Laptops VALUES ( '1013', 2.0, 16, 1000, 11, 1380000 )")
# cur.execute("INSERT INTO Laptops VALUES ( '1014', 2.0, 16, 1000, 15, 1660000 )")
# # Insert rows of data for Printers
# cur.execute("INSERT INTO Printers VALUES ( '1002', 'Color', 'Laser', 370000 )")
# cur.execute("INSERT INTO Printers VALUES ( '1007', 'NonColor', 'Laser', 270000 )")
# cur.execute("INSERT INTO Printers VALUES ( '1012', 'Color', 'Ink-jet', 440000 )")
# cur.execute("INSERT INTO Printers VALUES ( '1016', 'Color', 'Ink-jet', 270000 )")

conn.commit()
conn.close()