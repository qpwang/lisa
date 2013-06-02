# -*- coding: utf-8 -*-
from django.utils import simplejson as json
from lisa.util.json import json_response_ok, json_response_error
from lisa.util.respcode import PARAM_REQUIRED, ERROR_MESSAGE, DATA_ERROR
from lisa.decorator import user_auth
from lisa.api.models import (User, Secret, ThirdPartySource, Comment,
                             Notice, Group, GroupUserRelation)
from lisa.api.consts import *
from lisa.util.utils import datetime_to_timestamp, timestamp_to_datetime


@user_auth
def group(request):
    data = request.POST
    category = data.get('category')
    if not category:
        return json_response_error(PARAM_REQUIRED, 'category')

    try:
        groups = Group.objects.filter(category=int(category)).all()
    except Exception as e:
        return json_response_error(DATA_ERROR, e)

    result = []
    for group in groups:
        result.append({
            'id': group.id,
            'name': group.name,
            'pinyin': group.pinyin,
            'py_first': group.py_first,
        })
    return json_response_ok(result)


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

    source = data.get('source')
    if not source:
        return json_response_error(PARAM_REQUIRED,
                                   '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'source'))

    try:
        source_id = ThirdPartySource._access_token(access_token, uid, source)
        if not source_id:
            return json_response_error(DATA_ERROR, 'access_token failed')
        user = User._get_user(user_name, uid, source_id)
    except Exception as e:
        return json_response_error(DATA_ERROR,
                                   '%s: %s' % (ERROR_MESSAGE[DATA_ERROR], e))

    result = {'token': user.token}

    return json_response_ok(result)


def sample(request):
    size = 20
    secrets = Secret.objects.order_by('-id').all()[:size]

    result = {'secrets': []}
    for secret in secrets:
        hot = Comment.objects.filter(secret_id=secret.id).count()
        result['secrets'].append({
            'id': secret.id,
            'content': secret.content,
            'group_id': secret.group_id,
            'hot': hot,
            'time': datetime_to_timestamp(secret.create_time),
        })

    return json_response_ok(result)


@user_auth
def all_secrets(request):
    data = request.POST
    size = data.get('size', 50)
    timestamp = data.get('time')
    if not timestamp:
        return json_response_error(PARAM_REQUIRED, 'time')
    time_type = data.get('type', 'after')
    if time_type not in ['before', 'after']:
        return json_response_error(PARAM_REQUIRED, 'type')

    try:
        size = int(size)
        timestamp = int(timestamp)

        size = min(size, 100)

        if time_type == 'before':
            secrets = Secret.objects.filter(
                create_time__lt=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]
        else:
            secrets = Secret.objects.filter(
                create_time__gte=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]
    except Exception, e:
        return json_response_error(DATA_ERROR, e)

    result = {'secrets': []}
    for secret in secrets:
        hot = Comment.objects.filter(secret_id=secret.id).count()
        result['secrets'].append({
            'id': secret.id,
            'content': secret.content,
            'group_id': secret.group_id,
            'hot': hot,
            'time': datetime_to_timestamp(secret.create_time),
        })

    return json_response_ok(result)


@user_auth
def my_secrets(request):
    data = request.POST
    size = data.get('size', 50)
    timestamp = data.get('time')
    if not timestamp:
        return json_response_error(PARAM_REQUIRED, 'time')
    time_type = data.get('type', 'after')
    if time_type not in ['before', 'after']:
        return json_response_error(PARAM_REQUIRED, 'type')

    user = request.META['user']

    try:
        size = int(size)
        timestamp = int(timestamp)

        size = min(size, 100)


        group_ids = [
            relation.group_id for relation in GroupUserRelation.objects.filter(
                user_id=user.id).all(
                )]

        if time_type == 'before':
            secrets = Secret.objects.filter(create_time__lt=timestamp_to_datetime(
                timestamp), group_id__in=group_ids).order_by('-id').all()[:size]
        else:
            secrets = Secret.objects.filter(create_time__gte=timestamp_to_datetime(
                timestamp), group_id__in=group_ids).order_by('-id').all()[:size]
    except Exception, e:
        return json_response_error(DATA_ERROR, e)

    result = {'secrets': []}
    for secret in secrets:
        hot = Comment.objects.filter(secret_id=secret.id).count()
        result['secrets'].append({
            'id': secret.id,
            'content': secret.content,
            'group_id': secret.group_id,
            'hot': hot,
            'time': datetime_to_timestamp(secret.create_time),
        })

    return json_response_ok(result)


@user_auth
def add_secrets(request, group_id):
    data = request.POST
    content = data.get('content')
    if not content:
        return json_response_error(PARAM_REQUIRED, 'content')

    user = request.META['user']

    try:
        secret = Secret._add_secret(user, group_id, content)
    except Exception as e:
        return json_response_error(DATA_ERROR, e)

    result = {
        'id': secret.id,
        'time': datetime_to_timestamp(secret.create_time),
    }

    return json_response_ok(result)


@user_auth
def secrets(request, group_id):
    data = request.POST
    size = int(data.get('size', 50))
    timestamp = int(data.get('time'))
    if not timestamp:
        return json_response_error(PARAM_REQUIRED, 'time')
    time_type = data.get('type')
    if time_type not in ['before', 'after']:
        return json_response_error(PARAM_REQUIRED, 'type')

    size = min(size, 100)

    if time_type == 'before':
        secrets = Secret.objects.filter(create_time__lt=timestamp_to_datetime(
            timestamp), group_id=group_id).order_by('-id').all()[:size]
    else:
        secrets = Secret.objects.filter(create_time__gte=timestamp_to_datetime(
            timestamp), group_id=group_id).order_by('-id').all()[:size]

    result = {'secrets': []}
    for secret in secrets:
        hot = Comment.objects.filter(secret_id=secret.id).count()
        result['secrets'].append({
            'id': secret.id,
            'content': secret.content,
            'hot': hot,
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

    new_comment = Comment.objects.filter(
        secret_id=secret_id).order_by(
            '-floor').all(
            )
    if new_comment:
        floor = new_comment[0].floor + 1
    else:
        floor = 1

    try:
        if reply_to:
            reply_to = int(reply_to)
            replied_comment = Comment.objects.get(id=reply_to)
            receive_user_id = replied_comment.author_id
            comment = Comment._add_comment(
                content,
                user.id,
                secret_id,
                reply_to,
                floor)
        else:
            replied_secret = Secret.objects.get(id=secret_id)
            receive_user_id = replied_secret.author_id
            comment = Comment._add_comment(
                content,
                user.id,
                secret_id,
                reply_to,
                floor)
        Notice._add_notice(receive_user_id, comment)
    except Exception as e:
        return json_response_error(DATA_ERROR, e)

    result = {
        'id': comment.id,
        'time': datetime_to_timestamp(comment.create_time),
        'floor': floor,
    }

    return json_response_ok(result)


@user_auth
def comments(request, secret_id):
    data = request.REQUEST
    size = int(data.get('size', 50))
    timestamp = int(data.get('time'))
    if not timestamp:
        return json_response_error(PARAM_REQUIRED, 'time')
    time_type = data.get('type', 'after')
    if time_type not in ['before', 'after']:
        return json_response_error(PARAM_REQUIRED, 'type')

    size = min(size, 100)

    if time_type == 'before':
        comments = Comment.objects.filter(secret_id=secret_id).filter(
            create_time__lt=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]
    else:
        comments = Comment.objects.filter(secret_id=secret_id).filter(
            create_time__gte=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]

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
    data = request.REQUEST
    size = int(data.get('size', 50))
    timestamp = int(data.get('time'))
    if not timestamp:
        return json_response_error(PARAM_REQUIRED, 'time')
    time_type = data.get('type', 'after')
    if time_type not in ['before', 'after']:
        return json_response_error(PARAM_REQUIRED, 'type')

    size = min(size, 100)

    user = request.META['user']

    if time_type == 'before':
        secrets = Secret.objects.filter(author_id=user.id).filter(
            create_time__lt=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]
    else:
        secrets = Secret.objects.filter(author_id=user.id).filter(
            create_time__gte=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]

    result = {'secrets': []}

    for secret in secrets:
        result['secrets'].append({
            'id': secret.id,
            'time': datetime_to_timestamp(secret.create_time),
            'content': secret.content,
            'group_id': secret.group_id,
        })

    return json_response_ok(result)


@user_auth
def notice(request):
    data = request.REQUEST
    size = int(data.get('size', 50))
    timestamp = int(data.get('time'))
    if not timestamp:
        return json_response_error(PARAM_REQUIRED, 'time')
    time_type = data.get('type', 'after')
    if time_type not in ['before', 'after']:
        return json_response_error(PARAM_REQUIRED, 'type')

    size = min(size, 100)

    user = request.META['user']

    if time_type == 'before':
        notices = Notice.objects.filter(receive_user_id=user.id).filter(status=0).filter(
            create_time__lt=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]
    else:
        notices = Notice.objects.filter(receive_user_id=user.id).filter(status=0).filter(
            create_time__gte=timestamp_to_datetime(timestamp)).order_by('-id').all()[:size]

    result = {'notices': []}

    for notice in notices:
        try:
            reply_id = notice.comment_id
            comment = Comment.objects.get(id=reply_id)
            secret = Secret.objects.get(id=comment.secret_id)
            r = {
                'id': notice.id,
                'reply_id': reply_id,
                'secret': {
                'id': secret.id,
                'group_id': secret.group_id,
                'content': secret.content,
                'time': datetime_to_timestamp(secret.create_time),
                },
                'reply_time': datetime_to_timestamp(comment.create_time),
                'reply_content': comment.content,
            }
            if comment.reply_to_id:
                replied_content = Comment.objects.get(
                    id=comment.reply_to_id).content
                r['replied_content'] = replied_content
            result['notices'].append(r)
        except Exception as e:
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
    except Exception as e:
        return json_response_error(DATA_ERROR, e)

    return json_response_ok()


@user_auth
def relation(request):
    data = request.POST
    group_id = data.get('group_id')
    if not group_id:
        return json_response_error(PARAM_REQUIRED, 'group_id')
    action_type = data.get('type')
    if action_type not in ['follow', 'unfollow']:
        return json_response_error(PARAM_REQUIRED, 'type')

    user = request.META['user']
    try:
        group_id = int(group_id)
        if action_type == 'follow':
            relation = GroupUserRelation._update_relation(user.id, group_id, GROUP_USER_STATUS_FOLLOW)
            result = {'relation_id': relation.id}
        else:
            relation = GroupUserRelation._update_relation(user.id, group_id, GROUP_USER_STATUS_UNFOLLOW)
            result = {}
    except Exception as e:
        return json_response_error(DATA_ERROR, e)

    return json_response_ok(result)


@user_auth
def group_list(request):

    user = request.META['user']

    user_group_list = GroupUserRelation.objects.filter(user_id=user.id, status=0).all()

    group_id_list = [relation.group_id for relation in user_group_list]
    relation_time_dict = dict([(relation.group_id, relation.update_time) for relation in user_group_list])

    group_list = Group.objects.filter(id__in=group_id_list).all()

    result = []
    for group in group_list:
        result.append({
            'id': group.id,
            'name': group.name,
            'pinyin': group.pinyin,
            'py_first': group.py_first,
            'time': datetime_to_timestamp(relation_time_dict[group.id]),
        })

    return json_response_ok(result)
