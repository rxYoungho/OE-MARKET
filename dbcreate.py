import os
import sqlite3

print(os.path.abspath(os.path.dirname(__file__)))

conn = sqlite3.connect('JHps5.db')

cur = conn.cursor()

# Create tables
cur.execute('''DROP TABLE IF EXISTS Products''')
cur.execute('''CREATE TABLE Products
               (maker TEXT, model Integer, type TEXT )''') 

cur.execute('''DROP TABLE IF EXISTS PCs''')
cur.execute('''CREATE TABLE PCs
               (model Integer, speed REAL, ram Integer, hd Integer, price Integer)''')

cur.execute('''DROP TABLE IF EXISTS Laptops''')
cur.execute('''CREATE TABLE Laptops
               (model Integer, speed REAL, ram Integer, hd Integer, screen Integer, price Integer)''')

cur.execute('''DROP TABLE IF EXISTS Printers''')
cur.execute('''CREATE TABLE Printers
               (model Integer, color TEXT, type TEXT, price Integer)''') 
               

# Insert Products
cur.execute("INSERT INTO Products VALUES ('Samsung', '1', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Samsung', '2', 'Printer')")
cur.execute("INSERT INTO Products VALUES ('Samsung', '3', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('Samsung', '4', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('LG', '5', 'PC')")
cur.execute("INSERT INTO Products VALUES ('LG', '6', 'PC')")
cur.execute("INSERT INTO Products VALUES ('LG', '7', 'Printer')")
cur.execute("INSERT INTO Products VALUES ('LG', '8', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('LG', '9', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('LG', '10', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Apple', '11', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Apple', '12', 'Printer')")
cur.execute("INSERT INTO Products VALUES ('Apple', '13', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('Apple', '14', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('Dell', '15', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('Dell', '16', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('Dell', '17', 'Printer')")
cur.execute("INSERT INTO Products VALUES ('Dell', '18', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Asus', '19', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Asus', '20', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Asus', '21', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Lenovo', '22', 'Laptop')")
cur.execute("INSERT INTO Products VALUES ('Lenovo', '23', 'Printer')")
cur.execute("INSERT INTO Products VALUES ('Lenovo', '24', 'PC')")
cur.execute("INSERT INTO Products VALUES ('Lenovo', '25', 'Printer')")

# Insert PCs
cur.execute("INSERT INTO PCs VALUES ( '1', 2.3, 8, 1000, 998000 )")
cur.execute("INSERT INTO PCs VALUES ( '5', 1.6, 8, 550, 698000 )")
cur.execute("INSERT INTO PCs VALUES ( '6', 2.2, 16, 1000, 1138000 )")
cur.execute("INSERT INTO PCs VALUES ( '10', 2.0, 32, 1000, 2280000 )")
cur.execute("INSERT INTO PCs VALUES ( '11', 1.0, 4, 1000, 1778000 )")
cur.execute("INSERT INTO PCs VALUES ( '15', 3.0, 32, 5000, 1680000 )")
cur.execute("INSERT INTO PCs VALUES ( '18', 1.5, 8, 25600, 1140000 )")
cur.execute("INSERT INTO PCs VALUES ( '19', 2.0, 8, 51200, 122000 )")
cur.execute("INSERT INTO PCs VALUES ( '20', 2.23, 8, 51200, 1230000 )")
cur.execute("INSERT INTO PCs VALUES ( '21', 2.42, 16, 51200, 1180000 )")
cur.execute("INSERT INTO PCs VALUES ( '24', 2.61, 16, 102400, 2680000 )")
# Insert Laptops
cur.execute("INSERT INTO Laptops VALUES ( '3', 1.4, 8, 550, 11, 490000 )")
cur.execute("INSERT INTO Laptops VALUES ( '4', 1.4, 8, 1000, 15, 870000 )")
cur.execute("INSERT INTO Laptops VALUES ( '8', 1.4, 8, 1000, 13, 990000 )")
cur.execute("INSERT INTO Laptops VALUES ( '9', 1.4, 8, 550, 11, 640000 )")
cur.execute("INSERT INTO Laptops VALUES ( '13', 2.0, 16, 1000, 11, 1380000 )")
cur.execute("INSERT INTO Laptops VALUES ( '14', 2.0, 16, 1000, 15, 1660000 )")
cur.execute("INSERT INTO Laptops VALUES ( '15', 2.0, 16, 1000, 15, 1660000 )")
cur.execute("INSERT INTO Laptops VALUES ( '16', 2.0, 16, 1000, 15, 1660000 )")
cur.execute("INSERT INTO Laptops VALUES ( '22', 2.0, 16, 1000, 15, 1660000 )")

# Insert Printers
cur.execute("INSERT INTO Printers VALUES ( '2', 'True', 'Laser', 370000 )")
cur.execute("INSERT INTO Printers VALUES ( '25', 'True', 'Laser', 270000 )")
cur.execute("INSERT INTO Printers VALUES ( '7', 'False', 'Laser', 270000 )")
cur.execute("INSERT INTO Printers VALUES ( '12', 'True', 'Ink-jet', 440000 )")
cur.execute("INSERT INTO Printers VALUES ( '17', 'True', 'Ink-jet', 300000 )")
cur.execute("INSERT INTO Printers VALUES ( '23', 'True', 'Ink-jet', 550000 )")



conn.commit()
cur = conn.cursor()
conn.close()