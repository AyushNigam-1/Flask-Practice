from flask import Flask , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql://root:@localhost/test'
app.config["SLQALCHEMY_MODIFICATIONS"]=True
db = SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , unique=False , nullable = False)
    gmail = db.Column(db.Integer(100) , nullable = False)
   

@app.route('/')
def index():
    name = 'ocean'
    gmail = "ayushnigam123@gmail.com"
    entry = User(name=name,gmail=gmail)
    db.session.add(entry)
    db.session.commit()
    return "Success"

if __name__ == '__main__':
    app.run(debug= True)