from flask import Flask, flash
# from flask_bcrypt import Bcrypt
app = Flask(__name__)

# bcrypt = Bcrypt(app)

app.secret_key = "Hello World!"



DATABASE = 'users_schema'