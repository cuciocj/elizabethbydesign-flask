from flask import Flask, jsonify, Response, request, make_response, render_template
from flask_cors import CORS
from connect import Connect
from pymongo import MongoClient
from pprint import pprint
from bson import json_util, ObjectId
import json
import os

# instantiate db connection
connection = Connect.get_connection()
db = connection.Elizabeth_DB

# config
DEBUG = True

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

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
        {'$set': {post_data["ref"] : post_data["tab"]}}
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

@app.route('/measurement/<object_id>', methods=['PUT'])
def update_measurement(object_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    db.measurementCollection.update(
        {'_id': ObjectId(object_id)},
        {'$set': {post_data["ref"]: post_data}}
    )
    return jsonify(response_object)

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
    db.userCollection.update(
        {'_id': ObjectId(post_data.get("_id").get("$oid"))},
        {
            '$set': {
                'notes': post_data.get('notes')
            }
        }
    )
    return jsonify(response_object)

@app.route('/imgs', methods=['POST'])
def imgs():
    dir = request.form['dir']
    if request.files:
        for file in request.files:
            img = request.files[file]
            try:
                img.save(os.path.join("static/where",dir,file + ".jpg"))
            except:
                os.makedirs("static/where/" + dir)
                img.save(os.path.join("static/where",dir,file + ".jpg"))
    
    return jsonify("done")
    

if __name__ == '__main__':
    app.run()