#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import django.utils.timezone as timezone
from django.db import models
# Create your models here.
#问题答案数据表（ID主键，问题内容，关键词5个按权重由高到低，问题答案，教师权重）
class Faq(models.Model):
    id = models.AutoField(primary_key=True)
    question_content = models.TextField()
    answer_content = models.TextField()
    question_keyword = models.CharField(max_length=50)
    visit_wegiht=models.BigIntegerField(default=1)
    baidu_answer= models.TextField(default="")
    def __str__(self):
        return str(self.id)
class Meta:
    verbose_name_plural = '答疑表数据库'
    # 这是表的网页显示名称 
    verbose_name='faq'



#用户会话数据表（ID主键，userid，对话的完整内容，用户对这段对话的评价）
class UserSession(models.Model):
    id = models.AutoField(primary_key=True)
    userid=models.BigIntegerField(default=1)
    content = models.TextField()
    time= models.CharField(max_length=50)
    user_evalution=models.FloatField()
    def __str__(self):
        return str(self.id)
class Meta:
    verbose_name_plural = '用户session'
    # 这是表的网页显示名称 
    verbose_name='UserSession'

# 本地常用问答知识库

class Knowledge(models.Model):
    id = models.AutoField(primary_key=True)
    question_content = models.TextField()
    answer_content = models.TextField()
    def __str__(self):
        return str(self.id)
class Meta:
    verbose_name_plural = '知识库'
    # 这是表的网页显示名称 
    verbose_name='Knowledge'
