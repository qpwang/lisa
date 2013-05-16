# -*- coding: utf-8 -*-
from django.db import models


class ThirdPartySource(models.Model):
    '''第三方平台'''
    class Meta:
        db_table = 'third_party_source'
        verbose_name = verbose_name_plural = '第三方管理'

    name = models.CharField(max_length=64, verbose_name='名称')
    api = models.CharField(max_length=200, verbose_name='API地址')
    app_key = models.CharField(max_length=200, verbose_name='appkey')
    app_secret = models.CharField(blank=True, null=True, max_length=200, verbose_name='appsecret')
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class School(models.Model):
    '''学校'''
    class Meta:
        db_table = 'school'
        verbose_name = verbose_name_plural = '学校管理'

    name = models.CharField(max_length=128, verbose_name='名称')
    pinyin = models.CharField(max_length=200, verbose_name='拼音')
    city = models.CharField(max_length=64, null=True)
    update_time = models.DateTimeField(auto_now=True)


class User(models.Model):
    '''用户表'''
    class Meta:
        db_table = 'user'
        verbose_name = verbose_name_plural = '用户管理'
        unique_together = ('email', 'source')

    user_name = models.CharField(max_length=128, verbose_name='用户名')
    source = models.ForeignKey(ThirdPartySource, verbose_name='用户来源')
    token = models.CharField(max_length=200, verbose_name='token')
    email = models.CharField(max_length=200, verbose_name='email')
    status = models.IntegerField(default=0, verbose_name='用户状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user_name


class Secret(models.Model):
    '''秘密'''
    class Meta:
        db_table = 'secret'
        verbose_name = verbose_name_plural = '秘密管理'

    content = models.CharField(max_length=200, verbose_name='秘密内容')
    author = models.ForeignKey(User, verbose_name='发送人')
    school = models.ForeignKey(School, verbose_name='学校')
    status = models.IntegerField(default=0, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


class Comment(models.Model):
    '''评论'''
    class Meta:
        db_table = 'comment'
        verbose_name = verbose_name_plural = '评论管理'

    content = models.CharField(max_length=200, verbose_name='评论')
    author = models.ForeignKey(User)
    secret = models.ForeignKey(Secret, verbose_name='秘密')
    reply_to = models.ForeignKey('self', null=True)
    floor = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


class Notice(models.Model):
    '''通知'''
    class Meta:
        db_table = 'notice'
        verbose_name = verbose_name_plural = '通知管理'

    receive_user = models.ForeignKey(User, verbose_name='接收人')
    secret = models.ForeignKey(Comment, verbose_name='秘密')
    status = models.IntegerField(default=0, verbose_name='通知状态')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

