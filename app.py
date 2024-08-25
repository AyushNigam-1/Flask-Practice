from flask import Flask , render_template , request , redirect , url_for , abort , flash , session , make_response

app = Flask(__name__)
app.secret_key = "abc"
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


if __name__=='__main__':
    app.run(debug=True)