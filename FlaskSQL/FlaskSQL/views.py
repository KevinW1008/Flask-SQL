"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect
from FlaskSQL import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import pyodbc


#This configs the URL source of your SQL server. I used SQLExpress/MSSQL. Other types of SQL databases are acceptable. 
#To find your compatible URL check out this link in the Connection URI Format section:
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
app.config['SQLALCHEMY_DATABASE_URI']= "mssql://LENOVO-Y900\SQLEXPRESS/TestDB?driver=SQL+Server?trusted_connection=yes" #Put your URL in the quotes to the left
db = SQLAlchemy(app)

#Generates a quick and rudimentary object model from an existing database on the fly.
Base = automap_base()
#We are reflecting the databases
Base.prepare(db.engine, reflect= True)
#Mapped class customer is matched to table in SQL Database
Customer = Base.classes.customer
          
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year= datetime.now().year,
    )

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        if "addition" in request.form:
            cust_Name= request.form.get('name')
            home_Add= request.form.get('homeAdd')
            city_= request.form.get('city')
            state_Name= request.form.get('state')
            zip_Code= request.form.get('zipCode')
            email_= request.form.get('email')
            cell_= request.form.get('cell')

            new_cust= Customer(
                custName= "{}".format(cust_Name), 
                homeAdd= "{}".format(home_Add), 
                city= "{}".format(city_), 
                stateName= "{}".format(state_Name), 
                zipCode= "{}".format(zip_Code), 
                email= "{}".format(email_), 
                cell= "{}".format(cell_)
                )
            db.session.add(new_cust)
            db.session.commit()

        elif "deletion" in request.form:
            cust_ID= request.form.get('ID')
            db.session.query(Customer).filter(Customer.custID == cust_ID).delete()
            db.session.commit()

        elif "update" in request.form:
            cust_ID= request.form.get('ID')
            
            customer= db.session.query(Customer).get(cust_ID)

            #If any inputs are '' I assume the user does not want to change those values
            #Thus those fields will remain the same
            cust_Name= request.form.get('name')
            if(cust_Name == ''):
                cust_Name= customer.custName
            home_Add= request.form.get('homeAdd')
            if(home_Add == ''):
                home_Add= customer.homeAdd
            city_= request.form.get('city')
            if(home_Add == ''):
                home_Add= customer.homeAdd
            state_Name= request.form.get('state')
            if(state_Name == ''):
                state_Name= customer.stateName
            zip_Code= request.form.get('zipCode')
            if(zip_Code == ''):
                zip_Code= customer.zipCode
            email_= request.form.get('email')
            if(email_ == ''):
               email_= customer.email
            cell_= request.form.get('cell')
            if(cell_ == ''):
                cell_= customer.cell

            db.session.query(Customer).filter(Customer.custID == cust_ID).update(
                {Customer.custName: "{}".format(cust_Name), 
                Customer.homeAdd: "{}".format(home_Add), 
                Customer.city: "{}".format(city_), 
                Customer.stateName: "{}".format(state_Name), 
                Customer.zipCode: "{}".format(zip_Code), 
                Customer.email: "{}".format(email_), 
                Customer.cell: "{}".format(cell_)},
                )

            db.session.commit()

       
    #all() returns a list
    customers= db.session.query(Customer).all()
    db.session.close()
    return render_template(
        'table.html',
         title='Database',
         year=datetime.now().year,
         customer= customers
    )
