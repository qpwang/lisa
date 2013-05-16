from django.conf.urls import patterns, include, url
from lisa.api.views import all_secrets, add_secrets, get_secrets, profiles

urlpatterns = patterns('',
        url(r'^profiles$', profiles, name='profiles'),
        url(r'^all$', all_secrets, name='get_secrets'),
        url(r'^(?P<school_id>\d+)/secrets/all$', add_secrets, name='add_secrets'),
        url(r'^secrets/get$', get_secrets, name='get_secrets'),
)
