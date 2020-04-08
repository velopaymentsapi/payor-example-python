from flask import jsonify, Blueprint, Response, render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
import os, decimal
from flask import current_app as app
import velo_payments
from velo_payments.rest import ApiException
from flask_jwt_extended import jwt_required, get_jwt_identity

mod = Blueprint('settings', __name__)

@mod.route('/settings', methods=['GET'])
@jwt_required
def velo_payor_info():
    configuration = velo_payments.Configuration()
    configuration.access_token = app.config['VELO_API_ACCESSTOKEN']
    configuration.host = os.environ.get("VELO_BASE_URL")

    api_instance = velo_payments.PayorsApi(velo_payments.ApiClient(configuration))
    payor_id = os.environ.get("VELO_API_PAYORID")
    try:
        api_response = api_instance.get_payor_by_id_v2(payor_id)
    except ApiException as e:
        print("Exception when calling PayorsApi->get_payor_by_id_v2: %s\n" % e)

    res = {}
    a = {}
    a['city'] = api_response.address.city
    a['country'] = api_response.address.country
    a['county_or_province'] = api_response.address.county_or_province
    a['line1'] = api_response.address.line1
    a['line2'] = api_response.address.line2
    a['line3'] = api_response.address.line3
    a['line4'] = api_response.address.line4
    a['zip_or_postcode'] = api_response.address.zip_or_postcode
    res['address'] = a
    res['allows_language_choice'] = api_response.allows_language_choice
    res['collective_alias'] = api_response.collective_alias
    res['dba_name'] = api_response.dba_name
    res['includes_reports'] = api_response.includes_reports
    res['kyc_state'] = api_response.kyc_state
    res['language'] = api_response.language
    res['manual_lockout'] = api_response.manual_lockout
    res['max_master_payor_admins'] = api_response.max_master_payor_admins
    res['payee_grace_period_days'] = api_response.payee_grace_period_days
    res['payee_grace_period_processing_enabled'] = api_response.payee_grace_period_processing_enabled
    res['payment_rails'] = api_response.payment_rails
    res['payor_id'] = api_response.payor_id
    res['payor_name'] = api_response.payor_name
    res['primary_contact_email'] = api_response.primary_contact_email
    res['primary_contact_name'] = api_response.primary_contact_name
    res['primary_contact_phone'] = api_response.primary_contact_phone
    res['reminder_emails_opt_out'] = api_response.reminder_emails_opt_out
    res['support_contact'] = api_response.support_contact
    res['wu_customer_id'] = api_response.wu_customer_id

    return jsonify(res)

@mod.route('/settings/accounts', methods=['GET'])
@jwt_required
def velo_source_accounts():
    configuration = velo_payments.Configuration()
    configuration.access_token = app.config['VELO_API_ACCESSTOKEN']
    configuration.host = os.environ.get("VELO_BASE_URL")

    api_instance = velo_payments.FundingManagerApi(velo_payments.ApiClient(configuration))
    payor_id = os.environ.get("VELO_API_PAYORID")
    
    try:
        api_response = api_instance.get_source_accounts_v2(payor_id=payor_id)
    except ApiException as e:
        print("Exception when calling FundingManagerApi->get_source_accounts_v2: %s\n" % e)

    res = {}
    c = []
    for con in api_response.content:
        atuc = {}
        catuc = con.auto_top_up_config
        atuc['enabled'] = catuc.enabled
        atuc['min_balance'] = catuc.min_balance
        atuc['target_balance'] = catuc.target_balance
        arc = {}
        arc['auto_top_up_config'] = atuc
        arc['balance'] = con.balance
        arc['balance_visible'] = con.balance_visible
        arc['currency'] = con.currency
        arc['customer_id'] = con.customer_id
        arc['funding_account_id'] = con.funding_account_id
        arc['funding_ref'] = con.funding_ref
        arc['id'] = con.id
        arc['name'] = con.name
        nots = {}
        nots['minimum_balance'] = con.notifications.minimum_balance
        arc['notifications'] = nots
        arc['payor_id'] = con.payor_id
        arc['physical_account_id'] = con.physical_account_id
        arc['physical_account_name'] = con.physical_account_name
        arc['pooled'] = con.pooled
        arc['rails_id'] = con.rails_id
        c.append(arc)
    l = []
    for lin in api_response.links:
        arl = {}
        arl['href'] = lin.href
        arl['rel'] = lin.rel
        l.append(arl)
    p = {}
    p['number_of_elements'] = api_response.page.number_of_elements
    p['page'] = api_response.page.page
    p['page_size'] = api_response.page.page_size
    p['total_elements'] = api_response.page.total_elements
    p['total_pages'] = api_response.page.total_pages
    
    res['content'] = c
    res['links'] = l
    res['page'] = p

    return jsonify(res)

@mod.route('/settings/fundings', methods=['POST'])
@jwt_required
def velo_fund_account():
    content = request.json
    
    configuration = velo_payments.Configuration()
    configuration.access_token = app.config['VELO_API_ACCESSTOKEN']
    configuration.host = os.environ.get("VELO_BASE_URL")

    api_instance = velo_payments.FundingManagerApi(velo_payments.ApiClient(configuration))
    source_account_id = content['source_account']
    funding_request_v1 = velo_payments.FundingRequestV1(amount=content['amount'])
    
    try:
        api_instance.create_ach_funding_request(source_account_id, funding_request_v1)
    except ApiException as e:
        print("Exception when calling FundingManagerApi->create_ach_funding_request: %s\n" % e)

    return jsonify({})

@mod.route('/settings/countries', methods=['GET'])
def velo_countries():
    configuration = velo_payments.Configuration()
    configuration.host = os.environ.get("VELO_BASE_URL")

    api_instance = velo_payments.CountriesApi(velo_payments.ApiClient(configuration))

    try:
        api_response = api_instance.list_supported_countries()
    except ApiException as e:
        print("Exception when calling CountriesApi->list_supported_countries: %s\n" % e)
    
    res = []
    for country in api_response.countries:
        c = {}
        c['currencies'] = country.currencies
        c['iso_country_code'] = country.iso_country_code
        ra =[]
        for region in country.regions:
            r = {}
            r['abbreviation'] = region.abbreviation
            r['name'] = region.name
            ra.append(r)
        c['regions'] = ra
        res.append(c)
    
    return jsonify(res)

@mod.route('/settings/currencies', methods=['GET'])
def velo_currencies():
    configuration = velo_payments.Configuration()
    configuration.host = os.environ.get("VELO_BASE_URL")

    api_instance = velo_payments.CurrenciesApi(velo_payments.ApiClient(configuration))
    
    try:
        api_response = api_instance.list_supported_currencies()
    except ApiException as e:
        print("Exception when calling CurrenciesApi->list_supported_currencies: %s\n" % e)

    res = []
    for currency in api_response.currencies:
        c = {}
        c['currency'] = currency.currency
        c['max_payment_amount'] = currency.max_payment_amount
        res.append(c)

    return jsonify(res)