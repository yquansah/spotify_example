import json
import os
import tweepy
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_login import LoginManager



#basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the Flask app
app = Flask(__name__)

# Initialize Flask_Bootstrap for the app
Bootstrap(app)


# open json for parsing
MONGO_CLIENT = json.load(open('mongo_conf.json', 'r+'))

# App configurations
app.config['MONGOALCHEMY_DATABASE'] = MONGO_CLIENT['db_name']
app.config['MONGO_URI'] = MONGO_CLIENT['uri']
app.config['SECRET_KEY'] = '\x02\x84\x84\x88\x04\xe8.\x05\xe3\x99Fl\xc6\xd8\xce\xc1\xb2\xb9"\xe2\xc7^,\x11'

# Twitter authentication
# ckey = 'SfR10L97q4Soh6v7wii2vnShR'
# csecret = 'TINPY6L5pWFAW3zFKQz2T9WymDa1jVQD2az3Ym98eVgsPB43kI'
# atoken = '2568096792-wXQQYF3Uzl0u8utbFefHz33iNVx7gR30JADX20Z'
# asecret = 'JdsZjVStdH1QYm5P9CnzWPUXzjMF1CRlatLZXojYC3QWW'
# auth = tweepy.OAuthHandler(ckey, csecret)
# auth.set_access_token(atoken, asecret)
# api = tweepy.API(auth)
#  Client Keys
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypass@104.154.39.105:3306/kabombdi'

# Initialize database for app
db = PyMongo(app)

import views