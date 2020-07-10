from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from connect import Connect
from pymongo import MongoClient
from pprint import pprint

connection = Connect.get_connection()
db = connection.Elizabeth_DB

# config
DEBUG = True

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# TODO: get data from db
@app.route('/footer', methods=['GET'])
def get_footer():    
    response_object = db.footerCollection.find_one({}, {"_id": 0})
    return jsonify(response_object)

@app.route('/home', methods=['GET'])
def get_home():
    response_object = db.homeCollection.find_one({}, {"_id": 0})
    return jsonify(response_object)

@app.route('/test', methods=['GET'])
def hello():
    return jsonify("hello world")

if __name__ == '__main__':
    app.run()