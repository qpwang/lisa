# -*- coding: utf-8 -*-

from django.contrib import admin

from lisa.api.models import User, ThirdPartySource, Group, Secret


class ThirdPartySourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'api', 'app_key', 'app_secret', 'update_time')
    list_editable = ('api', 'app_key', 'app_secret')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'pinyin', 'py_first', 'update_time')
    list_editable = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'source', 'uid', 'status', 'create_time')
    list_editable = ('status',)
    list_filter = ('source', 'status')
    search_fields = ('name',)


class SecretAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'group', 'status', 'create_time')
    list_editable = ('status',)
    list_filter = ('status', 'group')
    search_fields = ('group', 'content', 'author')


admin.site.register(ThirdPartySource, ThirdPartySourceAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Secret, SecretAdmin)
