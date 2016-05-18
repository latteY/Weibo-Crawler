# -*- coding: utf-8 -*-
import urllib2
import sys
from os import mkdir   #makedir
from bs4 import BeautifulSoup

##craw the content of an URL,return string##
def crawler(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'spider')

    # set cookie
    request.add_header('cookie',
                       '_T_WM=469be68685afe20cd84e2dbee27036c4;SUB=_2A256PQhUDeTxGeRK4lQZ9S3Kzz6IHXVZwagcrDV6PUJbrdANLRTNkW1LHetA_h_5TqgcJ-cblMBCRI9hhfy7ng..;gsid_CTandWM=4uud70dc1YC8ByW9oHxTPatxPam')
    #return html of url
    page = urllib2.urlopen(request)

    #Using BeautifulSoup to analyse the page
    soup = BeautifulSoup(page,'lxml')

    return soup
    
# user_agent = {'User-agent': 'spider'}
# r = requests.get("http://weibo.com/u/5110432155?from=feed&loc=at&nick=%E6%9D%8E%E5%B0%8F%E9%B9%8F&is_all=1http://weibo.com/u/5110432155?from=feed&loc=at&nick=%E6%9D%8E%E5%B0%8F%E9%B9%8F&is_all=1",headers=user_agent)


# url = "http://weibo.cn/u/5110432155/"  #LXP
#url = "http://weibo.cn/5110432155/fans"
# url="http://www.zhihu.com/collection/27109279?page=1"

# url="http://www.weibo.com"
# url = "http://weibo.com/youaresucking?from=feed&loc=nickname"
# url="https://cn.linkedin.com/in/kaifulee?trk=pub-pbmap"
# url = "http://bl.ocks.org/mbostock/4063269"

# url = "http://weibo.cn/1993545240" #bianbianyubaishui

data_path="data/"  #set the path of the data
mkdir(data_path)
nickname="leehom"
mkdir(data_path+nickname)

url = "http://weibo.cn/leehom"

soup = crawler(url)

#write to file
f = file(data_path+nickname+'/'+'leehom.html', 'w+')   
text = (soup.prettify()).encode("utf-8")   #to UTF8
#f.write(soup.prettify())  # write HTML into File
f.write(text)
f.close()
#finish the writing

body_tag = soup.body

for tag in body_tag.find_all('div'):       #找到“资料”的链接
    if tag['class'] == ['ut']:
        for tag_in_div in tag.find_all('a'):
            if tag_in_div.string and tag_in_div.string == u'资料':
                info_url = tag_in_div["href"]
                break
        break

info_url = 'http://weibo.cn'+info_url
print info_url

soup=crawler(info_url)

#write to file
f = file(data_path+nickname+'/'+'leehom_info.html', 'w+')
text = (soup.prettify()).encode("utf-8")  # to UTF8
# f.write(soup.prettify())  # write HTML into File
f.write(text)
f.close()
#finish the writing




'''
request = urllib2.Request(url)
request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
response = urllib2.urlopen(request)
html = html.decode('utf-8','replace').encode(sys.getfilesystemencoding())
print html
'''



