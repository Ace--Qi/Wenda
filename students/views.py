# encoding: utf-8
from django.shortcuts import render
import  datetime
import MySQLdb
import string
import sys
sys.path.append("../")
import jieba
jieba.load_userdict("./extra_dict/userdict.txt")
import jieba.posseg as pseg
import jieba.analyse
import MeCab
import requests
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Faq
from jpype import  *
import json
#from django.views.decorators.csrf import csrf_protect
# Create your views here.
def sayHello(request):
    s="dad"
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1> %s </h1><p> %s </p></body></html>' % (s, current_time)
    return HttpResponse(html)
def showStudents(request):
     list = [{id: 1, 'name': 'Jack'}, {id: 2, 'name': 'Rose'}]
     return render_to_response('student.html',{'students': list})

#@csrf_protect
def showQuestion(request):
    return render(request, 'QuestionAnswerView.html')

def send(request):
    if request.method == 'POST':
        receive = request.POST['question']
        sentence = receive.encode("utf-8")
       # seg_list = jieba.cut(sentence, cut_all=False)
       #print("Default Mode: " + "/ ".join(seg_list))  # 默认模式

        tags = jieba.analyse.extract_tags(sentence, topK=20)
        keyword=",".join(tags)
        print(keyword)
        keyword_num=0
        last_match_keynum = 1
        num=len(tags)
        if num<5 and num>0:
            keyword_num=num
            keyword=tags[0]
            for i in range(1,keyword_num):
                keyword=keyword+","+tags[i]
        elif num >5:
            keyword_num=5
            keyword=tags[0]+","+tags[1]+","+tags[2]+","+tags[3]+","+tags[4]
        else:
            keyword=sentence
        print(keyword)
        json_data = {}
        try:
            message = Faq.objects.get(question_content=receive)
        except ObjectDoesNotExist:
            if keyword_num!=0 :
               data = Faq.objects.filter(question_keyword__contains=tags[0])
               for i in range(1,keyword_num-1):
                   if len(data):
                       if i == 1:
                        data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(question_keyword__contains=tags[1])
                        last_match_keynum=2
                       if i == 2:
                        data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(question_keyword__contains=tags[1]) .filter(question_keyword__contains=tags[2])
                        last_match_keynum=3
                       if i == 3:
                            data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                                question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(question_keyword__contains=tags[3])
                            last_match_keynum = 4
                       if i == 4:
                            data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                                question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(question_keyword__contains=tags[3]).filter(question_keyword__contains=tags[4])
                            last_match_keynum = 5
                   else:
                        break
               print data,last_match_keynum
               print ("模糊匹配数据库")
               if len(data)==0:
                   print ("模糊匹配数据库失败调用图灵")
                   url = 'http://www.tuling123.com/openapi/api'
                   key = '37c58bfcfd4c403c9c4baaa3644822ef'
                   query = {'key': key, 'info': sentence, 'userid': '1'}
                   headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
                   r = requests.get(url, params=query, headers=headers)
                   json_data = r.json()
                   count = Faq.objects.count()
                   print count
                   Faq.objects.create(id=count+1,question_content=sentence,answer_content=json_data["text"], question_keyword=keyword, teacher_wegiht=1,
                                      student_evaluation=50.00)
               else:
                   if last_match_keynum == 1:
                       answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).order_by('-teacher_wegiht').order_by('-student_evaluation')
                       print ("按teacher倒排序")
                       print answerdata[0].answer_content
                   if last_match_keynum == 2:
                       answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                           question_keyword__contains=tags[1]).order_by('-teacher_wegiht').order_by('-student_evaluation')
                       print ("按teacher倒排序")
                       print answerdata[0].answer_content
                   if last_match_keynum == 3:
                       answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                           question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).order_by('-teacher_wegiht').order_by('-student_evaluation')
                       print ("按teacher倒排序")
                       print answerdata[0].answer_content

                   if last_match_keynum == 4:
                       answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                           question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(
                           question_keyword__contains=tags[3]).order_by('-teacher_wegiht').order_by('-student_evaluation')
                       print ("按teacher倒排序")
                       print answerdata[0].answer_content

                   if last_match_keynum == 5:
                       answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                           question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(
                           question_keyword__contains=tags[3]).filter(question_keyword__contains=tags[4]).order_by('-teacher_wegiht').order_by('-student_evaluation')
                       print ("按teacher倒排序")
                       print answerdata[0].answer_content
                   json_data['text'] = answerdata[0].answer_content
                   json_data['answerid']=answerdata[0].id
            else:
                print ("分词后没有关键词调用图灵")
                url = 'http://www.tuling123.com/openapi/api'
                key = '37c58bfcfd4c403c9c4baaa3644822ef'
                query = {'key': key, 'info': sentence, 'userid': '1'}
                headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
                r = requests.get(url, params=query, headers=headers)
                json_data = r.json()
                count=Faq.objects.count()
                json_data['answerid'] =count+1
                print count
                Faq.objects.create(id=count+1,question_content=sentence,answer_content=json_data["text"], question_keyword=keyword,teacher_wegiht=1,student_evaluation=50.00)
        else:
            print ("问题完全匹配本地数据库回答")
            json_data['text'] = message.answer_content
            json_data['answerid'] = message.id
        '''
        KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'
        params = {'top_k': 2}
        data = json.dumps(sentence)
        headers = {'X-Token': '6rALcgNl.13077.nd_Ez638TQ-L'}
        resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data)
        dict=resp.json()
        s = str(dict).replace('u\'', '\'')
        print s.decode("unicode-escape")
        keyword_data={}
        for weight, word in resp.json():
              keyword_data[temptime]=word
              print(weight, word)
              temptime=temptime+1
        json_data={}
        print  keyword_data

        json_data = {}
        try:
            message = Faq.objects.get(question_content=receive)
        except ObjectDoesNotExist:
            print temptime
            if temptime >=3:
              data = Faq.objects.filter(question_keyword__contains=keyword_data[0]).filter(question_keyword__contains=keyword_data[1]).filter(question_keyword__contains=keyword_data[2])
            else:
              data = Faq.objects.filter(question_keyword__contains=keyword_data[0])
            print (data)
            json_data['data'] = "对不起，我听不懂你在说什么，我会把你的问题转交给管理员。"
        else:
            json_data['data'] = message.answer_content
        '''
    '''
    if request.method == 'POST':
        receive = request.POST['question']
        sentence=receive.encode("utf-8")
        url = 'http://www.tuling123.com/openapi/api'
        key='37c58bfcfd4c403c9c4baaa3644822ef'
        query = {'key': key, 'info': sentence,'userid':'1'}
        headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
        r = requests.get(url, params=query, headers=headers)
        json_data = r.json()

        #print("测试"+MeCab.VERSION)
        try:
            m = MeCab.Tagger("-d ./mecab_chinese_data_binary_v0.3/ -O pos")
            temp=m.parse(sentence)
            print m.parse(sentence)
            print (type(temp))
            t = m.parseToNode(sentence)
            while t:
                print t.surface.decode('string-escape')
                t = t.next
        except RuntimeError as e:
            print("RuntimeError:", e);

        if not isJVMStarted():
           startJVM(getDefaultJVMPath(),"-Djava.class.path=./hanlp-1.3.2-release/hanlp-1.3.2.jar:./hanlp-1.3.2-release")
           Hanlp = JClass('com.hankcs.hanlp.HanLP')
        # 中文分词
           temp = Hanlp.segment(sentence.decode("utf-8"));
           print temp.toString()
          # p=java.lang.Runtime.getRuntime()
          # p.destory()
           shutdownJVM()
        json_data = {}
        try:
            message= Faq.objects.get(question_content=receive)
        except ObjectDoesNotExist:
            data = Faq.objects.filter(question_keyword__regex=sentence)
            print (data)
            json_data['data'] = "对不起，我听不懂你在说什么，我会把你的问题转交给管理员。"
        else:
            json_data['data'] = message.answer_content
'''
    return JsonResponse(json_data)


def evaluation(request):
    if request.method == 'POST':
        receiveid = request.POST['i']
        receiveevaluation=request.POST['evaluation']
        print ("answer id ")
        print receiveid
        modifiers = Faq.objects.get(id=receiveid)
        print  type(modifiers)

        modifiers=Faq.objects.get(id=receiveid)
        if receiveevaluation==1:
            modifiers.teacher_wegiht=modifiers.teacher_wegiht+1
            modifiers.student_evaluation = modifiers.student_evaluation*0.02+modifiers.student_evaluation
            modifiers.save()
        else:
            modifiers.teacher_wegiht = modifiers.teacher_wegiht - 1
            modifiers.student_evaluation = modifiers.student_evaluation-modifiers.student_evaluation * 0.02
            modifiers.save()
        json_data={}
        return  JsonResponse(json_data)
