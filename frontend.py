 #!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import MySQLdb

import sqlite3

import sys

import config

import entities

USERNAME = config.USERNAME
PASSWORD = config.PASSWORD
DB_NAME = config.DB_NAME
host = config.ENDPOINT

app = Flask(__name__, static_url_path="")

@app.route('/', methods=['GET', 'POST'])
def home_page():
    
    conn = MySQLdb.connect (	host = host,
                            user = USERNAME,
                            passwd = PASSWORD,
                            db = DB_NAME,
                            port = 3306
                            )
            
    cursor = conn.cursor ()
    cursor.execute ("SELECT VERSION()")
    row = cursor.fetchone ()
    cursor.execute("SELECT * FROM Topic;")
    rows = cursor.fetchall()
    items=[]
    needs = []
    if request.method == 'POST':
        questions = request.form['question']
        options = entities.form_db_queries(questions)
        options.append(questions)
        
        for item in rows:
            for question in options:
                if (question == item[0]):
                    cursor.execute("SELECT * FROM Needs WHERE topicName='"+item[0]+"';")
                    inrows = cursor.fetchall()
                    print(inrows)
                    for it in inrows:
                        cursor.execute("SELECT * FROM Resource WHERE resourceName='"+it[1]+"';")
                        picrows = cursor.fetchall()
                        stri = "http://www.homedepot.com/s/"+str(it[1])
                        it = it + picrows + (stri,)
                        needs.append(it)
                    items.append(item)
        
        return results_page(question,items,needs)
    else:
        return render_template('ask.html')

@app.route('/results', methods=['GET'])
def results_page(question,items,needs):
    return render_template('results.html', qs = question, it = items, needs=needs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
