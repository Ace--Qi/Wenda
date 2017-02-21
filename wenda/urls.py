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
   url(r'^admin/', admin.site.urls),
   url(r'^student/',students.views.sayHello,name='sayHello'),
   url(r'^showStudents/', students.views.showStudents,name='showStudents'),
   url(r'^showQuestion/', students.views.showQuestion,name='showQuestion'),
   url(r'send$', students.views.send, name='send'),
   url(r'evaluation$', students.views.evaluation, name='evaluation'),
]
urlpatterns += staticfiles_urlpatterns()
