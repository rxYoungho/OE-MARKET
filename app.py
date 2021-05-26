
import os
import sqlite3
from flask import Flask, render_template
#session, redirect, url_for, flash, request

app = Flask(__name__)

conn = sqlite3.connect('KYHFinal.db', check_same_thread=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)