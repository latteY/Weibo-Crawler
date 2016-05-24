# -*- coding: utf-8 -*-
import urllib2
import sys
import os
from bs4 import BeautifulSoup
import re
import threading
import time
from Queue import Queue

lock = threading.RLock()  # 锁——用于需要原子操作的地方(可重入锁)

def request_page(url):
    '''craw the content of an URL,return soup object'''
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'spider')

    # set cookie
    request.add_header('cookie','_T_WM=469be68685afe20cd84e2dbee27036c4;SUB=_2A256PQhUDeTxGeRK4lQZ9S3Kzz6IHXVZwagcrDV6PUJbrdANLRTNkW1LHetA_h_5TqgcJ-cblMBCRI9hhfy7ng..;gsid_CTandWM=4uud70dc1YC8ByW9oHxTPatxPam')
    
    # return html of url
    page = urllib2.urlopen(request)

    # Using BeautifulSoup to analyse the page
    soup = BeautifulSoup(page, 'lxml')

    return soup

def crawl(url):
    # 从用户主页出发抽取用户的信息，url为用户主页
    homepage = request_page(url)  #请求用户主页

    user_profile = dict()  # 存储用户资料的字典
    user_profile.setdefault('homepage',homepage) #将首页信息写入字典

    # 找到“基本资料”的链接
    body_tag = homepage.body

    info_url=str()
    for tag in body_tag.find_all('div'):
        if tag['class'] == ['ut']:
            for tag_in_div in tag.find_all('a'):
                if tag_in_div.string and tag_in_div.string == u'资料':
                    info_url = tag_in_div["href"]
                    break
            break

    info_url = 'http://weibo.cn' + info_url

    user_profile.setdefault('user_info_url', info_url)

    info_soup = request_page(info_url)
    user_profile.setdefault('info_soup', info_soup)

    '''
    f=file('data/info.html','w+')
    text = (info_soup.prettify()).encode("utf-8")
    f.write(text)
    f.close()
    '''
    # 在资料页中中找出用户的昵称
    username = info_soup.find_all(text=re.compile(u'昵称:'))  # 搜索含有"昵称:"的字符串
    username = username[0].split(':')[1]  # 将用户名存入username
    testlist.append(username)
    user_profile.setdefault('username', username)

    # 关注链接
    follow_url = info_url.replace('info', 'follow')
    follow_soup = request_page(follow_url)
    user_profile.setdefault('follow_soup', follow_soup)

    # 粉丝连接
    fans_url = info_url.replace('info', 'fans')
    fans_soup = request_page(fans_url)
    user_profile.setdefault('fans_soup', fans_soup)

    # 提取用户关注的人，将他们的URL通过list()存储
    user_profile.setdefault('follow_list', list())  # construct data structure

    body_tag = follow_soup.body

    # 暂时先爬一页的关注列表
    for table_tag in body_tag.find_all('table', recursive=False):
        followlist = user_profile['follow_list']
        followlist.append(table_tag.a['href'])  # list是可变对象所以，followlist变，user_profile['follow_list']也变

    return user_profile

def write2file(object, path='data/'):
    '''object是存储用户信息的字典，path是文件写入路径（默认是：crawler.py所在
    路径下的data文件夹),mode='absolute_path'时需要填绝对路径,若路径不存在会自动创建'''

    # check if has file 'data' in the dir,if not, add the file 'data'
    if path == 'data/':
        pass
    else:
        path = path + '/data'

    if not os.path.exists(path):
        os.makedirs(path)  # make the directory of the data

    if type(object) == type(dict()):
        user_profile = object
        username = user_profile['username']

        if not os.path.exists(path + '/' + username):  # 若某用户的文件夹不存在
            os.makedirs(path + '/' + username)  # make the directory of the data

        FileNameList = ['homepage','fans_soup','follow_soup','info_soup']

        for i in range(len(FileNameList)):
            if user_profile.has_key(FileNameList[i]):
                f = file(path + '/' + username + '/' + username+'_'+FileNameList[i].split('_')[0]+'.html', 'w+')
                # if type(soup) == type(BeautifulSoup('', 'lxml')):
                text = (user_profile[FileNameList[i]].prettify()).encode("utf-8")  # to UTF8
                f.write(text)  #写文件
                f.close()
            else:
                print FileNameList[i]+'is not in user_profile(user_profile is a dict)'
        # finish writing
    return

class Crawler_Thread(threading.Thread):
    def run(self):
        global queue
        global visited_url
        global url_in_queue

        while len(visited_url)<50:
            print self.name + ' in....' + '\n'
            lock.acquire()
            url = queue.get()
            visited_url.setdefault(url, '')
            lock.release()

            user_profile = dict()  # 存放用户基本信息
            user_profile = crawl(url)

            Followlist = user_profile['follow_list']

            lock.acquire()
            for i in range(len(Followlist)):
                if visited_url.has_key(Followlist[i]):
                    continue
                if url_in_queue.has_key(Followlist[i]):
                    continue
                queue.put(Followlist[i])
                url_in_queue.setdefault(Followlist[i], '')
            lock.release()

            write2file(user_profile)
            print self.name + 'over' + '\n'
            time.sleep(0.5)
        #exit()

#seed url
seedurl = list()
seedurl.append("http://weibo.cn/leehom")
seedurl.append("http://weibo.cn/huangbo")
seedurl.append("http://weibo.cn/kaifulee")
seedurl.append("http://weibo.cn/guodegang")
seedurl.append("http://weibo.cn/happyzhangjiang")
seedurl.append("http://weibo.cn/jlin7")

queue = Queue()  # 存放尚未被访问过的URL
visited_url = dict()  # 存放已经被访问过的URL，用于快速查询
url_in_queue = dict()  # 存放queue中URL，用于快速查询

testlist=list()

for i in range(len(seedurl)):
    queue.put(seedurl[i])

for i in range(len(seedurl)):
    url_in_queue.setdefault(seedurl[i], '')

if __name__ == '__main__':
    #create thread

    for j in range(5):
        t = Crawler_Thread()
        t.start()

    #print queue.qsize()

# 将关注列表写入文件
'''
f=file('data/list.txt','w+')
for i in range(10):
    f.write(user_profile['follow_list'][i]+'\n')
f.close()
'''
