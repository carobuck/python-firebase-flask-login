## following pyrebase tutorial directly, since other tutorials not working
# https://github.com/thisbejim/Pyrebase#manage-users
# fyi for urllib3 error: https://github.com/firebase/firebase-admin-python/issues/262

# this is for authenticating/saving user login...which I suppose is good from code practice...
# but might not be "necessary" for my purposes
import pyrebase
import config

firebase = pyrebase.initialize_app(config.keys)

# Get a reference to the auth service
auth = firebase.auth()
# Get a reference to the database service
db = firebase.database()


email = 'cbuck727@gmail.com'
password = 'caroline'
auth.create_user_with_email_and_password(email,password) # not sure where this gets saved within firebase...?

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)

# This works to save data, but kinda saves in a chaotic manner. let's save a better way
data = {"name": "caro 'Morty' Smith"}
db.child("users").push(data)

# to save in more orderly fashion
