from flask import Flask , abort , render_template , request , session , redirect
from flask_pymongo import PyMongo
from mongoconfig import config
import json
import time
import re
from hashlib import sha256
from utils import get_random_string
app = Flask(__name__)
app.secret_key  = b'kjsdfjbdf/sjdnf'
app.config['MONGO_URI'] = config['mongo_url']
mongo = PyMongo(app)

@app.route("/logout")
def logout_user():
    session.pop("userToken",None)
    session['signupSuccess'] = 'You are now logged out.'
    return redirect("/login")

@app.route("/")
def show_index():
    if not 'userToken' in session:
        session['error'] = "You must login to access this page"
        return redirect('/login')
    token_document = mongo.db.user_tokens.find_one({
        'sessionHash':session['userToken'],
    })
    
    if token_document is None:
        session.pop("userToken",None)
        session['error'] = 'You must login again to access this page'
        return redirect("/login")
    
    print('Inside secure dashboard function')
    print(session['userToken'])
    
    return 'This is my secure home page'


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
    
    if not len(password) >0:
        session['error'] = 'Password is required'
        return redirect('/login')
    
    user_document = mongo.db.users.find_one({"email":email})
    if user_document is None:
        session['error'] = 'No account exists with this email address'
        return redirect('login')
    
    password_hash = sha256(password.encode('utf-8')).hexdigest()
    if password != password_hash:
        session['error'] = 'Invalid password'
        return redirect('/login')
    
    random_string = get_random_string()
    randomSessionHash = sha256(random_string.encode('utf-8')).hexdigest()
    result = mongo.db.users.insert_one({
            'userId':user_document['_id'],
            'sessionHash':randomSessionHash,
            'createdAt':time.time(),
        })
    session['userToken'] = randomSessionHash

    return redirect('/')

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