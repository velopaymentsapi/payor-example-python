from api import create_app
from flask import Blueprint
from flask import current_app as app
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
import velo_payments
from velo_payments.rest import ApiException

app = create_app()

def refreshVeloOAuth():
    # Check if OAuth2 token is about to expire ... if so .. issue event to refresh it
    # grab the VELO_API_ACCESSTOKENEXPIRATION from django.constance
    # if now is >= VELO_API_ACCESSTOKENEXPIRATION ... call api and update configs with access_token & expires_in
    # when updating expiration be sure to remove 5 mins (300 sec) off of expires_in
    now_int = int(time.time())
    if int(app.config['VELO_API_ACCESSTOKENEXPIRATION']) <= now_int:
        print('CALL VELO API TO REFRESH TOKEN')
        configuration = velo_payments.Configuration()
        configuration.username = os.environ.get("VELO_API_APIKEY")
        configuration.password = os.environ.get("VELO_API_APISECRET")
        configuration.host = os.environ.get("VELO_BASE_URL")
        grant_type = 'client_credentials'

        try:
            # Authentication endpoint
            api_instance = velo_payments.LoginApi(velo_payments.ApiClient(configuration))
            api_response = api_instance.velo_auth(grant_type=grant_type)
            print(api_response)
            app.config['VELO_API_ACCESSTOKEN'] = api_response.access_token
            app.config['VELO_API_ACCESSTOKENEXPIRATION'] = (now_int + int(api_response.expires_in)) - 300
            print("new velo oauth2 token expires at: %s\n" % app.config['VELO_API_ACCESSTOKENEXPIRATION'])
        except ApiException as e:
            print("Exception when calling AuthApi->velo_auth: %s\n" % e)
    else:
        print("velo oauth token has not expired")

scheduler = BackgroundScheduler()
scheduler.add_job(refreshVeloOAuth, 'interval', minutes=1)
scheduler.start()

refreshVeloOAuth()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)