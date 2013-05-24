# -*- coding: utf-8 -*-

from django.contrib import admin

from lisa.api.models import User, ThirdPartySource, School, Secret


class ThirdPartySourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'api', 'app_key', 'app_secret', 'update_time')
    list_editable = ('api', 'app_key', 'app_secret')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pinyin', 'py_first', 'update_time')
    list_editable = ('pinyin',)
    search_fields = ('name', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'source', 'school', 'uid', 'status', 'create_time')
    list_editable = ('status',)
    list_filter = ('source', 'school')
    search_fields = ('name', )


class SecretAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'school', 'status', 'create_time')
    list_editable = ('status', )
    list_filter = ('school',)
    search_fields = ('school', 'content', 'author')


admin.site.register(ThirdPartySource, ThirdPartySourceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Secret, SecretAdmin)
