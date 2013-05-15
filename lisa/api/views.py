# -*- coding: utf-8 -*-
from lisa.util.json import json_response_ok, json_response_error
from lisa.util.respcode import PARAM_REQUIRED, ERROR_MESSAGE, DATA_ERROR
from lisa.decorator import user_auth
from lisa.api.models import User, Secret


def profiles(request):
    data = request.GET

    token = data.get('token')
    if not token:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'token'))

    user_name = data.get('user_name')
    if not user_name:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'user_name'))

    email = data.get('email')
    if not email:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'email'))

    source = data.get('source')
    if not source:
        return json_response_error(PARAM_REQUIRED,
                '%s: %s' % (ERROR_MESSAGE[PARAM_REQUIRED], 'source'))

    try:
        user = User()
        user.user_name = user_name
        user.source_id = source
        user.token = token
        user.email = email
        user.school_id = 1
        user.status = 0
        user.save()
    except Exception, e:
        return json_response_error(DATA_ERROR,
                '%s: %s' % (ERROR_MESSAGE[DATA_ERROR], e))

    result = {'id': user.id}

    return json_response_ok(result)


@user_auth
def all_secrets(request):
    data = request.REQUEST
    page = int(data.get('page', 1))

    start = 20 * (page - 1)

    secrets = Secret.objects.all()[start:start+20]

    return json_response_ok(secrets)


@user_auth
def send_secrets(request):
    user = request.META['user']
    data = request.POST
    content = data.get('content')
    return json_response_ok(content)


def get_secrets(request):
    #TODO
    pass
