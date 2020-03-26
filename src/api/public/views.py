from flask import jsonify, Blueprint

mod = Blueprint('public', __name__)

@mod.route('/', methods=['GET'])
def index():
    return jsonify('payor api index')
