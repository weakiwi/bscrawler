#coding=utf-8
import urllib2
import urllib
import cookielib
import re
import jieba.analyse
import time
from multiprocessing import Pool
from bs4 import BeautifulSoup

def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
#        print "%s ValueError" % num
        return False

def hianalyse(num):
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)

	loginURL = 'http://www.hi-pda.com/forum/logging.php?action=login'#登陆网址

	postdata = {							#构造登陆数据
		'formhash' : '7fb05e5b',
		'referer' : 'index.php',
		'loginfield' : 'username',
		'username' : '用户名',
		'password' : '密码',
		'questionid' : '0',
		'answer' : '',
		'loginsubmit' : 'true',
		'cookietime' : '2592000'}

	postdata = urllib.urlencode(postdata)
	opener.open(loginURL,postdata)

	DiscoveryURL = 'http://www.hi-pda.com/forum/forumdisplay.php?fid=2&orderby=dateline&filter=2592000&page='+str(num)
	response = opener.open(DiscoveryURL)
	page = BeautifulSoup(response)
	urls = page.find_all(href = re.compile('viewthread\.php\?tid=\d*'))
	
	counter = 2
	for i in urls:
		if counter%2 == 0:
			f = open('temp_'+str(num)+'.txt','a+')
			f.write('http://www.hi-pda.com/forum/'+str(i.get('href'))+'\n')
			f.close()
		counter+=1#因为处理的网也中有重复，所以跳着来写网页
	print 'get url task '+str(num)+' done!!!'

	f = open('temp_'+str(num)+'.txt','r')
	for line in f.readlines():
		response = opener.open(line)
		page = BeautifulSoup(response)
		content = page.find_all(id = re.compile('postmessage_'))#获取帖子正文
		for i in content:
			fcontent = open('temp_content.txt','a+')
			fcontent.write(i.get_text().encode('utf-8'))
			fcontent.close()
	print 'task  '+str(num)+'done!!!'

"""
	msg = ''
	for page_num in range(num*100-99, num*100):
		bsURL = 'http://www.hi-pda.com/forum/forumdisplay.php?fid=2&page='+str(page_num)
		response = opener.open(bsURL)
		page = BeautifulSoup(response)
		tag = page.find_all(href = re.compile('viewthread\.php\?tid=\d*'))
	for each_tag in tag:
		if is_num_by_except(each_tag.get_text()) == True:
			continue
		else:
			each_tag = each_tag.get_text().encode('utf-8')
			msg = msg + each_tag
	print 'task '+str(num)+' done!!!' 
	f = open('temp.txt','a+')
	f.write(msg)
	f.close()

if __name__ == '__main__':
	p = Pool()
	for i in range(10):
		p.apply_async(hianalyse,args=(i,))
	p.close()
	p.join()

"""
if __name__ == '__main__':
	p = Pool()
	for i in range(1,300):#多线程处理
		p.apply_async(hianalyse,args=(i,))
	p.close()
	p.join()
