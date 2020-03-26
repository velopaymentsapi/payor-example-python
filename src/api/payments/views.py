from flask import jsonify, Blueprint, Response, render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
import os
from flask import current_app as app
import velo_payments
from velo_payments.rest import ApiException
from flask_jwt_extended import jwt_required

mod = Blueprint('payments', __name__)

@mod.route('/payments', methods=['POST'])
@jwt_required
def create_payment():
    return jsonify({})

@mod.route('/payments//<string:payment_id>', methods=['PUT', 'DELETE'])
@jwt_required
def update_delete_payment(payment_id):
    return jsonify({})

@mod.route('/payments//<string:payment_id>', methods=['GET'])
@jwt_required
def get_payment(payment_id):
    return jsonify({})