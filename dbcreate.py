"""
Youngho Kim
110710626

youngho.kim@stonybrook.edu
"""
import os
import sqlite3

print(os.path.abspath(os.path.dirname(__file__)))

conn = sqlite3.connect('JHPps5.db')

cur = conn.cursor()

# Create tables
cur.execute('''DROP TABLE IF EXISTS Address''')
cur.execute('''CREATE TABLE Address (
                uid int NOT NULL,
                zip varchar(45) NOT NULL,
                state varchar(45) NOT NULL,
                city varchar(45) NOT NULL,
                street varchar(45) NOT NULL,
                PRIMARY KEY (uid)
            )''') # type: PC, laptop, printer

cur.execute('''DROP TABLE IF EXISTS Cart''')
cur.execute('''CREATE TABLE Cart (
                uid int NOT NULL,
                pid int NOT NULL,
                date datetime NOT NULL,
                PRIMARY KEY (uid)
            )''')
            
cur.execute('''DROP TABLE IF EXISTS CategoryPreference''')
cur.execute('''CREATE TABLE CategoryPreference (
                uid int NOT NULL,
                CategoryPreferencecol varchar(45) DEFAULT NULL,
                PRIMARY KEY (uid)
            )''')

cur.execute('''DROP TABLE IF EXISTS Producer''')
cur.execute('''CREATE TABLE Producer (
                producerid int NOT NULL,
                country varchar(45) DEFAULT NULL,
                brand varchar(45) DEFAULT NULL,
                PRIMARY KEY (producerid)
            )''')

cur.execute('''DROP TABLE IF EXISTS Product''')
cur.execute('''CREATE TABLE Product (
                pid int NOT NULL,
                name varchar(45) NOT NULL,
                price int NOT NULL,
                stock int NOT NULL,
                pinfo varchar(200) DEFAULT NULL,
                PRIMARY KEY (pid)
            )''')

cur.execute('''DROP TABLE IF EXISTS ProductCategory''')
cur.execute('''CREATE TABLE ProductCategory (
                pid int NOT NULL,
                category varchar(45) NOT NULL,
                PRIMARY KEY (pid)
            )''') 

cur.execute('''DROP TABLE IF EXISTS Purchase''')
cur.execute('''CREATE TABLE Purchase (
                purchaseid int NOT NULL,
                uid int NOT NULL,
                pid int NOT NULL,
                quantity int NOT NULL,
                date datetime NOT NULL,
                zipcode varchar(45) DEFAULT NULL,
                state varchar(45) DEFAULT NULL,
                city varchar(45) DEFAULT NULL,
                street varchar(45) DEFAULT NULL,
                PRIMARY KEY (purchaseid)
            )''') 

cur.execute('''DROP TABLE IF EXISTS Selling''')
cur.execute('''CREATE TABLE Selling (
                sid int NOT NULL,
                pid int NOT NULL,
                Date datetime NOT NULL,
                PRIMARY KEY (sid)
            )''') 

cur.execute('''DROP TABLE IF EXISTS Shipping''')
cur.execute('''CREATE TABLE Shipping (
                orderid int NOT NULL,
                uid int NOT NULL,
                pid int NOT NULL,
                quantity int NOT NULL,
                orderDate datetime NOT NULL,
                zipcode varchar(45) NOT NULL,
                state varchar(45) NOT NULL,
                city varchar(45) NOT NULL,
                street varchar(45) NOT NULL,
                PRIMARY KEY (orderid)
            )''') 

cur.execute('''DROP TABLE IF EXISTS User''')
cur.execute('''CREATE TABLE User (
                uid int NOT NULL,
                id varchar(45) NOT NULL,
                pw varchar(45) NOT NULL,
                name varchar(45) NOT NULL,
                zip varchar(45) NOT NULL,
                PRIMARY KEY (uid)
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