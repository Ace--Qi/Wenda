#-*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from students.models import Faq
#from ipApp.models import Publisher, Author, Book

class FaqAdmin(admin.ModelAdmin):
    search_fields = ('id','question_content','answer_content','question_keyword','teacher_wegiht','student_evaluation') #根据属性搜索
    list_display=('id','question_content','answer_content','question_keyword','teacher_wegiht','student_evaluation')  #列表显示的属性
    list_filter = ('id',)   #筛选
    pass
admin.site.register(Faq,FaqAdmin)
