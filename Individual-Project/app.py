from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyAwpeUL5l9-xd-MZhr6-2Je2judJYWuZ44",
  "authDomain": "indi-67fb3.firebaseapp.com",
  "projectId": "indi-67fb3",
  "storageBucket": "indi-67fb3.appspot.com",
  "messagingSenderId": "997405169102",
  "appId": "1:997405169102:web:68aa0f131ab84164e0079f",
  "measurementId": "G-3M9LJ16EKS",
  "databaseURL":"https://indi-67fb3-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
#Code goes below here
@app.route('/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        preference = request.form['preference']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            uid = login_session['user']['localId']
            user = {"email" : email, 'password': password, "name" : name, "preference" : preference}
            db.child("Users").child(uid).set(user)
            return redirect(url_for("choices"))
        except:
            error = "oppsie smol mistake try agean"
            print(error)
            return render_template("signup.html")
    else:
        return render_template('signup.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for("choices"))
        except:
            error = "oppsie smol mistake try agean"
            return render_template('login.html')
    else:
        return render_template("login.html")

@app.route('/choices', methods = ['GET', 'POST'])
def choices():
    if request.method == 'POST':
        answer = request.form['ans']
        try:
            uid = login_session['user']['localId']
            preference = db.child('Users').child(uid).get().val()
            print(preference)
            if answer == 'yes':
                if preference['preference']== 'thin':
                    return redirect(url_for('thin'))
                elif preference['preference']== 'fat':
                    return redirect(url_for('fat'))
                elif preference['preference']== 'old':
                    return redirect(url_for('old'))
                elif preference['preference']== 'young':
                    return redirect(url_for('young'))
            if answer == 'no':
                return redirect(url_for("banned"))
        except:
            error = 'oppsie smol mistake'
            print(error)
    return render_template('choices.html')
        
@app.route('/cats', methods = ['GET', 'POST'])
def cats():
    if request.method == 'POST':
        return render_template("cats.html")

@app.route('/banned', methods = ['GET', 'POST'])
def banned():
    return render_template("banned.html")

@app.route('/thin', methods = ['GET', 'POST'])
def thin():
    return render_template("thin.html")

@app.route('/fat', methods = ['GET', 'POST'])
def fat():
    return render_template("fat.html")

@app.route('/old', methods = ['GET', 'POST'])
def old():
    return render_template("old.html")

@app.route('/young', methods = ['GET', 'POST'])
def young():
    return render_template("young.html")



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)