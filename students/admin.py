#-*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from students.models import Faq,UserSession,Knowledge
#from ipApp.models import Publisher, Author, Book

class FaqAdmin(admin.ModelAdmin):
    search_fields = ('id','question_content','answer_content','question_keyword','visit_wegiht','baidu_answer') #根据属性搜索
    list_display=('id','question_content','answer_content','question_keyword','visit_wegiht','baidu_answer')  #列表显示的属性
    list_filter = ('id',)   #筛选
    pass
admin.site.register(Faq,FaqAdmin)


class UserSessionAdmin(admin.ModelAdmin):
    search_fields = ('id','content','time','userid') #根据属性搜索
    list_display=('id','content','time','userid')  #列表显示的属性
    list_filter = ('id','userid')   #筛选
    pass
admin.site.register(UserSession,UserSessionAdmin)



class KnowledgeAdmin(admin.ModelAdmin):
    search_fields = ('id','question_content','answer_content') #根据属性搜索
    list_display=('id','question_content','answer_content')  #列表显示的属性
    list_filter = ('id',)   #筛选
    pass
admin.site.register(Knowledge, KnowledgeAdmin)
