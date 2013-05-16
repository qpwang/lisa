# -*- coding: utf-8 -*-
from lisa.api.models import User
from lisa.util.json import json_response_error


def user_auth(func):
    def _(request, *args, **kwargs):
        token = request.POST.get('token')
        try:
            user = User.objects.get(token=token)
            request.META['user'] = user
        except:
            return json_response_error(1, 'user auth failed')
        return func(request, *args, **kwargs)
    return _

