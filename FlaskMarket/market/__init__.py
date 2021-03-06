from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '411680636cde03a1a3589178'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from market import routes