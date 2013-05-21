# -*- coding: utf-8 -*-

from django.contrib import admin

from lisa.api.models import User, ThirdPartySource, School, Secret, UpdateInfo


class ThirdPartySourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'api', 'app_key', 'app_secret', 'update_time')
    list_editable = ('api', 'app_key', 'app_secret')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'pinyin', 'city', 'update_time')
    list_editable = ('pinyin',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'source', 'school', 'uid', 'status', 'create_time')
    list_editable = ('status',)
    list_filter = ('source', 'school')


class SecretAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'school', 'status', 'create_time')
    list_editable = ('status', )
    list_filert = ('school',)


class UpdateInfoAdmin(admin.ModelAdmin):
    list_display = ('version', 'content', 'url', 'flag', 'update_time')

admin.site.register(ThirdPartySource, ThirdPartySourceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Secret, SecretAdmin)
admin.site.register(UpdateInfo, UpdateInfoAdmin)
