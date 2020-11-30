# 
# IMPORTS
# 
# you might have to import additional things you need

from flask import Flask, render_template, request, jsonify, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

#
# SETUP/CONFIG
#
# change the classname to reflect the name of your table
# change the columns to reflect the columns you need
# each row of your data will be an instance of this class

app = Flask(__name__)

app.config["ENV"] = 'development'
app.config["SECRET_KEY"]=b'_5#y2L"F4Q8z\n\xec]/'

# change the following .db file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-db-name.db'
# this line is to prevent SQLAlchemy from throwing a warning
# if you don't get one with out it, feel free to remove
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#
# DB SETUP
# 

# this set's up our db connection to our flask application
db = SQLAlchemy(app)

# this is our model (aka table)
class DBTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    # email = db.Column(db.Text, nullable=False)
    # phone = db.Column(db.Integer, nullable=False)
    #column_3 = db.Column(db.DateTime, nullable=False)
    #column_4 = db.Column(db.Float, nullable=False)
    #column_5 = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<DBTable {self.id} {self.first_name} {self.last_name}>" 

    def serialize():
        return {"id": DBTable.id,
                "first_name": DBTable.first_name,
                "last_name": DBTable.last_name}
                # "email": DBTable.email,
                # "phone": DBTable.phone}

d = DBTable.serialize()

#
# VIEWS 
#

# set up your index view to show your "home" page
# it should include:
# links to any pages you have
# information about your data
# information about how to access your data
# you can choose to output data on this page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# include other views that return html here:
@app.route('/other',  methods=['GET', 'POST'])
def other():
    error = None
    if request.method == 'POST':
        if request.form['first_name'] != 'kari' or \
                request.form['last_name'] != 'sakib':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('other.html', error=error)

# set up the following views to allow users to make
# GET requests to get your data in json
# POST requests to store/update some data
# DELETE requests to delete some data

# change this to return your data
@app.route('/api', methods=['GET'])
def get_data():
    table = DBTable.query.all()
    d = {row.first_name:row.last_name for row in table}
    return jsonify(d)

# change this to allow users to add/update data
@app.route('/api', methods=['POST'])
def add_data():
    added = {}
    for k,v in request.args.items():
        if not k in d.keys():
            added[k] = v
            d[k] = v
    return jsonify(d)
        
# change this to allow the deletion of data
@app.route('/api', methods=['DELETE'])
def delete_data():
    deleted = {}
    for k,v in request.args.items():
        try:
            d.pop(k)
            deleted[k] = v
        except:
            continue
    return jsonify(d)

#
# CODE TO BE EXECUTED WHEN RAN AS SCRIPT
#

if __name__ == '__main__':
    app.run(debug=True)
