from flask import Flask, request, redirect, session, render_template, url_for
from firebase_admin import credentials, auth
import firebase_admin
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyDwZeFyPVyW2uoZQPbu4I_7GlkAbqMF0f0",
  "authDomain": "echobudget-a33b6.firebaseapp.com",
  "databaseURL": "https://echobudget-a33b6.firebaseio.com",
  "projectId": "echobudget-a33b6",
  "storageBucket": "echobudget-a33b6.appspot.com",
  "messagingSenderId": "885731958339",
  "appId": "1:885731958339:web:a413543b33d9fdf2e73ef6",
  "measurementId": "G-CW9D3MDWPM"
}
app = Flask(__name__)

cred = credentials.Certificate('./dronevr-393dd-firebase-adminsdk-geanm-58098126de.json')
firebase_a = firebase_admin.initialize_app(cred)
fb = pyrebase.initialize_app(firebaseConfig)
db = fb.database()
auth = fb.auth()
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


@app.route("/")
def login():
    return render_template("index.html")


@app.route("/home")
def home():
    if person["is_logged_in"]:
        return render_template("loading.html", email=person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))


@app.route("/result", methods=["POST","GET"])
def result():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        try:
            # Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            # Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            # Redirect to welcome page
            return redirect(url_for('home'))
        except:
            # If there is any error, redirect back to login
            return redirect(url_for('login'))
        else:
            if person["is_logged_in"] == True:
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
