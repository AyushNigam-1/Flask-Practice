from flask import Flask , render_template , request , redirect , url_for , abort , flash , session , make_response
from flask.mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "abc"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "mydb"

mysql = MySQL(app)

@app.route("/")
def index():
    fname = "Ayush"
    lname = "Nigam"
    curr = mysql.connection_cursor()
    curr.execute("INSERT INTO user(fname , lname) VALUES(%s, %s)" , {fname,lname})
    mysql.connection.connect()
    curr.close()
    return "SUccess"

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        name = int(request.form['Name'])
        password = int(request.form['Password'])
        session['key'] = name
        flash("User Data Saved !")
        res = make_response(render_template("form.html"))
        res.set_cookie("framework",f"{password}")
        return res
        # res.set_cookie("Framework","flask")
        # return redirect(url_for(f'success',score=sc+total))
    # return render_template('form.html')

@app.route('/success/<int:score>')
def success(score):
    res = ""
    if score>=50:
        res = "PASS"
    else:
        res = "FAIL"
    exp = {"res":res,"score":score}

    return render_template("index.html",results=res)

def get_cookie():
    name = request.cookie.get("framework")
    return name

def Blog(db.Model):
    sno = db.Column(db.integer , primary_key = True),
    name = db.Column(db.String(80),unique=True,nullable=False),
    blogcontent = db.Column(db.String(80),unique=True,nullable=False)
    title = db.Column(db.String(256))

def profile():
    if('email' in session):
        posts = Blog.query.filter_by(email = session['email'])
        return render_template('profile.html' , account = posts)
    else:
        return render_template("login.html")
    

def deletepost(id):
    if "email" in session:
        user = Blog.query.filter_by(index=id).first()
        db.session.delete(user)
        db.session.commit()
        flask("delete successfully")
        return redirect("/profile")
    


if __name__=='__main__':
    app.run(debug=True)