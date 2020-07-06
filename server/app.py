from flask import Flask, jsonify, request
from flask_cors import CORS

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

    response_object = {
        'info': {
            'mobile': '(64)22 123 4567',
            'email': 'ebdesign@gmail.com',
            'address': 'Auckland, New Zealand'
        },
        'links': {
            'facebook': 'https://www.facebook.com/cuciocj',
            'instagram': 'https://www.instagram.com/cuciocj',
            'twitter': 'https://www.twitter.com/cuciocj'
        }
    }
    
    return jsonify(response_object)

@app.route('/home', methods=['GET'])
def get_home():

    response_object = {
        'welcome_jumbotron': {
            'header': 'Elizabeth by Design',
            'subheader': 'Welcome to Elizabeth by Design,' 
                + ' where we work with you to create your perfect outfit,' 
                + ' whether it be for casual, formal or work.'
        }
    }

    return jsonify(response_object)

@app.route('/test', methods=['GET'])
def hello():
    return jsonify('hello world!')

if __name__ == '__main__':
    app.run()