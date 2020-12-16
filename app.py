from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["ENV"] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Database(db.Model):
    rank = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    percentage = db.Column(db.String(255), nullable=False)

@app.route("/", methods=["GET"])
def home():
    table = Database.query.all()
    d=[]
    for row in table:
        row_as_dict = {
            "rank": row.rank,
            "company": row.company,
            "country": row.country,
            "percentage": row.percentage,
        }
        d.append(row_as_dict)
    return render_template("index.html", data = d)

@app.route("/api", methods=["GET"])
def api_route():
    table = Database.query.all()
    d=[]
    for row in table:
        row_as_dict = {
            "rank": row.rank,
            "company": row.company,
            "country": row.country,
            "percentage": row.percentage,
        }
        d.append(row_as_dict)
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)