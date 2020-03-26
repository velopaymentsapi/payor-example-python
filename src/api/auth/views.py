from flask import jsonify, Blueprint, request
from datetime import datetime, timedelta
import os
from api.auth.models import User
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt

mod = Blueprint('auth', __name__)

@mod.route('/auth/login', methods=['POST'])
def auth():
    content = request.json
    u = User.query.filter_by(username=content['username']).first_or_404()

    bcrypt = Bcrypt()
    if not bcrypt.check_password_hash(u.password, content['password']):
        return jsonify("invalid credentials"), 401
    expires = timedelta(hours=4)
    access_token = create_access_token(identity=u.api_key, expires_delta=expires)
    return jsonify({"token":access_token})
