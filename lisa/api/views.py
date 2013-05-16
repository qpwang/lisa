# -*- coding: utf-8 -*-
import requests
from uuid import uuid4
from django.utils import simplejson as json
from lisa.util.json import json_response_ok, json_response_error
from lisa.util.respcode import PARAM_REQUIRED, ERROR_MESSAGE, DATA_ERROR
from lisa.decorator import user_auth
from lisa.api.models import User, Secret, ThirdPartySource


def profiles(request):
    data = request.POST

    access_token = data.get('access_token')
    if not access_token:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'access_token'))

    uid = int(data.get('uid'))
    if not uid: 
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'uid'))

    user_name = data.get('username')
    if not user_name:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'username'))

    email = data.get('email')
    if not email:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'email'))

    source = data.get('source')
    if not source:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'source'))

    try:
        source_id = _access_token(access_token, uid, source)
        if not source_id:
            return json_response_error(DATA_ERROR, 'access_token failed')
        user = _get_user(user_name, source_id, email)
    except Exception, e:
        return json_response_error(DATA_ERROR,
                '%s: %s' % (ERROR_MESSAGE[DATA_ERROR], e))

    result = {'token': user.token}

    return json_response_ok(result)


def _get_user(user_name, source_id, email):
    user = User.objects.filter(source_id=source_id).filter(email=email).all()
    if not user:
        user = User()
        user.user_name = user_name
        user.source_id = source_id
        user.token = uuid4()
        user.email = email
        user.school_id = 1
        user.status = 0
        user.save()
    else:
        user = user[0]
    return user


def _access_token(access_token, uid, source):
    third_party_source = ThirdPartySource.objects.get(name=source)
    if source == 'sina':
        post_dict = {
                'access_token': access_token,
            }
        api = '%s?access_token%s' % (third_party_source.api, access_token)
    elif source == 'renren':
        post_dict = {
                'access_token': access_token,
                'v': '1.0',
                'format': 'json',
            }
    response = requests.post(api, post_dict)
    result = json.loads(response.content)
    if result.get('uid') == uid:
        return third_party_source.id


@user_auth
def all_secrets(request):
    data = request.REQUEST
    page = int(data.get('page', 1))

    start = 20 * (page - 1)

    secrets = Secret.objects.all()[start:start+20]

    return json_response_ok(secrets)


@user_auth
def add_secrets(request, school_id):
    user = request.META['user']
    data = request.POST
    content = data.get('content')
    return json_response_ok(school_id)


def get_secrets(request):
    #TODO
    pass
