from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def test():
    return jsonify({"message" : "test ok"})

import api.routes.stock
import api.routes.user
import api.routes.porveedor