# -*- coding: utf-8 -*-
from django.utils import simplejson as json
from lisa.util.json import json_response_ok, json_response_error
from lisa.util.respcode import PARAM_REQUIRED, ERROR_MESSAGE, DATA_ERROR
from lisa.decorator import user_auth
from lisa.api.models import User, Secret, ThirdPartySource, Comment, Notice, UpdateInfo
from util.utils import datetime_to_timestamp


def profiles(request):
    data = request.POST

    access_token = data.get('access_token')
    if not access_token:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'access_token'))

    uid = data.get('uid')
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
        uid = int(uid)
        source_id = ThirdPartySource._access_token(access_token, uid, source)
        if not source_id:
            return json_response_error(DATA_ERROR, 'access_token failed')
        user = User._get_user(user_name, source_id, email)
    except Exception, e:
        return json_response_error(DATA_ERROR,
                '%s: %s' % (ERROR_MESSAGE[DATA_ERROR], e))

    result = {'token': user.token}

    return json_response_ok(result)


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
        secret = Secret._add_secret(user, school_id, content)
    except Exception, e:
        return json_response_error(DATA_ERROR, e)

    result = {
            'id': secret.id,
            'time': datetime_to_timestamp(secret.create_time),
            }

    return json_response_ok(result)


@user_auth
def secrets(request, school_id):
    data = request.POST
    page = int(data.get('page', 1))
    size = int(data.get('size', 20))

    size = min(size, 1000)

    start = size * (page - 1)

    secrets = Secret.objects.filter(school_id=school_id).order_by('-id').all()[start:start+size]

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
        if reply_to:
            reply_to = int(reply_to)
            replied_comment = Comment.objects.get(id=reply_to)
            receive_user_id = replied_comment.author_id
            comment = Comment._add_comment(content, user.id, secret_id, reply_to, floor)
            Notice._add_notice(receive_user_id, comment)
        else:
            comment = Comment._add_comment(content, user.id, secret_id, reply_to, floor)
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


@user_auth
def mine(request):
    data = request.POST
    page = int(data.get('page', 1))
    size = int(data.get('size', 20))

    size = min(size, 1000)

    start = size * (page - 1)

    user = request.META['user']

    secrets = Secret.objects.filter(author_id=user.id).order_by('-id').all()[start:start+size]

    result = {'secrets': []}

    for secret in secrets:
        result['secrets'].append({
            'id': secret.id,
            'time': datetime_to_timestamp(secret.create_time),
            'content': secret.content,
            'school_id': secret.school_id,
        })

    return json_response_ok(result)


@user_auth
def notice(request):
    data = request.POST
    page = int(data.get('page', 1))
    size = int(data.get('size', 20))

    size = min(size, 1000)

    start = size * (page - 1)

    user = request.META['user']

    notices = Notice.objects.filter(receive_user_id=user.id).filter(status=0).order_by('-id').all()[start:start+size]

    result = {'notices': []}

    for notice in notices:
        try:
            reply_id = notice.comment_id
            comment = Comment.objects.get(id=reply_id)
            secret = Secret.objects.get(id=comment.secret_id)
            if comment.reply_to_id:
                replied_content = Comment.objects.get(id=comment.reply_to_id).content
                result['notices'].append({
                    'id': notice.id,
                    'replied_content': replied_content,
                    'secret': {
                        'id': secret.id,
                        'school_id': secret.school_id,
                        'content': secret.content,
                        'time': datetime_to_timestamp(secret.create_time),
                    },
                    'reply_content': comment.content,
                })
            else:
                result['notices'].append({
                    'id': notice.id,
                    'secret': {
                        'id': secret.id,
                        'school_id': secret.school_id,
                        'content': secret.content,
                        'time': datetime_to_timestamp(secret.create_time),
                    },
                    'reply_content': comment.content,
                })
        except Exception, e:
            return json_response_error(DATA_ERROR, e)

    return json_response_ok(result)



@user_auth
def notice_delete(request):
    data = request.POST
    id_list = data.get('id_list')
    if not id_list:
        return json_response_error(PARAM_REQUIRED, 'id_list')

    try:
        id_list = json.loads(id_list)
        Notice.objects.filter(id__in=id_list).all().update(status=1)
    except Exception, e:
        return json_response_error(DATA_ERROR, e)

    return json_response_ok()


def update(request):
    update_info = UpdateInfo.objects.order_by('-update_time').all()
    if update_info:
        update_info = update_info[0]
        result = {
            'version': update_info.version,
            'content': update_info.content,
            'url': update_info.url,
            'flag': update_info.flag,
            'update_time': datetime_to_timestamp(update_info.update_time),
        }
        return json_response_ok(result)
    else:
        return json_response_ok()



