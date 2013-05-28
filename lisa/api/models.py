# -*- coding: utf-8 -*-
import requests
from uuid import uuid4
from django.db import models
from django.utils import simplejson as json


class ThirdPartySource(models.Model):
    '''第三方平台'''
    class Meta:
        db_table = 'lisa_third_party_source'
        verbose_name = verbose_name_plural = '第三方管理'

    name = models.CharField(max_length=64, verbose_name='名称')
    api = models.CharField(max_length=200, verbose_name='API地址')
    app_key = models.CharField(max_length=200, verbose_name='appkey')
    app_secret = models.CharField(blank=True, null=True, max_length=200, verbose_name='appsecret')
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def _access_token(cls,access_token, uid, source):
        third_party_source = cls.objects.get(name=source)
        if source == 'sina':
            post_dict = {
                    'access_token': access_token,
                }
            api = '%s?access_token%s' % (third_party_source.api, access_token)
            response = requests.post(api, post_dict)
            result = json.loads(response.content)
            if str(result.get('uid')) == uid:
                return third_party_source.id
        elif source == 'renren':
            post_dict = {
                    'access_token': access_token,
                    'v': '1.0',
                    'format': 'json',
                    'method': 'users.getInfo',
                    'fields': 'uid',
                }
            api = third_party_source.api
            response = requests.post(api, post_dict)
            result = json.loads(response.content)
            if str(result[0].get('uid')) == uid:
                return third_party_source.id


class School(models.Model):
    '''学校'''
    class Meta:
        db_table = 'lisa_school'
        verbose_name = verbose_name_plural = '学校管理'
        ordering = ('id',)

    name = models.CharField(max_length=128, verbose_name='名称')
    pinyin = models.CharField(max_length=200, verbose_name='拼音')
    py_first = models.CharField(max_length=200, verbose_name='拼音')
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class User(models.Model):
    '''用户表'''
    class Meta:
        db_table = 'lisa_user'
        verbose_name = verbose_name_plural = '用户管理'
        unique_together = ('uid', 'source')

    user_name = models.CharField(max_length=128, verbose_name='用户名')
    uid = models.CharField(max_length=128, verbose_name='uid')
    source = models.ForeignKey(ThirdPartySource, verbose_name='用户来源')
    token = models.CharField(max_length=200, verbose_name='token')
    school = models.ForeignKey(School, verbose_name='学校', blank=True, null=True)
    status = models.IntegerField(default=0, verbose_name='用户状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user_name

    @classmethod
    def _get_user(cls, user_name, uid, source_id):
        user = cls.objects.filter(source_id=source_id).filter(uid=uid).all()
        if not user:
            user = User()
            user.user_name = user_name
            user.uid = uid
            user.source_id = source_id
            user.token = uuid4()
            user.status = 0
            user.save()
        else:
            user = user[0]
        return user


class Secret(models.Model):
    '''秘密'''
    class Meta:
        db_table = 'lisa_secret'
        verbose_name = verbose_name_plural = '秘密管理'

    content = models.CharField(max_length=200, verbose_name='秘密内容')
    author = models.ForeignKey(User, verbose_name='发送人')
    school = models.ForeignKey(School, verbose_name='学校')
    status = models.IntegerField(default=0, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

    @classmethod
    def _add_secret(cls, user, school_id, content):
        secret = cls()
        secret.content = content
        secret.author_id = user.id
        secret.school_id = school_id
        secret.status = 0
        secret.save()
        return secret



class Comment(models.Model):
    '''评论'''
    class Meta:
        db_table = 'lisa_comment'
        verbose_name = verbose_name_plural = '评论管理'

    content = models.CharField(max_length=200, verbose_name='评论')
    author = models.ForeignKey(User)
    secret = models.ForeignKey(Secret, verbose_name='秘密')
    reply_to = models.ForeignKey('self', null=True)
    floor = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

    @classmethod
    def _add_comment(cls, content, user_id, secret_id, reply_to, floor):
        comment = cls()
        comment.content = content
        comment.author_id = user_id
        comment.secret_id = secret_id
        comment.reply_to_id = reply_to
        comment.floor = floor
        comment.save()
        return comment


class Notice(models.Model):
    '''通知'''
    class Meta:
        db_table = 'lisa_notice'
        verbose_name = verbose_name_plural = '通知管理'

    receive_user = models.ForeignKey(User, verbose_name='接收人')
    comment = models.ForeignKey(Comment, verbose_name='秘密')
    status = models.IntegerField(default=0, verbose_name='通知状态')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    @classmethod
    def _add_notice(cls, receive_user_id, comment):
        notice = cls()
        notice.receive_user_id = receive_user_id
        notice.comment_id = comment.id
        notice.status = 0
        notice.save()


class SchoolUserRelation(models.Model):
    '''学校关注列表'''
    class Meta:
        db_table = 'lisa_school_user_relation'
        verbose_name = verbose_name_plural = '关注列表'
        unique_together = ('user', 'school')


    school = models.ForeignKey(School)
    user = models.ForeignKey(User)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    @classmethod
    def _add_relation(cls, user_id, school_id):
        relation = SchoolUserRelation.objects.filter(user_id=user_id).filter(school_id=school_id).all()
        if relation:
            relation = relation[0]
            relation.status = 0
            relation.save()
        else:
            relation = SchoolUserRelation()
            relation.user_id = user_id
            relation.school_id = school_id
            relation.status = 0
            relation.save()
        return relation

    @classmethod
    def _update_relation(cls, user_id, school_id, status):
        relation = SchoolUserRelation.objects.filter(user_id=user_id).filter(school_id=school_id).all()[0]
        relation.status = status
        relation.save()
        return relation

