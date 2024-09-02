from flask import Flask , abort , render_template , request , session , redirect
from flask_pymongo import PyMongo
from mongoconfig import config
import json
import datetime
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
    return render_template('login.html',signupSuccess=signupSuccess)


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
def login ():
    if request.method == 'POST':
        # try:
        #    email = request.form['username']
        # except KeyError:
        #    email = ''
        # try:
        #    password = request.form['password']
        # except KeyError:
        #    password = ''

        # if not len(email) > 0 or not '@' in email or not '.' in email:
        #     session['error'] = 'Email is required'
        #     return redirect('/')
        
        # if not len(password) > 0:
        #     session['error'] = 'Password is required'
        #     return redirect('/')
        
        # user_count = mongo.db.users.count_documents({"email" :email})
        # if user_count > 0:
        #     session['error']= 'Email already exists'
        #     return redirect('/')
          
        result = mongo.db.users.insert_one({
            'email':request.form['username'],
            'password':sha256(request.form['password'].encode('utf-8')).hexdigest(),
            'name':'',
            'lastLoginDate':None,
            # 'createdAt':datetime.utcnow,
            'updatedAt':123
        })
        session['signupSuccess'] = 'Your user account is ready . You can log'
        # return f"{email} , {password}"
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug= True)