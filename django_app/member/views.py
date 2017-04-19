from pprint import pprint

import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from facebook import settings


def login_fbv(request):
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id,
    }
    return render(request, 'member/login.html', context)


def logout_fbv(request):
    logout(request)
    return redirect('index')


def login_facebook(request):
    APP_ID = settings.config['facebook']['app_id']
    SECRET_CODE = settings.config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE
    )

    # redirect uri를 이용해 다시 login_facebook으로 돌아온 후의 동작
    if request.GET.get('code'):
        code = request.GET.get('code')

        # 전달받은 code값을 이용해 access token 요청
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token'
        params = {
            'client_id': APP_ID,
            'redirect_uri': REDIRECT_URI,
            'client_secret': SECRET_CODE,
            'code': code,
        }

        r = requests.get(url_request_access_token, params=params)
        dict_access_token = r.json()
        print(dict_access_token)
        USER_ACCESS_TOKEN = dict_access_token['access_token']
        print('ACCESS TOKEN : %s' % USER_ACCESS_TOKEN)
        print('code : %s' % code)

        # 유저 액세스 토큰과 앱 엑세스 토큰을 사용해서 토큰 검증 : debug token 요청
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params = {
            'scopes': 'public_profile, email',
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN,
        }

        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        pprint(dict_debug_token)
        USER_ID = dict_debug_token['data']['user_id']
        print('USER ID: %s' % USER_ID)

        # 해당 USER_ID 로 graph API에 유저정보를 요청
        url_api_user = 'https://graph.facebook.com/{user_id}'.format(
            user_id=USER_ID
        )
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'picture',
            'email'
        ]
        params = {
            'fields': ','.join(fields),
            'access_token': USER_ACCESS_TOKEN
        }
        r = requests.get(url_api_user, params)
        dict_user_info = r.json()
        pprint(dict_user_info)

        # 페이스북 유저 아이디만으로 인증
        user = authenticate(facebook_id=USER_ID, extra_fields=dict_user_info)
        login(request, user)
        return redirect('index')
