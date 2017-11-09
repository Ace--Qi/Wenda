# encoding: utf-8
"""wenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import  students.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
   #数据库
   url(r'^admin/', admin.site.urls),
   #问答主页
   url(r'^showQuestion/', students.views.showQuestion,name='showQuestion'),
   #请求问题
   url(r'send$', students.views.send, name='send'),
   #是否对图灵的答案满意
   #url(r'evaluation$', students.views.evaluation, name='evaluation'),
   #是否对百度的答案满意
   url(r'csanswer$', students.views.csanswer, name='csanswer'),
   #对此次会话的评价
   url(r'star$',students.views.star,name='star'),
   url(r'defineanswer$',students.views.defineanswer,name='defineanswer')
]
urlpatterns += staticfiles_urlpatterns()
