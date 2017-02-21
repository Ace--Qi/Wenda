#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.
class Faq(models.Model):
    id = models.AutoField(primary_key=True)
    question_content = models.TextField()
    answer_content = models.TextField()
    question_keyword = models.CharField(max_length=50)
    teacher_wegiht=models.BigIntegerField(default=1)
    student_evaluation=models.FloatField(max_length=10,default=50.0)
    def __str__(self):
        return str(self.id)
class Meta:
    verbose_name_plural = '答疑表数据库'
    # 这是表的网页显示名称 
    verbose_name='faq'

