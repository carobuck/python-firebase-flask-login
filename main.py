# source: https://makedeveasy.medium.com/authenitcation-using-python-flask-and-firestore-1958d29e2240
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import pyrebase
from flask_cors import CORS
import io
import json

from firebase_admin import auth

# TODO make config work in this file. config.keys
import config
#config.keys
app=Flask(__name__)
CORS(app)


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route("/")  #basic api
def home():
    return "hello all"

@app.route('/signup',methods=['POST'])   #signup api
def signup():
    email=request.json['email']   #get the email from json
    password=request.json['password'] #get the password from json
    if email is None or password is None:
       return jsonify({'message':'username and password must not in blank'}),400
    try:
        user = auth.create_user_with_email_and_password(email,password)
        user = auth.sign_in_with_email_and_password(email, password)
        #pb.auth().send_email_verification(user['idToken']) # ADD if want email verification?
        return jsonify({'message': f'Successfully created user'}),200
    except:
        if email:
            # TODO: this causes bugs.
            emailexists=auth.get_user_by_email(email)
            if(emailexists.uid):
                return jsonify({'message': 'user is already exists '}),400
        else:
            return jsonify({'message': 'error creating in user'}),400

@app.route('/signin',methods=['POST'])  #signin api
def signin():
    email=request.json['email']
    password=request.json['password']
    if email is None or password is None:
        return jsonify({'message':'username and password must not to be empty'})
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
        # TODO: what the heck is this stuff??
        arr=''

        for x in user:
            if x == 'localId':
                arr=(user[x])

        user1= auth.get_user(arr)
        user3=user1.email_verified
        print(user3)
        if user3:
            return user
        else:
            return jsonify({'message':'please verify your account with your mailId'}),400
    except:
        return jsonify({'message':'invalid crendentails please enter with valid credentials'}),400

if __name__ == "__main__":
    app.run()
