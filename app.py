from flask import Flask , render_template , request , redirect , url_for

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route('/form',methods=['GET','POST'])
def form():
    if request.methods=='POST':
        sc = request.form['score']
        total = request.form['total']
        return redirect(url_for(f'/success',score=sc+total))
    return render_template('form.html')

@app.route('/success/<int:score>')
def success(score):
    res = ""
    if score>=50:
        res = "PASS"
    else:
        res = "FAIL"
    exp = {"res":res,"score":score}

    return render_template("index.html",results=res)

if __name__=='__main__':
    app.run(debug=True)