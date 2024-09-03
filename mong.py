from flask import Flask , abort , render_template , request , session , redirect
from flask_pymongo import PyMongo
from mongoconfig import config
import json
import time
import re
from hashlib import sha256
app = Flask(__name__)
app.secret_key  = b'kjsdfjbdf/sjdnf'
app.config['MONGO_URI'] = config['mongo_url']
mongo = PyMongo(app)

@app.route("/login")
def show_login():
    signupSuccess = ''
    if 'signupSuccess' in session:
        signupSuccess = session['signupSuccess']
        session.pop('signupSuccess',None)

    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error',None)
    return render_template('login.html',signupSuccess=signupSuccess)


def check_login():
    try:
        email = request.form['username']
    except KeyError:
        email = ''
    try:
        password = request.form['password']
    except KeyError:
        password = ''
    
    if not len(email)>0:
        session['error'] = 'Email is required'
        return redirect('/login')

    user_documents = mongo.db.users.find({"email":email})
# @app.route("/")
# def hello_world():
#     teach = mongo.db.teachers.find()
#     # user = mongo.db.users.find()
#     # print(user)
#     # user = list(user)
#     for doc in teach:
#         print(doc["name"])
#     # return json.dumps(user)
#     return "Hello"


def show_signup():
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error',None)
    
    return render_template('signup.html',error=error)

@app.route("/" , methods=['GET','POST'])
def signup ():
    print(request.form['email'] ,request.form['password'] )
    # if request.method == 'POST':
    #     try:
    #        email = request.form['username']
    #     except KeyError:
    #        email = ''
    #     try:
    #        password = request.form['password']
    #     except KeyError:
    #        password = ''

    #     if validate_email(email):
    #         session['error'] = 'Email is required'
    #         return redirect('/')
        
    #     if not len(password) > 0:
    #         session['error'] = 'Password is required'
    #         return redirect('/')
        
    #     user_count = mongo.db.users.count_documents({"email" :email})
    #     if user_count > 0:
    #         session['error']= 'Email already exists'
    #         return redirect('/')
          
    #     result = mongo.db.users.insert_one({
    #         'email':request.form['username'],
    #         'password':sha256(request.form['password'].encode('utf-8')).hexdigest(),
    #         'name':'',
    #         'lastLoginDate':None,
    #         'createdAt':time.time(),
    #         'updatedAt':time.time()
    #     })
    #     session['signupSuccess'] = 'Your user account is ready . You can log'
        # return f"{email} , {password}"
    return render_template('signup.html')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

if __name__ == '__main__':
    app.run(debug= True)