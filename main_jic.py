################################################################################
################################################################################
########                                                                ########
########   Python - Firebase - Flask Login/Register App                 ########
########   Author: Hemkesh Agrawal                                      ########
########   Website: http://hemkesh.com                                  ########
########   Last updated on: 11/27/2019                                  ########
########                                                                ########
########   P.S. This is my first ever github project, so I              ########
########   would love to hear your feedback : agrawalh@msu.edu          ########
########                                                                ########
################################################################################
################################################################################
# source https://github.com/Hemkesh/python-firebase-flask-login
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_cors import CORS

# caro add
import config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)       #Initialze flask constructor
CORS(app)

#Add your own details
#config = {
 # "apiKey":"",
 # "authDomain": "color-thingy.firebaseapp.com",
 # "databaseURL":"https://color-thingy-default-rtdb.firebaseio.com/",
#  "databaseURL": "color-thingy.firebaseio.com",
  #"storageBucket": "color-thingy.appspot.com"
#}

#initialize firebase
#cred = credentials.Certificate(config.firestore_secret)
#firebase = pyrebase.initialize_app(cred)
#auth = firebase.auth()
#db = firebase.database()

## Caro add
cred = credentials.Certificate(config.firestore_secret)
auth = firebase_admin.initialize_app(cred)
db = firestore.client()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            print('one')
            #Try signing in the user with the given information
            #user = auth.sign_in_with_email_and_password(email, password)
            print('two')
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            print('three')
            #Get the name of the user
            doc_ref = db.collection(email).document('self')
            doc = doc_ref.get()
            data = doc.to_dict()
            print(doc)
            print(data)

            #data = db.child("users").get()
            print('four')
            person["name"] = data['name']
            print('five')
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            print('login fail')
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        #try:
        print(' step 0')
        #Try creating the user account using the provided data
        #auth.create_user_with_email_and_password(email, password)
        print('step 1.3')
        #Login the user
        #user = auth.sign_in_with_email_and_password(email, password)
        print('step 1')
        #Add data to global person
        global person
        person["is_logged_in"] = True
        person["email"] = email#user["email"]
        person["uid"] = 'blah TBD'# user["localId"]
        person["name"] = name
        print('step 2')
        #Append data to the firebase realtime database
        data = {"name": name, "email": email}
        print('step 3')
        #db.child("users").child(person["uid"]).set(data) # realtime database
        db.collection(email).document('self').set(data, merge=True) #firestore database
        print('step 4')
        #Go to welcome page
        return redirect(url_for('welcome'))
        #except:
        #    print('stuck here')
            #If there is any error, redirect to register
    #        return redirect(url_for('signup')) # changed register to signup

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run()
