from flask import Flask, jsonify, Response, request, make_response, render_template
from flask_cors import CORS
from connect import Connect
from pymongo import MongoClient
from pprint import pprint
from bson import json_util, ObjectId
import json
import os

# Getting static asset
WHERE_FOLDER = os.path.join('static', 'where/casual')

# instantiate db connection
connection = Connect.get_connection()
db = connection.Elizabeth_DB

# config
DEBUG = True

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = WHERE_FOLDER

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/footer', methods=['GET'])
def get_footer():    
    response_object = db.footerCollection.find_one()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/footer/<object_id>', methods=['PUT'])
def update_footer(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    db.footerCollection.update(
        {'_id': ObjectId(object_id)},
        post_data
    )
    return jsonify(response_object)

@app.route('/home', methods=['GET'])
def get_home():
    response_object = db.homeCollection.find_one()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/home/<object_id>', methods=['PUT'])
def update_home(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    db.homeCollection.update(
        {'_id': ObjectId(object_id)},
        {'$set': {post_data["ref"]: post_data}}
    )
    return jsonify(response_object)

@app.route('/about_us', methods=['GET'])
def get_about_us():
    response_object = db.aboutUsCollection.find_one()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/about_us/<object_id>', methods=['PUT'])
def update_about_us(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    db.aboutUsCollection.update(
        {'_id': ObjectId(object_id)},
        post_data
    )
    return jsonify(response_object)

@app.route('/where', methods=['GET'])
def where():
    response_object = db.whereCollection.find_one()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/where/<object_id>', methods=['PUT'])
def update_where(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    db.whereCollection.update(
        {'_id': ObjectId(object_id)},
        {'$set': {post_data["ref"]: post_data}}
    )
    return jsonify(response_object)

@app.route('/style', methods=['GET'])
def get_style():
    response_object = db.styleCollection.find_one()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/style/<object_id>', methods=['PUT'])
def update_style(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    db.styleCollection.update(
        {'_id': ObjectId(object_id)},
        post_data
    )
    return jsonify(response_object)

@app.route('/measurement', methods=['GET'])
def get_measurement():
    response_object = db.measurementCollection.find_one()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/contact_us', methods=['GET'])
def get_contact_us():
    pipeline = [
            {
                '$lookup': {
                    'from': 'footerCollection', 
                    'localField': 'string', 
                    'foreignField': 'string', 
                    'as': 'contactInfo'
                }
            }, {
                '$project': {
                    'keepInTouch.contactInfo': False,
                    'contactInfo._id': False
                }
            }
        ]
    response_object = list(db.contactCollection.aggregate(pipeline))[0]
    # pprint(json.dumps(response_object, default=json_util.default))
    # return jsonify(response_object)
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/contact_us/<object_id>', methods=['PUT'])
def update_contact_us(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    pprint(post_data)
    db.contactCollection.update(
        {'_id': ObjectId(object_id)},
        {
            '$set': {
                'header': post_data.get('header'),
                'subheader': post_data.get('subheader'),
                'calendlyApi': post_data.get('calendlyApi'),
                'keepInTouch': {
                    'header': post_data.get('keepInTouch').get('header'),
                    'subheading': post_data.get('keepInTouch').get('subheading')
                }
            }
        }
    )
    return jsonify(response_object)

@app.route('/get_customers', methods=['GET'])
def get_customers():
    response_object = db.userCollection.find()
    return Response(
        json_util.dumps(response_object),
        mimetype='application/json'
    )

@app.route('/adduser', methods=['PUT'])
def add_user():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    pprint(post_data)
    db.userCollection.insert_one(post_data)
    return jsonify(response_object)

@app.route('/update_customer', methods=['PUT'])
def update_customer():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    # pprint(post_data.get("_id").get("$oid"))
    db.userCollection.update(
        {'_id': ObjectId(post_data.get("_id").get("$oid"))},
        {
            '$set': {
                'notes': post_data.get('notes')
            }
        }
    )
    return jsonify(response_object)

@app.route('/test', methods=['GET'])
def hello():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '1.jpg')
    return render_template("index.html", user_image = full_filename)

if __name__ == '__main__':
    app.run()