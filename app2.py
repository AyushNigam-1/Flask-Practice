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


def editpost():
    if('email' in session):
        Blog.query.filter_by(index=id).first()
        return render_template('editpost.html',username=session['email'],account=user)
    else:
        return render_template('login.html')
    
app.route("/updatepost/<int:id>",methods=['POST'])
def updatepost(id):
    if ("email" in session):
        if request.method == 'POST':
            user = Blog.query.filter_by(index=id).first()
            user.title=request.form['title']
            user.blogcontent= request.form['blogdata']
            db.session.add(user)
            db.session.commit()
            flash("updated successfully")
            return redirect("/profile")
        else:
            flash("updated successfully")
            return redirect("/profile")
    else:
        return render_template('login_html')

