from app import app
from flask import redirect, request, abort, session, render_template, url_for
import requests
import random
from app.functions import check_bearer_token, get_client_id

app_client_id = app.config["APP_CLIENT_ID"]
app_client_secret = app.config["APP_CLIENT_SECRET"]
app_redirect_uri = app.config["REDIRECT_AUTHORIZED_URL"]
base_site_url = app.config["BASE_SITE_URL"]
base_api_url = app.config["BASE_API_URL"]

@app.route('/')
@app.route('/index')
def index():
    return redirect(base_site_url + f'oauth/authorize?response_type=code&client_id={app_client_id}&redirect_uri={app_redirect_uri}&scope=all')

@app.route('/authorized')
def authorized():
    if request.args.get('code', None) is None:
        return abort(401)

    data_request = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': app_redirect_uri,
        'client_id': app_client_id,
        'client_secret': app_client_secret
    }

    headers_request = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_response = requests.post(base_site_url + 'oauth/token', 
                                   data=data_request, 
                                   headers=headers_request).json()


    
    if token_response.get('access_token', None) is None:
        return url_for('index')

    access_token = token_response['access_token']

    session['access_token'] = access_token

    return render_template('list_possibilities.html')

@app.route('/extlist')
def extlist():
    if check_bearer_token(session) is False:
        return abort(401)
    
    bearer_token = session.get('access_token')

    client_id = get_client_id(base_api_url, bearer_token)
    if client_id is None:
        return abort(500)
    
    if session.get('client_id', None) is None:
        session['client_id'] = client_id

    extlist = requests.get(base_api_url + f'client/{session["client_id"]}/extension', 
                           headers={'Authorization': f'Bearer {bearer_token}'})
    return extlist.json()

@app.route('/randomext')
def randomext():
    if check_bearer_token(session) is False:
        return abort(401)
    
    bearer_token = session.get('access_token')

    client_id = get_client_id(base_api_url, bearer_token)
    if client_id is None:
        return abort(500)
    
    if session.get('client_id', None) is None:
        session['client_id'] = client_id

    extlist_response = requests.get(base_api_url + f'client/{session["client_id"]}/extension', 
                                      headers={'Authorization': f'Bearer {bearer_token}'}
                                      ).json()

    return random.choice(extlist_response) #рандомный элемент из массива

@app.route('/logout')
def logout():
    session.clear()
    return redirect('index')