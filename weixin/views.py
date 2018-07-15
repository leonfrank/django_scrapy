import markdown
from datetime import timedelta,datetime
from django.db.models import Sum,Q
from django.shortcuts import HttpResponse
from django.shortcuts import render,get_object_or_404
from .scrapy import *
from .models import CompResult


def index(request):
    return render(request, 'weixin/index.html')
# Create your views here.
def stats(request):
    '''
    q = request.GET.get('q')
    keywords = request.GET.get('keywords')
    #print(q,keywords)
    if not q:
        error_msg = '请输入公司名'
        return render(request,'comp/error.html',{'error_msg':error_msg})
    elif not keywords:
        error_msg = '请输入关键字'
        return render(request, 'comp/error.html', {'error_msg': error_msg})

    comps = q.strip().split()
    '''
    #CompResult.objects.all().delete()
    timerange = request.GET.get("timerange")
    if timerange == "oneday":
        starttime,endtime = datetime.date(datetime.today())-timedelta(days=1), datetime.date(datetime.today())
    elif timerange == "onemonth":
        starttime,endtime = datetime.date(datetime.today())-timedelta(days=30), datetime.date(datetime.today())
    comp_list = CompResult.objects.all().filter(created_time__range=[starttime,endtime]).values('company').annotate(title_score = Sum('title_score')).order_by()

    #print(type(comp_list))
    return render(request,'weixin/scrapy.html',{'comp_list':comp_list})
def details(request,comp):
    starttime, endtime = datetime.now() - timedelta(days=1), datetime.now()
    details = CompResult.objects.filter(Q(company = comp),created_time__range = [starttime,endtime] )
    #print(type(details))
    return render(request,'weixin/detail.html',{'comp':comp,'details':details})

def update():
    comps = ['阿里巴巴', '百度', '京东', '万科集团', '世贸集团']
    keywords = ['违约', '法院', '诉讼', '风险']
    searchOptions = default_searchOptions()

    for comp in comps:
        # print(comp)
        newsData = get_list(comp, keywords, searchOptions)
        for record in newsData:
            compresult = CompResult(title=record['title'], company=comp, created_time=record['scrapy_time'],
                                    title_score=record['title_score'], wx_link=record['wx_link'])
            compresult.save()

    print(datetime.datetime.now(), "news_count:", len(newsData))
