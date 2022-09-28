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
    return render_template('HRMain.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')

@app.route("/registerEmp", methods=['GET', 'POST'])
def registerEmp():
    return render_template('RegisterEmp.html')

@app.route("/searchEmp", methods=['GET', 'POST'])
def searchEmp():
    return render_template('SearchEmp.html')

@app.route("/backMain", methods=['GET', 'POST'])
def backMain():
    return render_template('HRMain.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    emp_id = request.form.get('emp_id')
    cursor = db_conn.cursor()

    query = "SELECT first_name FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query)
    first_name = cursor.fetchone()
    first_name = ''.join(first_name)

    query2 = "SELECT last_name FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query2)
    last_name = cursor.fetchone()
    last_name = ''.join(last_name)

    query3 = "SELECT pri_skill FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query3)
    pri_skill = cursor.fetchone()
    pri_skill = ''.join(pri_skill)


    query4 = "SELECT location FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query4)
    location = cursor.fetchone()
    location = ''.join(location)

    return render_template('DisplayEmp.html',first_name = first_name, last_name = last_name, pri_skill = pri_skill, location = location,emp_id = emp_id)

@app.route("/editAndDeleteEmp", methods=['GET', 'POST'])
def editAndDeleteEmp():
    emp_id = request.form.get('emp_id')
    cursor = db_conn.cursor()

    query = "SELECT first_name FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query)
    first_name = cursor.fetchone()
    first_name = ''.join(first_name)

    query2 = "SELECT last_name FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query2)
    last_name = cursor.fetchone()
    last_name = ''.join(last_name)

    query3 = "SELECT pri_skill FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query3)
    pri_skill = cursor.fetchone()
    pri_skill = ''.join(pri_skill)


    query4 = "SELECT location FROM employee WHERE emp_id = '{}'".format(emp_id)
    cursor.execute(query4)
    location = cursor.fetchone()
    location = ''.join(location)

    return render_template('EditAndDeleteEmp.html',first_name = first_name, last_name = last_name, pri_skill = pri_skill, location = location,emp_id = emp_id)

@app.route("/completeEdit", methods=['POST'])
def completeEdit():
    emp_id = request.form.get("emp_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    pri_skill = request.form.get("pri_skill")
    location = request.form.get("location")

    update_sql = "Update employee set first_name = %s , last_name = %s , pri_skill = %s, location = %s where emp_id = %s"
    cursor = db_conn.cursor()

    cursor.execute(update_sql, (first_name, last_name , pri_skill, location , emp_id))
    db_conn.commit()
    return render_template('SearchEmp.html')

@app.route("/completeDelete", methods=['POST'])
def completeDelete():
    emp_id = request.form.get("emp_id")

    delete_sql = "Delete from employee where emp_id = %s"
    cursor = db_conn.cursor()

    cursor.execute(delete_sql, (emp_id))
    db_conn.commit()
    return render_template('SearchEmp.html')


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
    return render_template('RegisterEmpOutput.html', name=emp_name)


 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
