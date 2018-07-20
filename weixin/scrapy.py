import sys
import urllib
import re
import os
from  bs4 import BeautifulSoup
from urllib.parse import urlencode
import time
import datetime
import pytz
import gc
def scoring(line,keywords):
    score = 0
    for kwd in keywords:
        if line.find(kwd)!=-1:
            score = score - 10
    return score
def get_wx_body(wx_link):
    wx_headers = {
        "Host": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        # "Referer":"http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4&tsn=1&ft=&et=&interation=&wxid=&usip="
    }
    req = urllib.request.Request(wx_link, headers=wx_headers)
    response = urllib.request.urlopen(req)
    h = response.read()
    soup = BeautifulSoup(h,'html.parser')
    paras = soup.find_all('p')
    body = [p.get_text() for p in paras]
    return ''.join(body)

def extract_content(div,keywords):
    title = div.find('a').get_text()
    wx_link = div.find('a').get('href')
    #body = get_wx_body(wx_link)
    title_score = scoring(title,keywords)
    #body_score = scoring(body,keywords)
    script = div.find('script')
    timestamp = re.search('\d+', script.get_text()).group(0)
    scrapy_time= datetime.datetime.fromtimestamp(
        int(timestamp),tz = pytz.timezone('Asia/Shanghai'))
    cont = {'title':title,'scrapy_time':scrapy_time,'title_score':title_score,'wx_link':wx_link}
    return  cont

def get_list(comp,keywords,searchOptions,opener):
    newsData = []
    start_url = "http://weixin.sogou.com/weixin?"
    #keywords = keywords.strip().split()    
    query = comp
    d = {'type': 2 ,'ie':'utf8','query':query,'page':1}
    d.update(searchOptions)

    for i in range(1,11):#前10页爬取
        d['page'] = i
        pname  = urlencode(d)
        href = start_url + pname
        print(href)
        hdr = {"Host":"weixin.sogou.com","Referer":href,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
        req = urllib.request.Request(href,headers = hdr)
        response = opener.open(req)
        html = response.read()
        soup = BeautifulSoup(html,'html.parser')
        divs = soup.find_all('div',{'class':'txt-box'})        
        for div in divs:
            newsData.append(extract_content(div,keywords))        
        time.sleep(10)
    '''
    x_label = range(len(keywords))
    y_data = newsData.values()
    font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\msyhl.ttc", size=14)  # C:\WINDOWS\Fonts
    plt.bar(x_label,y_data,align ='center',alpha = 0.5)
    plt.xticks(x_label,keywords,fontproperties = font)
    plt.ylabel(u"搜索结果条数",fontproperties=font)
    plt.title((u"%s公司微信关键词搜索统计" %comp),fontproperties = font)
    TT = str(int(time.time()))
    plt.savefig('static/comp/img/'+comp+'-'+TT+'.png')
    '''
    gc.collect()
    return newsData

def default_searchOptions():
    searchOptions = {}
    # tsn = 1 & ft = & et = & interation = & wxid = & usip =
    searchOptions['tsn'] = 1
    searchOptions['ft'] = ''
    searchOptions['et'] = ''
    searchOptions['interation'] = ''
    searchOptions['wxid'] = ''
    searchOptions['usip'] = ''
    
    return searchOptions

def get_proxy():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H98Q204O5T48O3TD"
    proxyPass = "624F33F77FFF3527"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host" : proxyHost,
        "port" : proxyPort,
        "user" : proxyUser,
        "pass" : proxyPass,
    }

    proxy_handler = urllib.request.ProxyHandler({
        "http"  : proxyMeta,
        "https" : proxyMeta,
    })

    #auth = request.HTTPBasicAuthHandler()
    #opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)

    opener = urllib.request.build_opener(proxy_handler)
    return opener
def main():

    comps = ['阿里巴巴', '百度', '京东', '万科集团', '世贸集团']
    keywords = ['违约', '法院', '诉讼', '风险']
    searchOptions = default_searchOptions()
    opener = get_proxy()
    total= 0
    
    for comp in comps:
        print(comp)
        start_time = time.time()
        newsData = get_list(comp, keywords, searchOptions,opener)
        total += len(newsData)
        '''
        for record in newsData:
            compresult = CompResult(title=record['title'], company=comp, created_time=record['scrapy_time'],
                                    title_score=record['title_score'], wx_link=record['wx_link'])
            compresult.save()
        '''
        print(time.time()-start_time)
    print(datetime.datetime.now(),"news_count:",total)

def check():
    print ("hello django crontab")
if __name__=='__main__':
    main()
