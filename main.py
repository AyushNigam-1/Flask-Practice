from flask import Flask , abort
from flask_pymongo import PyMongo
from mongoconfig import config
import json
app = Flask(__name__)

app.config['MONGO_URI'] = config['mongo_url']
mongo = PyMongo(app)

@app.route("/")
def hello_world():
    user = mongo.db.users.find({})
    print(user)
    user = list(user)
    for doc in user:
        print(doc)
    return json.dumps(user)
    # return "Hello"

# @app.route("/")