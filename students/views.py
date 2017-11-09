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
import zlib
import  difflib
import requests
import  tutorial
import os
import  scrapy
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import JsonResponse
from tutorial.spiders.dmoz_spider import DmozSpider
from django.core.exceptions import ObjectDoesNotExist
from .models import Faq
from .models import UserSession
from jpype import  *
import json
#from django.views.decorators.csrf import csrf_protect
# Create your views here.
#@csrf_protect
from scrapy.crawler import CrawlerProcess
from scrapy import signals,log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
global questionurl,questionsen
questionurl=""
questionsen=""
def showQuestion(request):
    return render(request, 'QuestionAnswerView.html')

def send(request):
    json_data = {}
    if request.method == 'POST':
        receive = request.POST['question']
        sentence = receive.encode("utf-8")

        # 爬虫百度答案
        global questionurl, questionsen
        questionurl = "https://zhidao.baidu.com/search?ct =17&pn=0&tn=ikaslist&rn=10&word=" + sentence
        questionsen = sentence
        runner = CrawlerRunner()
        d = runner.crawl(DmozSpider, start_urls=[questionurl])
        d.addBoth(lambda _: reactor.crash())
        reactor.run()
        with open("/Users/wangqi/PycharmProjects/wenda/tutorial/items.json", "r") as f:
            message = json.load(f)
        s = message["desc"].encode("utf-8")
        a = message["title"].encode("utf-8")
        # json_data['baidu'] = 1
        json_data['baidutext'] = s
        if json_data['baidutext'] == "":
            json_data['baidutext'] = message["answer"].encode("utf-8")
        if json_data['baidutext'] == "":
            json_data['baidutext'] = "百度也不知道呢"
        # global question
        json_data['baiduquestion'] = questionsen
        f.close()
        # seg_list = jieba.cut(sentence, cut_all=False)
       #print("Default Mode: " + "/ ".join(seg_list))  # 默认模式

        tags = jieba.analyse.extract_tags(sentence, topK=20)
        keyword=",".join(tags)
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
        print "Participles keywords (no more than 5) "+keyword

        try:
            message = Faq.objects.get(question_content=receive)
        except ObjectDoesNotExist:
            if keyword_num!=0 :
               data = Faq.objects.filter(question_keyword__contains=tags[0])
               print tags[0],data
               if len(data) ==0:
                   last_match_keynum=0
               for i in range(1,keyword_num):
                   if len(data):
                       if i == 1:
                        data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(question_keyword__contains=tags[1])
                        last_match_keynum=1
                       if i == 2:
                        data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(question_keyword__contains=tags[1]) .filter(question_keyword__contains=tags[2])
                        last_match_keynum=2
                       if i == 3:
                            data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                                question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(question_keyword__contains=tags[3])
                            last_match_keynum = 3
                       if i == 4:
                            data = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                                question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(question_keyword__contains=tags[3]).filter(question_keyword__contains=tags[4])
                            last_match_keynum = 4
                   else:
                        print ("数据库中关键词没有完全匹配")
                        break

               print data,last_match_keynum
               if len(data)==0:
                   temp_match_num = [0 for x in range(1000)]
                   k = 0
                   print ("数据库中关键词没有完全匹配，进行语句相似度匹配")
                   question = Faq.objects.all()
                   temp_match =float(difflib.SequenceMatcher(None, sentence, question[0].question_content.encode("utf-8")).ratio())
                   for i in range(0, len(question)):
                       print difflib.SequenceMatcher(None, sentence,
                                                     question[i].question_content.encode("utf-8")).ratio()
                       if difflib.SequenceMatcher(None, sentence, question[i].question_content.encode("utf-8")).ratio() > temp_match or difflib.SequenceMatcher(None, sentence,
                                                                                                question[i].question_content.encode("utf-8")).ratio() == temp_match:
                           if difflib.SequenceMatcher(None, sentence, question[
                               i].question_content.encode("utf-8")).ratio() > 0.8 or difflib.SequenceMatcher(None, sentence, question[
                               i].question_content.encode("utf-8")).ratio() == 0.8:
                               temp_match = difflib.SequenceMatcher(None, sentence,
                                                                    question[i].question_content.encode("utf-8")).ratio()
                               temp_match_num[i] = question[i].id
                               k=k+1
                   maxmatch = 0.8
                   answerid = 0
                   print  "匹配语句条数："
                   print k
                   if k == 0:
                       json_data["answerid"]=0
                       json_data["text"]="知识库没有答案"
                       print ("数据库语句匹配失败，进行部分关键词匹配")
                       if last_match_keynum ==0:
                           json_data['text'] = "知识库没有答案"
                           json_data['answerid'] = 0
                       if last_match_keynum == 1:
                           answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).order_by(
                               '-visit_wegiht')
                           json_data['text'] = answerdata[0].answer_content
                           json_data['answerid'] = 0
                       if last_match_keynum == 2:
                           answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                               question_keyword__contains=tags[1]).order_by(
                               '-visit_wegiht')
                           json_data['text'] = answerdata[0].answer_content
                           json_data['answerid'] = 0
                       if last_match_keynum == 3:
                           answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                               question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).order_by(
                               '-visit_wegiht')
                           json_data['text'] = answerdata[0].answer_content
                           json_data['answerid'] = 0
                       if last_match_keynum == 4:
                           answerdata = Faq.objects.filter(question_keyword__contains=tags[0]).filter(
                               question_keyword__contains=tags[1]).filter(question_keyword__contains=tags[2]).filter(
                               question_keyword__contains=tags[3]).order_by(
                               '-visit_wegiht')
                           json_data['text'] = answerdata[0].answer_content
                           json_data['answerid'] = 0
                   else:
                       for j in range(0, 1000):
                           if temp_match_num[j]==0:
                               continue
                           else:
                               if maxmatch < float(difflib.SequenceMatcher(None, sentence, question[temp_match_num[j]-1].question_content.encode("utf-8")).ratio()) or maxmatch ==float(difflib.SequenceMatcher(None, sentence, question[temp_match_num[j]-1].question_content.encode("utf-8")).ratio()):
                                   maxweight=float(difflib.SequenceMatcher(None, sentence, question[temp_match_num[j]-1].question_content.encode("utf-8")).ratio())
                                   answerid = j+1
                       sentencemessage = Faq.objects.get(id=answerid)
                       count = Faq.objects.count()
                       json_data['text']=sentencemessage.answer_content
                       json_data['answerid'] = sentencemessage.id
                       sentencemessage.visit_wegiht+=1
                       sentencemessage.save()
                       model = Faq(id=count + 1, question_content=sentence, answer_content=json_data["text"],
                                   question_keyword=keyword, visit_wegiht=1,baidu_answer=json_data["baidutext"])
                       model.save()
                       json_data['answerid'] = model.id
               else:
                       print "关键词完全匹配"
                       data.order_by('-visit_wegiht')[0].visit_wegiht+=1
                       data.order_by('-visit_wegiht')[0].save()
                       json_data['text'] = data.order_by('-visit_wegiht')[0].answer_content
                       json_data['answerid'] =  data.order_by('-visit_wegiht')[0].id


            else:
                json_data['text'] = "知识库没有答案"
                json_data['answerid'] = 0
        else:
            print ("问题完全匹配本地数据库回答")
            message.visit_wegiht=message.visit_wegiht+1
            message.save()
            json_data['text'] = message.answer_content
            json_data['answerid'] = message.id

        #图灵答案
        url = 'http://www.tuling123.com/openapi/api'
        key = 'ae50cd76cf114d209e9a5cfdfe3e2adf'
       # key = '37c58bfcfd4c403c9c4baaa3644822ef'
        query = {'key': key, 'info': sentence, 'userid': '1'}
        headers = {'Content-type': 'text/html', 'charset': 'utf-8'}
        r = requests.get(url, params=query, headers=headers)
        tulingjson_data = r.json()
        if tulingjson_data["code"]==200000:
          json_data["tulingurl"]=tulingjson_data["url"]
        else:
            json_data["tulingurl"] = ""
        if json_data['answerid']==0:
            count = Faq.objects.count()
            Faq.objects.create(id=count+1,question_content=sentence,answer_content=tulingjson_data["text"], question_keyword=keyword, visit_wegiht=1)
            model = Faq(id=count + 1, question_content=sentence, answer_content=tulingjson_data["text"],
                        question_keyword=keyword, visit_wegiht=1,baidu_answer=json_data["baidutext"])
            model.save()
            json_data['tulingtext'] = model.answer_content
            json_data['tulinganswerid'] = model.id
        else:
            json_data['tulingtext'] =tulingjson_data["text"]
            json_data['tulinganswerid'] =0
            model=Faq.objects.get(id=json_data["answerid"])
            model.baidu_answer=json_data["baidutext"]
            model.save()


        return JsonResponse(json_data)

def spider_closing(spider):
    """Activates on spider closed signal"""
    log.msg("Closing reactor", level=log.INFO)
    reactor.stop()
def notThreadSafe(x):
    """do something that isn't thread-safe"""


def csanswer(request):
    if request.method == 'POST':
        receiveqid = request.POST['qid']
        receiveanswer = request.POST['qanswer']
        model = Faq.objects.get(id=receiveqid)
        if request.POST['isbaidu']=="1":
            receiveanswer=model.baidu_answer
        model.answer_content = receiveanswer
        model.save()
        json_data = {}
        return JsonResponse(json_data)


def star(request):
    if request.method == 'POST':
        stars = request.POST['stareva']
        wcontent = request.POST['wholecontent']
        time=request.POST['time']
    count = UserSession.objects.count()
    model = UserSession(id=count + 1, content=wcontent,time=time,user_evalution=stars)
    model.save()
    json_data = {}
    return JsonResponse(json_data)

def defineanswer(request):
    if request.method == 'POST':
        defineqid = request.POST['deqid']
        define_answer = request.POST['deanswer']
        print  defineqid, define_answer
        model = Faq.objects.get(id=defineqid)
        model.answer_content=define_answer
        model.save()
    json_data = {}
    return JsonResponse(json_data)
