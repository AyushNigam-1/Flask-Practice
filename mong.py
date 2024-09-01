from flask import Flask , abort , render_template , request
from flask_pymongo import PyMongo
from mongoconfig import config
import json
app = Flask(__name__)
app.secret_key  = b'kjsdfjbdf/sjdnf'
app.config['MONGO_URI'] = config['mongo_url']
mongo = PyMongo(app)


@app.route("/")
def hello_world():
    teach = mongo.db.teachers.find()
    # user = mongo.db.users.find()
    # print(user)
    # user = list(user)
    for doc in teach:
        print(doc["name"])
    # return json.dumps(user)
    return "Hello"

@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        return f"{email} , {password}"
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug= True)