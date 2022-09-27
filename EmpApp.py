from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('RegisterEmp.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addemp", methods=['POST', 'GET'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)

@app.route("/fetchdata", methods=['POST', 'GET'])
def fetchdata():
    emp_id = (request.form['emp_id']).lower()
    check_sql = "SELECT emp_id FROM employee WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(check_sql, (emp_id))
    emp_id = re.sub('\W+','', str(cursor.fetchall()))
    check_sql = "SELECT first_name FROM employee WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(check_sql, (emp_id))
    emp_fname = re.sub('\W+','', str(cursor.fetchall()))
    check_sql = "SELECT last_name FROM employee WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(check_sql, (emp_id))
    emp_lname = re.sub('\W+','', str(cursor.fetchall()))
    check_sql = "SELECT pri_skill FROM employee WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(check_sql, (emp_id))
    emp_interest = re.sub('\W+','', str(cursor.fetchall()))
    check_sql = "SELECT location FROM employee WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(check_sql, (emp_id))
    emp_location = re.sub('\W+','', str(cursor.fetchall()))
    check_sql = "SELECT check_in FROM employee WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(check_sql, (emp_id))
    emp_image_url = re.sub('\W+','', str(cursor.fetchall()))
    if str(emp_fname) != "":
        return render_template('GetEmpOutput.html', id=emp_id, fname=emp_fname, 
        lname=emp_lname, interest=emp_interest, location=emp_location, image_url = emp_image_url)
    else:
        print("Invalid ID")
        return render_template('GetEmp.html')
    

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    return render_template('RegisterEmp.html')

@app.route("/searchEmp", methods=['GET', 'POST'])
def submit():
    return render_template('SearchEmp.html')

@app.route("/searchEmp", methods=['GET', 'POST'])
def submit():
    return render_template('SearchEmp.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
