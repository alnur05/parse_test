# auth_facebook.py
from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
from facebook_business.api import FacebookAdsApi

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'

    oauth = OAuth(app)

    # Замените значения YOUR_APP_ID и YOUR_APP_SECRET на значения из вашего Facebook App
    facebook = oauth.remote_app(
        'facebook',
        consumer_key='323958937015510',
        consumer_secret='4017320d9d5dcc49869874e73904b872',
        request_token_params={'scope': 'email'},
        base_url='https://graph.facebook.com',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='/oauth/access_token',
        authorize_url='https://www.facebook.com/dialog/oauth'
    )

    @app.route('/')
    def index():
        return 'Добро пожаловать! <a href="/login">Войти с использованием Facebook</a>'

    @app.route('/login')
    def login():
        return facebook.authorize(callback=url_for('authorized', _external=True))

    @app.route('/logout')
    def logout():
        session.pop('facebook_token', None)
        return redirect(url_for('index'))

    @app.route('/login/authorized')
    def authorized():
        response = facebook.authorized_response()

        if response is None or response.get('access_token') is None:
            return 'Доступ запрещен: причина = {}, ошибка = {}'.format(
                request.args['error_reason'],
                request.args['error_description']
            )

        session['facebook_token'] = (response['access_token'], '')
        user_data = facebook.get('/me')

        return 'Добро пожаловать, {}'.format(user_data.data['name'])

    @facebook.tokengetter
    def get_facebook_oauth_token():
        return session.get('facebook_token')

    return app