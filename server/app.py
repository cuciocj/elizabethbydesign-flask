from flask import Flask, jsonify, request
from flask_cors import CORS

# config
DEBUG = True

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# test endpoint
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify('hello world!')

if __name__ == '__main__':
    app.run()