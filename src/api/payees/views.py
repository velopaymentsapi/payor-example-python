from flask import jsonify, Blueprint, Response, render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
import os
from flask import current_app as app
import velo_payments
from velo_payments.rest import ApiException
from flask_jwt_extended import jwt_required

mod = Blueprint('payees', __name__)

@mod.route('/payees', methods=['GET', 'POST'])
@jwt_required
def list_or_create():
    if request.method == 'GET':
        configuration = velo_payments.Configuration()
        configuration.access_token = app.config['VELO_API_ACCESSTOKEN']
        configuration.host = os.environ.get("VELO_BASE_URL")

        api_instance = velo_payments.PayeesApi(velo_payments.ApiClient(configuration))
        payor_id = os.environ.get("VELO_API_PAYORID")
        try:
            api_response = api_instance.list_payees_v3(payor_id)
            print(api_response)
        except ApiException as e:
            print("Exception when calling PayeesApi->list_payees_v3: %s\n" % e)
    elif request.method == 'POST':
        pass
    
    return jsonify({})

@mod.route('/payees/<string:payee_id>', methods=['GET'])
@jwt_required
def get_payee(payee_id):
   
    return jsonify({})

@mod.route('/payees/<string:payee_id>/invite', methods=['POST'])
@jwt_required
def resend_payee_invite(payee_id):
    return jsonify({})