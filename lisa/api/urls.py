from django.conf.urls import patterns, url
from lisa.api.views import all_secrets, add_secrets, secrets, add_comments, comments, profiles, mine, notice_delete, notice, sample, group, relation, group_list, my_secrets

urlpatterns = patterns('',
                       url(r'^profiles$', profiles, name='profiles'),
                       url(r'^all$', all_secrets, name='all_secrets'),
                       url(r'^follow/secrets$', my_secrets, name='my_secrets'),
                       url(r'^(?P<group_id>\d+)/secrets/add$',
                           add_secrets, name='add_secrets'),
                       url(r'^(?P<group_id>\d+)/secrets$',
                           secrets, name='secrets'),
                       url(r'^(?P<secret_id>\d+)/comments/add$',
                           add_comments, name='add_comments'),
                       url(r'^(?P<secret_id>\d+)/comments$',
                           comments, name='commentts'),
                       url(r'^mine$', mine, name='mine'),
                       url(r'^notice$', notice, name='notice'),
                       url(r'^notice/delete$',
                           notice_delete, name='notice_delete'),
                       url(r'^sample$', sample, name='sample'),
                       url(r'^group$', group, name='group'),
                       url(r'^follow$', group_list, name='group_list'),
                       url(r'^relation$', relation, name='relation'),
                       )
