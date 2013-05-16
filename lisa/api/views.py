# -*- coding: utf-8 -*-
import requests
from uuid import uuid4
from django.utils import simplejson as json
from lisa.util.json import json_response_ok, json_response_error
from lisa.util.respcode import PARAM_REQUIRED, ERROR_MESSAGE, DATA_ERROR
from lisa.decorator import user_auth
from lisa.api.models import User, Secret, ThirdPartySource, Comment
from util.utils import datetime_to_timestamp


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
    size = int(data.get('size', 20))

    size = min(size, 1000)

    start = size * (page - 1)

    secrets = Secret.objects.all()[start:start+size]

    result = {'secrets': []}
    for secret in secrets:
        result['secrets'].append({
                'id': secret.id,
                'content': secret.content,
                'time': datetime_to_timestamp(secret.create_time),
            })

    return json_response_ok(result)


@user_auth
def add_secrets(request, school_id):
    data = request.POST
    content = data.get('content')
    if not content:
        return json_response_error(PARAM_REQUIRED, 'content')

    user = request.META['user']

    try:
        secret = _add_secret(user, school_id, content)
    except Exception, e:
        return json_response_error(DATA_ERROR, e)

    result = {
            'id': secret.id,
            'time': datetime_to_timestamp(secret.create_time),
            }

    return json_response_ok(result)


def _add_secret(user, school_id, content):
    secret = Secret()
    secret.content = content
    secret.author_id = user.id
    secret.school_id = school_id
    secret.status = 0
    secret.save()
    return secret

@user_auth
def secrets(request, school_id):
    data = request.POST
    page = int(data.get('page', 1))
    size = int(data.get('size', 20))

    size = min(size, 1000)

    start = size * (page - 1)

    secrets = Secret.objects.filter(school_id=school_id).all()[start:start+size]

    result = {'secrets': []}
    for secret in secrets:
        result['secrets'].append({
                'id': secret.id,
                'content': secret.content,
                'time': datetime_to_timestamp(secret.create_time),
            })

    return json_response_ok(result)


@user_auth
def add_comments(request, secret_id):
    data = request.POST
    content = data.get('content')
    if not content:
        return json_response_error(PARAM_REQUIRED, 'content')

    reply_to = data.get('reply_to')

    user = request.META['user']

    new_comment = Comment.objects.filter(secret_id=secret_id).order_by('-floor').all()
    if new_comment:
        floor = new_comment[0].floor + 1
    else:
        floor = 1
   
    try:
        comment = Comment()
        comment.content = content
        comment.author_id = user.id
        comment.secret_id = secret_id
        comment.reply_to_id = reply_to
        comment.floor = floor
        comment.save()
    except Exception, e:
        return json_response_error(DATA_ERROR, e)

    result = {
            'id': comment.id,
            'time': datetime_to_timestamp(comment.create_time),
            'floor': floor,
            }

    return json_response_ok(result)


@user_auth
def comments(request, secret_id):
    data = request.POST
    page = int(data.get('page', 1))
    size = int(data.get('size', 20))

    size = min(size, 1000)

    start = size * (page - 1)

    comments = Comment.objects.filter(secret_id=secret_id).all()[start:start+size]

    result = {'comments': []}

    for comment in comments:
        if comment.reply_to_id:
            replied_floor = Comment.objects.get(id=comment.reply_to_id).floor
            result['comments'].append({
                    'id': comment.id,
                    'content': comment.content,
                    'time': datetime_to_timestamp(comment.create_time),
                    'floor': comment.floor,
                    'replied_floor': replied_floor,
                })
        else:
            result['comments'].append({
                    'id': comment.id,
                    'content': comment.content,
                    'time': datetime_to_timestamp(comment.create_time),
                    'floor': comment.floor,
                })

    return json_response_ok(result)



def get_secrets(request):
    #TODO
    pass
