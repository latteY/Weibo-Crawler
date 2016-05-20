# -*- coding: utf-8 -*-
import urllib2
import sys
import os
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

def extract_info(soup):
    #从用户主页出发抽取用户的信息，soup为用户主页
    user_profile=dict()  #存储用户资料的字典

    # 找到“资料”的链接
    body_tag = soup.body

    for tag in body_tag.find_all('div'):
        if tag['class'] == ['ut']:
            for tag_in_div in tag.find_all('a'):
                if tag_in_div.string and tag_in_div.string == u'资料':
                    info_url = tag_in_div["href"]
                    break
            break

    info_url='http://weibo.cn'+info_url
    user_profile.setdefault('user_info_url',info_url)

    info_soup=crawler(info_url)
    user_profile.setdefault('info_soup', info_soup)

    #关注链接
    follow_url = info_url.replace('info','follow')
    follow_soup=crawler(follow_url)
    user_profile.setdefault('follow_soup', follow_soup)

    #粉丝连接
    fans_url=info_url.replace('info','fans')
    fans_soup=crawler(fans_url)
    user_profile.setdefault('fans_soup', fans_soup)

    #提取粉丝信息 extract user's profile link
    body_tag = soup.body

    for tag in body_tag.find_all('div'):
        if tag['class'] == ['ut']:
            for tag_in_div in tag.find_all('a'):
                if tag_in_div.string and tag_in_div.string == u'资料':
                    info_url = tag_in_div["href"]
                    break
            break

    #extract user's follow list
    user_profile.setdefault('follow_list',list()) #construct data structure

    body_tag = follow_soup.body

    for table_tag in body_tag.find_all('table'):
        for _tag in table_tag.find_all()
        
        if tag['class'] == ['ut']:
            for tag_in_div in tag.find_all('a'):
                if tag_in_div.string and tag_in_div.string == u'资料':
                    info_url = tag_in_div["href"]
                    break
            break
    
    
    return user_profile

def write2file(soup,name,path='data/'):
    '''soup是要写入文件的内容，name是文件名，path是文件写入路径（默认是：crawler.py所在
    路径/data/),mode='absolute_path'时需要填绝对路径,若路径不存在会自动创建）
    mode='data'时，识别文件名中包含的用户名并写入相应用户的文件夹'''

    #check if has file 'data' in the dir,if not, add the file 'data'
    if path.endswith('/data') or path.endswith('/data/'):  
        pass
    else:
        path = path + '/data'
    
    if not os.path.exists(path):
        os.makedirs(path)     # make the directory of the data

    if name.find('_')==-1:    #提取用户名,name中不包含“_”就返回-1
        username = name.split('.')[0]
    else:
        username = name.split('_')[0]

    if not os.path.exists(path+'/'+username):  #若某用户的文件夹不存在
        os.makedirs(path+'/'+username)  # make the directory of the data

    f = file(path + '/' +username + '/' + name, 'w+')

    if type(soup) == type(BeautifulSoup('','lxml')):
        text = (soup.prettify()).encode("utf-8")  # to UTF8

    f.write(text)
    f.close()
    # finish writing

# user_agent = {'User-agent': 'spider'}
# r = requests.get("http://weibo.com/u/5110432155?from=feed&loc=at&nick=%E6%9D%8E%E5%B0%8F%E9%B9%8F&is_all=1http://weibo.com/u/5110432155?from=feed&loc=at&nick=%E6%9D%8E%E5%B0%8F%E9%B9%8F&is_all=1",headers=user_agent)


# url = "http://weibo.cn/u/5110432155/"  #LXP
#url = "http://weibo.cn/5110432155/fans"

# url="http://www.weibo.com"
# url = "http://weibo.com/youaresucking?from=feed&loc=nickname"
# url="https://cn.linkedin.com/in/kaifulee?trk=pub-pbmap"
# url = "http://bl.ocks.org/mbostock/4063269"

# url = "http://weibo.cn/1993545240" #bianbianyubaishui

url = "http://weibo.cn/leehom"

soup = crawler(url)

user_profile=dict()
user_profile=extract_info(soup)

follow_soup = user_profile['follow_soup']
fans_soup = user_profile['fans_soup']
info_soup = user_profile['info_soup']

write2file(soup,'leehom.html',path='/home/ndscbigdata/')
write2file(user_profile['fans_soup'],'leehom_fans.html',path='/home/ndscbigdata/')
write2file(user_profile['follow_soup'],'leehom_follow.html',path='/home/ndscbigdata/')
write2file(user_profile['info_soup'],'leehom_info.html',path='/home/ndscbigdata/')
