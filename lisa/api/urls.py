from django.conf.urls import patterns, include, url
from lisa.api.views import all_secrets, send_secrets, get_secrets, profiles

urlpatterns = patterns('',
        url(r'^profiles$', profiles, name='profiles'),
        url(r'^all$', all_secrets, name='get_secrets'),
        url(r'^secrets/send$', send_secrets, name='send_secrets'),
        url(r'^secrets/get$', get_secrets, name='get_secrets'),
)
